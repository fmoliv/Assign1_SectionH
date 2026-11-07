# FinOps simples de IA: Copilot, Claude e Gemini, chat e API, por usuário

Objetivo: uma tabela só, atualizada todo dia, que responda por pessoa "quanto por cento do uso é dela" e "quanto custa em real ou dólar", cobrindo contas corporativas de Microsoft 365 Copilot, Claude e Gemini, tanto no chat quanto na API. Contas pessoais ficam fora do custo, mas entram como alerta.

## 1. A ideia central: dois tipos de produto, duas fórmulas

| Tipo | Produtos | Como o fornecedor cobra | Custo por usuário | Percentual de uso |
|---|---|---|---|---|
| **Assento** | Copilot M365, Gemini no Workspace, Claude Team | preço fixo por licença | preço do assento, rateado (não varia com o uso) | atividade do usuário dividida pela atividade total do produto |
| **Consumo** | Claude Enterprise, API Anthropic, API Gemini (Vertex), Azure OpenAI, agentes Copilot (créditos) | tokens ou créditos | custo medido pelo fornecedor, em dólar | custo do usuário dividido pelo custo total |

A unidade de atividade muda por produto, e isso é aceitável: o percentual é sempre relativo dentro do mesmo produto.

| Produto | Unidade de atividade por usuário | Fonte |
|---|---|---|
| Copilot M365 | dias ativos no período, ou prompts (métrica nova de 2026) | Graph API |
| Gemini Workspace | dias ativos (28 dias) ou eventos `active_generate` e `active_summarize` | Admin console e Reports API |
| Claude Team | mensagens e tokens | spend report CSV |
| Claude Enterprise, Claude Code, Cowork | tokens e dólar | Analytics API |
| APIs (Anthropic, Vertex, Azure OpenAI) | tokens e dólar | gateway LiteLLM ou billing do provedor |

Para produto por assento, dois números derivados valem mais que o percentual: **custo por dia ativo** (assento dividido por dias ativos; assento de US$ 30 com 2 dias ativos custa US$ 15 por dia de uso) e **assento ocioso** (zero atividade em 30 dias).

## 2. Fontes de dados por produto

### Claude (chat, Claude Code, Cowork e API) numa só API

Anthropic unificou tudo na Usage and Cost Analytics API. Os mesmos dois endpoints servem Claude Enterprise e Claude Console (API):

```
GET https://api.anthropic.com/v1/organizations/analytics/cost
GET https://api.anthropic.com/v1/organizations/analytics/usage
headers: x-api-key, anthropic-version: 2023-06-01, anthropic-beta: analytics-usage-cost-2026-08-24
params: starting_at, ending_at, time_bucket_width=1d,
        group_by[]=actor&group_by[]=product, actor_types[]=user_actor, limit=1000
```

- Chave: no Enterprise, chave com escopo `read:analytics` criada pelo Primary Owner em claude.ai. No Console (API), Admin API key.
- `actor` traz `email_address`; `product` separa `chat`, `claude_code`, `cowork`, `office_agent`, `claude_tag`. `amount` vem em centavos com seis casas: `"41280.000000"` é US$ 412,80.
- Janela: no máximo 31 dias por chamada, até 365 dias para trás. Dados têm atraso de um dia.
- Na API, o actor só é a pessoa se a chave for pessoal (ou login sem chave no Claude Code). Chave de workspace legada aparece como a própria chave. Regra: uma chave pessoal por desenvolvedor; aplicações compartilhadas ganham um workspace por projeto e o custo é rateado ou atribuído ao projeto, não a uma pessoa.
- Claude Team não tem API. Exporte o spend report (Settings > Analytics > Export spend report) uma vez por mês. O CSV tem e-mail, produto, modelo, tokens e gasto em dólar por linha.

### Gemini no Workspace (chat)

- Custo: assento. Preço da edição (Business Standard US$ 14 anual, por exemplo) rateado por usuário licenciado.
- Atividade por usuário: Admin console > Generative AI > Gemini reports > User-level usage, exportar CSV (dias ativos, nível de uso, uso por app, últimos 28 dias). Para automatizar, Reports API do Admin SDK: `activities.list` com `applicationName=gemini_in_workspace_apps`, que devolve eventos por usuário com `actor.email`, app e categoria (`active_generate`, `active_summarize`). Escopo `admin.reports.audit.readonly`.
- Atraso de 2 a 3 dias. Não há tokens nem dólar por pessoa, e não vai haver: é licença fixa.

### Gemini via API (Vertex AI ou AI Studio)

Duas opções. A simples é passar tudo por um gateway (seção 3). A alternativa nativa: chamar Vertex AI com `labels` em cada `generateContent` (`user=email`, `team=...`), ligar o export detalhado de billing para BigQuery e somar `cost` por label. Chaves do AI Studio não aceitam labels, então todas as chaves de um projeto viram um total só.

### Microsoft 365 Copilot (chat nos apps)

- Custo: assento de US$ 30 (Enterprise) ou US$ 21 (Business), rateado.
- Atividade por usuário: Graph API, permissão `Reports.Read.All`:

```
GET https://graph.microsoft.com/beta/reports/getMicrosoft365CopilotUsageUserDetail(period='D30')?$format=application/json
```

Devolve `userPrincipalName`, `lastActivityDate` e a última atividade por app (Teams, Word, Excel, PowerPoint, Outlook, Copilot Chat). A Microsoft está migrando para o caminho `/copilot/reports/` e adicionando contagem de prompts e dias ativos por usuário. Os nomes vêm mascarados por padrão; desligue a ocultação em Admin center > Settings > Org settings > Reports.
- Só usuários com licença Copilot aparecem. Copilot Chat gratuito fica fora do Graph.
- Agentes e Copilot Studio por consumo: créditos aparecem no Azure Cost Management; exporte o custo diário por meter e atribua ao dono do agente.
- Azure OpenAI (API): o custo nativo é por recurso, não por pessoa. Use o gateway ou a política `azure-openai-emit-token-metric` do API Management com `User ID` como dimensão.

### A peça que simplifica tudo na API: um gateway

Coloque o LiteLLM (open source) na frente de todas as APIs: Anthropic, Vertex AI, Azure OpenAI. Cada pessoa recebe uma chave virtual com `user_id`, `team` e `tags` de projeto. O gateway grava tokens e custo em dólar por requisição na tabela `LiteLLM_SpendLogs`, com o mesmo formato para os três fornecedores, e impõe orçamento por chave e time. Sem isso, cada fornecedor exige um método diferente de atribuição.

## 3. Modelo de dados: três tabelas

```sql
-- Um registro por pessoa, produto, canal e dia
CREATE TABLE fato_uso_ia (
  data            DATE,
  email           TEXT,          -- chave de junção com RH/SSO
  fornecedor      TEXT,          -- anthropic | google | microsoft
  produto         TEXT,          -- claude_chat | claude_code | cowork | gemini_workspace | gemini_api | copilot_m365 | copilot_agentes | azure_openai | claude_api
  canal           TEXT,          -- chat | api
  atividade       NUMERIC,       -- tokens, eventos, prompts ou 1 (dia ativo)
  unidade         TEXT,          -- tokens | eventos | prompts | dia_ativo
  custo_usd       NUMERIC(12,4), -- medido ou rateado
  metodo_custo    TEXT,          -- medido | assento_rateado
  origem          TEXT,          -- claude_analytics_api | graph_api | google_reports_api | litellm | csv_manual
  PRIMARY KEY (data, email, produto, canal, origem)
);

CREATE TABLE dim_usuario (
  email TEXT PRIMARY KEY, nome TEXT, departamento TEXT, centro_custo TEXT, gestor TEXT, ativo BOOLEAN
);

CREATE TABLE dim_cambio (
  data DATE PRIMARY KEY, usd_brl NUMERIC(10,4)   -- PTAX de venda do dia
);

-- Assentos: quem tem licença de quê e quanto custa por mês
CREATE TABLE dim_assento (
  email TEXT, produto TEXT, preco_usd_mes NUMERIC(10,2), inicio DATE, fim DATE
);
```

Rateio do assento: todo dia, para cada licença ativa, insira uma linha com `custo_usd = preco_usd_mes / dias_do_mes` e `metodo_custo = 'assento_rateado'`. Assim o custo mensal fecha com a fatura e o relatório diário não depende de o usuário ter usado.

## 4. As consultas que respondem a pergunta

```sql
-- Percentual de uso e de custo por pessoa e produto, no mês
WITH base AS (
  SELECT email, produto, canal,
         SUM(atividade) AS atividade,
         SUM(custo_usd) AS custo_usd,
         SUM(custo_usd * c.usd_brl) AS custo_brl
  FROM fato_uso_ia f JOIN dim_cambio c USING (data)
  WHERE data >= DATE_TRUNC('month', CURRENT_DATE)
  GROUP BY 1,2,3
)
SELECT b.email, u.departamento, b.produto, b.canal,
       b.atividade,
       ROUND(100.0 * b.atividade / SUM(b.atividade) OVER (PARTITION BY b.produto), 1) AS pct_uso_no_produto,
       b.custo_usd, b.custo_brl,
       ROUND(100.0 * b.custo_usd / SUM(b.custo_usd) OVER (), 1)                      AS pct_custo_total
FROM base b LEFT JOIN dim_usuario u USING (email)
ORDER BY custo_usd DESC;

-- Assentos ociosos (30 dias sem atividade) e custo por dia ativo
SELECT a.email, a.produto, a.preco_usd_mes,
       COALESCE(SUM(CASE WHEN f.unidade='dia_ativo' THEN f.atividade END), 0) AS dias_ativos_30d,
       a.preco_usd_mes / NULLIF(SUM(CASE WHEN f.unidade='dia_ativo' THEN f.atividade END),0) AS usd_por_dia_ativo
FROM dim_assento a
LEFT JOIN fato_uso_ia f ON f.email=a.email AND f.produto=a.produto AND f.data >= CURRENT_DATE - 30
WHERE a.fim IS NULL
GROUP BY 1,2,3
ORDER BY dias_ativos_30d ASC;
```

Resultado típico por linha: `maria@empresa.com | Engenharia | claude_code | api | 2,1 M tokens | 18,4 % do produto | US$ 61,20 | R$ 331,78 | 7,9 % do total`.

## 5. Pipeline mínimo

```
[Claude Analytics API] ─┐
[Graph API Copilot]    ─┤   script Python diário        tabela fato_uso_ia        painel
[Google Reports API]   ─┼─► (cron, GitHub Actions ou ─► (Postgres, BigQuery ─► (Looker Studio,
[LiteLLM SpendLogs]    ─┤    Cloud Run Job, 5 min)       ou Google Sheets)       Power BI, Metabase)
[Azure Cost export]    ─┤
[PTAX Banco Central]   ─┘
```

- **MVP em uma semana:** Google Sheets como banco, script Python no GitHub Actions rodando às 6h, Looker Studio em cima da planilha. Serve bem até algumas centenas de usuários.
- **Versão estável:** BigQuery ou Postgres, mesmo script, Metabase ou Power BI.
- **Câmbio:** a fatura chega em dólar. Grave a PTAX de venda do dia (endpoint público do Banco Central, usado no comparativo) e converta no relatório, não na coleta. Se a empresa paga com cartão, acrescente IOF e spread como fator configurável.
- **Alertas semanais (uma query cada, enviada por e-mail ou Slack):** assento sem uso há 30 dias; usuário acima de 20% do custo do produto; custo da pessoa cresceu mais de 50% sobre a semana anterior; nova despesa de Anthropic, OpenAI ou Google em cartão corporativo fora da conta central (fonte: ERP ou Nudge Security), que é o alerta de conta pessoal.

## 6. Esqueleto de coletor

O arquivo `finops/coletor_exemplo.py` traz as quatro funções de coleta (Claude, Graph, Google, LiteLLM), a normalização para `fato_uso_ia` e a PTAX. É um esqueleto para adaptar, não um produto pronto. O `finops/modelo.sql` tem o DDL e as consultas acima.

## 7. Roteiro de quatro semanas

| Semana | Entrega |
|---|---|
| 1 | Chaves: Analytics API do Claude, app registration no Entra com `Reports.Read.All`, service account no Google com escopo de reports. Desmascarar nomes nos relatórios do Microsoft 365. Planilha com `dim_usuario` e `dim_assento` vindas do RH ou do SSO. |
| 2 | Coletor rodando diário para Claude e Copilot. Painel com custo e percentual por pessoa nesses dois. |
| 3 | Gemini Workspace via Reports API. LiteLLM na frente das APIs com uma chave por desenvolvedor e tag por projeto. |
| 4 | Câmbio PTAX, visão por departamento e centro de custo, alertas semanais, reconciliação do total mensal com as faturas. |

## 8. O que esse desenho não resolve

- **Gemini e Copilot não dão tokens por pessoa.** O custo é o assento rateado. O percentual é de atividade, não de consumo. É a melhor aproximação possível com os dados que os fornecedores expõem hoje.
- **Claude Team não tem API.** Só exportação manual mensal. Para automação completa, migre para Enterprise (mínimo 20 assentos).
- **Conta pessoal segue invisível.** O alerta vem das despesas, do SSO ou de uma ferramenta de descoberta, não do fornecedor de IA.
- **Chaves compartilhadas na API quebram a atribuição.** A regra "uma chave por pessoa, um workspace ou tag por projeto" tem que ser política, não sugestão.
- **Atrasos:** Claude um dia, Copilot até 48 horas, Gemini dois a três dias. O painel é de ontem, não de agora.

## Fontes

- Usage and Cost Analytics API (Claude): https://platform.claude.com/docs/en/manage-claude/usage-cost-analytics-api
- Analytics APIs do Claude, chaves e planos: https://platform.claude.com/docs/en/manage-claude/analytics-api
- Spend report do Claude Team e Enterprise: https://support.claude.com/en/articles/12883420-view-usage-analytics-for-team-and-enterprise-plans
- Graph API, Copilot usage user detail: https://learn.microsoft.com/en-us/graph/api/reportroot-getmicrosoft365copilotusageuserdetail?view=graph-rest-beta
- Microsoft, novas métricas de prompts e dias ativos: https://m365admin.handsontek.net/?p=22535
- Gemini reports no Admin console: https://support.google.com/a/answer/14564320
- Gemini for Workspace log events (Reports API): https://knowledge.workspace.google.com/admin/reports/gemini-for-workspace-log-events
- Admin SDK release notes, `gemini_in_workspace_apps`: https://developers.google.com/workspace/admin/release-notes
- Vertex AI, labels em chamadas: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/add-labels-to-api-calls
- Cloud Billing export para BigQuery: https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery
- Azure API Management, emit-token-metric: https://learn.microsoft.com/en-ie/azure/api-management/azure-openai-emit-token-metric-policy
- LiteLLM, spend tracking: https://docs.litellm.ai/docs/proxy/cost_tracking
- PTAX, Banco Central: https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/
