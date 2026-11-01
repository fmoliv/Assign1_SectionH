"""
Esqueleto de coletor diário para o FinOps simples de IA.

Coleta ontem (UTC) de quatro fontes, normaliza para o formato de fato_uso_ia
e grava em CSV (troque gravar_csv por INSERT no Postgres/BigQuery ou append no Sheets).

Variáveis de ambiente esperadas:
  ANTHROPIC_ANALYTICS_KEY   chave read:analytics (Enterprise) ou Admin API key (Console)
  MS_TENANT_ID, MS_CLIENT_ID, MS_CLIENT_SECRET   app registration com Reports.Read.All (application)
  GOOGLE_SA_JSON            caminho do JSON da service account com domain-wide delegation
  GOOGLE_ADMIN_EMAIL        admin a ser impersonado
  LITELLM_URL, LITELLM_MASTER_KEY
"""
import csv, datetime as dt, json, os, sys, urllib.parse, urllib.request

ONTEM = (dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=1))
INICIO = f"{ONTEM}T00:00:00Z"
FIM = f"{ONTEM + dt.timedelta(days=1)}T00:00:00Z"


def http_json(url, headers=None, data=None):
    req = urllib.request.Request(url, headers=headers or {}, data=data)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def linha(email, fornecedor, produto, canal, atividade, unidade, custo_usd, metodo, origem):
    return dict(data=str(ONTEM), email=email.lower(), fornecedor=fornecedor, produto=produto, canal=canal,
                atividade=atividade, unidade=unidade, custo_usd=round(custo_usd, 4), metodo_custo=metodo, origem=origem)


# 1. Claude: chat, Claude Code, Cowork e API, custo medido por pessoa e produto
def coletar_claude():
    chave = os.environ["ANTHROPIC_ANALYTICS_KEY"]
    h = {"x-api-key": chave, "anthropic-version": "2023-06-01",
         "anthropic-beta": "analytics-usage-cost-2026-08-24"}
    out, page = [], None
    while True:
        q = {"starting_at": INICIO, "ending_at": FIM, "time_bucket_width": "1d",
             "group_by[]": ["actor", "product"], "actor_types[]": "user_actor", "limit": 1000}
        if page:
            q["page"] = page
        url = "https://api.anthropic.com/v1/organizations/analytics/cost?" + urllib.parse.urlencode(q, doseq=True)
        resp = http_json(url, h)
        for row in resp.get("data", []):
            actor = (row.get("group") or {}).get("actor") or {}
            email = actor.get("email_address")
            if not email:
                continue
            produto = (row["group"].get("product") or "claude_api")
            canal = "api" if produto in ("claude_api",) else "chat"
            if produto == "claude_code":
                canal = "api"
            usd = float(row["cost"]["amount"]) / 100.0  # centavos -> dólar
            out.append(linha(email, "anthropic", produto, canal, 0, "tokens", usd, "medido", "claude_analytics_api"))
        if not resp.get("has_more"):
            break
        page = resp.get("next_page")
    # Para tokens por pessoa, repita o mesmo loop em /analytics/usage e some usage.input_tokens + output_tokens
    return out


# 2. Microsoft 365 Copilot: dia ativo por usuário (custo vem do rateio do assento)
def coletar_copilot():
    tenant, cid, sec = os.environ["MS_TENANT_ID"], os.environ["MS_CLIENT_ID"], os.environ["MS_CLIENT_SECRET"]
    tok = http_json(f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token",
                    {"Content-Type": "application/x-www-form-urlencoded"},
                    urllib.parse.urlencode({"client_id": cid, "client_secret": sec, "grant_type": "client_credentials",
                                            "scope": "https://graph.microsoft.com/.default"}).encode())["access_token"]
    h = {"Authorization": f"Bearer {tok}"}
    url = "https://graph.microsoft.com/beta/reports/getMicrosoft365CopilotUsageUserDetail(period='D7')?$format=application/json"
    out = []
    while url:
        resp = http_json(url, h)
        for u in resp.get("value", []):
            # dia ativo = última atividade igual a ontem (o relatório só traz datas; prompts chegam na versão nova)
            if u.get("lastActivityDate") == str(ONTEM):
                out.append(linha(u["userPrincipalName"], "microsoft", "copilot_m365", "chat", 1, "dia_ativo", 0, "assento_rateado", "graph_api"))
        url = resp.get("@odata.nextLink")
    return out


# 3. Gemini no Workspace: eventos por usuário via Reports API (custo vem do rateio do assento)
def coletar_gemini_workspace():
    from google.oauth2 import service_account  # pip install google-auth google-api-python-client
    from googleapiclient.discovery import build
    cred = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_SA_JSON"], scopes=["https://www.googleapis.com/auth/admin.reports.audit.readonly"]
    ).with_subject(os.environ["GOOGLE_ADMIN_EMAIL"])
    svc = build("admin", "reports_v1", credentials=cred)
    contagem, token = {}, None
    while True:
        r = svc.activities().list(userKey="all", applicationName="gemini_in_workspace_apps",
                                  startTime=INICIO, endTime=FIM, pageToken=token, maxResults=1000).execute()
        for it in r.get("items", []):
            email = it["actor"].get("email")
            if email:
                contagem[email] = contagem.get(email, 0) + len(it.get("events", []))
        token = r.get("nextPageToken")
        if not token:
            break
    out = []
    for email, n in contagem.items():
        out.append(linha(email, "google", "gemini_workspace", "chat", n, "eventos", 0, "assento_rateado", "google_reports_api"))
        out.append(linha(email, "google", "gemini_workspace", "chat", 1, "dia_ativo", 0, "assento_rateado", "google_reports_api"))
    return out


# 4. LiteLLM: custo medido por pessoa em todas as APIs que passam pelo gateway
def coletar_litellm():
    base, key = os.environ["LITELLM_URL"].rstrip("/"), os.environ["LITELLM_MASTER_KEY"]
    h = {"Authorization": f"Bearer {key}"}
    url = f"{base}/global/spend/report?start_date={ONTEM}&end_date={ONTEM}&group_by=internal_user"
    out = []
    for row in http_json(url, h):
        email = row.get("user_email") or row.get("internal_user") or row.get("user_id")
        if not email:
            continue
        modelo = row.get("model") or ""
        fornecedor = "anthropic" if "claude" in modelo else "google" if "gemini" in modelo else "microsoft" if "azure" in modelo else "outro"
        produto = {"anthropic": "claude_api", "google": "gemini_api", "microsoft": "azure_openai"}.get(fornecedor, "api_outra")
        out.append(linha(email, fornecedor, produto, "api", float(row.get("total_tokens") or 0), "tokens",
                         float(row.get("total_spend") or 0), "medido", "litellm"))
    return out


# 5. PTAX de venda do dia (Banco Central)
def ptax(d):
    ds = d.strftime("%m-%d-%Y")
    url = ("https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
           f"CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{ds}'&$format=json")
    v = http_json(url).get("value") or []
    return v[-1]["cotacaoVenda"] if v else None


def gravar_csv(linhas, caminho):
    campos = ["data", "email", "fornecedor", "produto", "canal", "atividade", "unidade", "custo_usd", "metodo_custo", "origem"]
    novo = not os.path.exists(caminho)
    with open(caminho, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        if novo:
            w.writeheader()
        w.writerows(linhas)


if __name__ == "__main__":
    todas = []
    for nome, fn in [("claude", coletar_claude), ("copilot", coletar_copilot),
                     ("gemini", coletar_gemini_workspace), ("litellm", coletar_litellm)]:
        try:
            l = fn(); todas += l; print(f"{nome}: {len(l)} linhas", file=sys.stderr)
        except KeyError as e:
            print(f"{nome}: pulado, falta variável {e}", file=sys.stderr)
        except Exception as e:
            print(f"{nome}: erro {e}", file=sys.stderr)
    gravar_csv(todas, "fato_uso_ia.csv")
    cot = ptax(ONTEM)
    if cot:
        novo = not os.path.exists("dim_cambio.csv")
        with open("dim_cambio.csv", "a", newline="") as f:  # troque por INSERT em dim_cambio
            w = csv.DictWriter(f, fieldnames=["data", "usd_brl"])
            if novo:
                w.writeheader()
            w.writerow({"data": str(ONTEM), "usd_brl": cot})
        print(f"PTAX {ONTEM}: {cot}", file=sys.stderr)
