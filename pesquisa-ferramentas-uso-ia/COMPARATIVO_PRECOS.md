# Comparativo de preços: ferramentas de uso e custo de IA

Pesquisa feita em 01/11/2026. Valores em dólar, lista oficial, sem impostos. Onde o fornecedor não publica preço, está marcado "sob consulta" e, quando há fonte de mercado, uma faixa indicativa. Cotação em real varia por região e contrato.

## Resumo em uma tabela

| Camada | Ferramenta | Preço de entrada | Como cobra | Preço publicado? | Mostra custo por pessoa? |
|---|---|---|---|---|---|
| 1. Nativo | Claude Team | US$ 20 a 25/usuário/mês (padrão), US$ 100 a 125 (premium) | por assento, mín. 2, máx. 150 | Sim | Sim (CSV com tokens e US$) |
| 1. Nativo | Claude Enterprise | US$ 20/usuário/mês + uso cobrado a preço de API | assento anual, mín. 20 | Sim (assento), uso varia | Sim (painel, CSV e API) |
| 1. Nativo | Google Workspace (Gemini incluso) | US$ 7 / 14 / 22/usuário/mês (anual) | por assento, máx. 300 nos planos Business | Sim | Não (só nível de uso) |
| 1. Nativo | Google AI Expanded Access | sob consulta | add-on por usuário | Não | Não |
| 1. Nativo | ChatGPT Business | US$ 20/usuário/mês (anual) ou 25 (mensal); premium US$ 100 a 125 | por assento, mín. 2 | Sim | Não (mensagens, sem US$) |
| 1. Nativo | ChatGPT Enterprise | sob consulta (mercado: US$ 45 a 75/usuário/mês, mín. ~150) | por assento + créditos | Não | Não (mensagens, sem US$) |
| 1. Nativo | Microsoft 365 Copilot | US$ 30/usuário/mês (Enterprise), US$ 21 (Business, promo US$ 18) | add-on anual sobre licença M365 | Sim | Parcial (créditos de agentes) |
| 2. Gateway | LiteLLM | US$ 0 (open source) | infra própria; Enterprise anual sob consulta | Só o grátis | Sim |
| 2. Gateway | Portkey | US$ 0 (10 mil logs/mês) ou US$ 49/mês (100 mil logs) | por volume de logs; Enterprise sob consulta | Sim | Sim |
| 2. Gateway | Helicone | US$ 0 (10 mil req/mês), US$ 79/mês Pro, US$ 799/mês Team | por volume de requisições | Sim | Sim |
| 2. Observab. | Langfuse | US$ 0 (50 mil unidades), US$ 29 Core, US$ 199 Pro, US$ 2.499 Enterprise | por volume de unidades; self-host grátis (MIT) | Sim | Sim |
| 2. Medição | OpenMeter | open source grátis; nuvem sob consulta | eventos | Não | Sim |
| 3. FinOps | Vantage | US$ 0 (até US$ 2.500 de gasto rastreado), US$ 30, US$ 200/mês | por gasto rastreado e usuários | Sim | Sim (lê a API do Claude Enterprise) |
| 3. FinOps | Finout | sob consulta | taxa fixa por faixa de gasto comprometido | Não | Sim |
| 3. FinOps | CloudZero | sob consulta (mercado: US$ 1.500 a 2.500/mês mínimo) | assinatura única por escala do ambiente | Não | Sim |
| 3. Governança SaaS | Nudge Security | US$ 750/mês até 150 usuários; US$ 5/usuário/mês de 150 a 1.500 | flat ou por caixa de e-mail, anual | Sim | Não (descobre contas e gasto) |
| 3. Governança SaaS | CloudEagle | sob consulta (mercado: ~US$ 2.000 a 2.500/mês por módulo) | módulos | Não | Sim (tokens e US$ por usuário) |
| 3. Governança SaaS | Torii | sob consulta | por funcionário, 3 ofertas (IGA, SMP, AI Management) | Não | Sim (tokens por departamento) |
| 3. Governança SaaS | Zylo | sob consulta | 3 tiers anuais (Core, Premium, Enterprise) | Não | Parcial |
| 3. Governança | Credal | sob consulta (mercado: mediana ~US$ 4.000/ano em amostra pequena) | assentos de builder e usuário + indexação + tokens | Não | Sim |

## Camada 1: planos corporativos dos fornecedores de IA

### Claude (Anthropic), página oficial de preços

| Plano | Mensal | Anual | Mínimo | Observação |
|---|---|---|---|---|
| Pro (individual) | US$ 20 | US$ 17 | 1 | Sem painel para a empresa |
| Max (individual) | US$ 100 | não há | 1 | Sem painel para a empresa |
| Ultra (individual) | US$ 200 | não há | 1 | Sem painel para a empresa |
| Team, assento padrão | US$ 25 | US$ 20 | 2 (máx. 150) | Painel de uso e spend report em CSV |
| Team, assento premium | US$ 125 | US$ 100 | 2 | 5x mais uso que o padrão |
| Enterprise | não há | US$ 20 | 20 | Uso cobrado à parte a preço de API; limites de gasto por usuário e grupo, SCIM, Analytics API |

Conta: 10 pessoas no Team padrão anual custam US$ 200/mês. As mesmas 10 pessoas em Pro individual custam US$ 170/mês, mas sem nenhuma visibilidade. O Enterprise fica em US$ 400/mês de assento (mínimo 20) mais o consumo real.

### Google Workspace (Gemini incluso), página oficial de billing

| Edição | Flexível (mensal) | Anual | Gemini |
|---|---|---|---|
| Business Starter | US$ 8,40 | US$ 7 | Limitado (Gmail e app Gemini) |
| Business Standard | US$ 16,80 | US$ 14 | Completo em Docs, Sheets, Slides, Meet |
| Business Plus | US$ 26,40 | US$ 22 | Completo |
| Enterprise | sob consulta | sob consulta | Completo |
| AI Expanded Access (add-on) | sob consulta | sob consulta | Limites maiores; só Standard ou superior |

O add-on Gemini separado deixou de existir em 2025. Não há custo por pessoa a controlar: o relatório de admin serve para cortar licença de quem não usa.

### ChatGPT (OpenAI), central de ajuda oficial

| Plano | Mensal | Anual | Mínimo |
|---|---|---|---|
| Business, assento padrão | US$ 25 | US$ 20 | 2 |
| Business, assento premium | US$ 125 | US$ 100 | 2 |
| Enterprise | sob consulta | sob consulta | mercado cita ~150 assentos |

Preço do Business caiu US$ 5 em abril de 2026. Estimativas de mercado para o Enterprise ficam entre US$ 45 e 75 por usuário/mês, não confirmadas pela OpenAI.

### Microsoft 365 Copilot, página oficial de preços

| Plano | Preço | Observação |
|---|---|---|
| Copilot Chat | US$ 0 | Incluído em licenças M365 elegíveis; agentes cobrados por consumo |
| Microsoft 365 Copilot (Enterprise) | US$ 30/usuário/mês, anual | Add-on; exige licença E3, E5 ou similar |
| Microsoft 365 Copilot Business (add-on) | US$ 21/usuário/mês, promo US$ 18 no 1º ano | Até 300 usuários; promo até 31/12/2026 |
| Business Standard com Copilot | US$ 23,50/usuário/mês | Pacote licença + Copilot |
| Business Premium com Copilot | US$ 32/usuário/mês | Pacote licença + Copilot |
| Créditos de agentes | mercado: US$ 0,01 por crédito ou US$ 200 por 25 mil/mês | Exige assinatura Azure |

## Camada 2: gateways e observabilidade de API

| Ferramenta | Grátis | Pago | Enterprise | Self-host |
|---|---|---|---|---|
| LiteLLM | Open source completo: chaves virtuais, usuários, times, spend tracking, budgets, Prometheus | não há plano intermediário | Anual, sob consulta, por capacidade de requisições, nunca por token; adiciona SSO, SCIM, audit log, SLA | Sim, grátis |
| Portkey | 10 mil logs/mês | US$ 49/mês com 100 mil logs, +US$ 9 a cada 100 mil | Sob consulta, 10 milhões+ logs, budgets granulares, SSO | Gateway open source |
| Helicone | 10 mil requisições/mês, 1 assento, 7 dias de retenção | Pro US$ 79/mês (assentos ilimitados, 1 mês de retenção); Team US$ 799/mês (SOC 2, HIPAA, 3 meses) | Sob consulta, SAML, on-prem | Sim, open source |
| Langfuse | 50 mil unidades/mês | Core US$ 29, Pro US$ 199, Enterprise US$ 2.499/mês, todos com 100 mil unidades e US$ 8 por 100 mil extras; Teams add-on US$ 300 | Self-host Enterprise sob consulta | Sim, MIT, grátis |
| OpenMeter | Open source | nuvem sob consulta | sob consulta | Sim |

Para uma empresa que só quer custo por chave, time e projeto, o LiteLLM self-hosted custa zero de licença. O custo real é a VM e o Postgres, na casa de dezenas de dólares por mês.

## Camada 3: FinOps e governança de SaaS

| Ferramenta | Preço | Base de cobrança | Fonte |
|---|---|---|---|
| Vantage | Starter grátis (até US$ 2.500/mês rastreados, 3 usuários); Pro US$ 30/mês (US$ 7.500, 5 usuários); Business US$ 200/mês (US$ 20 mil, 10 usuários); Enterprise sob consulta | gasto rastreado e número de usuários | página oficial |
| Finout | sob consulta | taxa fixa por faixa de gasto comprometido em nuvem e IA, fixa durante o contrato | página oficial |
| CloudZero | sob consulta; mercado cita mínimo de US$ 1.500 a 2.500/mês ou US$ 10 mil a 70 mil/ano | assinatura única, escala do ambiente | página oficial + terceiros |
| Nudge Security | Essential US$ 750/mês até 150 usuários; Growth US$ 5/usuário/mês de 150 a 1.500; Enterprise sob consulta | flat ou por caixa de e-mail, anual | página oficial |
| CloudEagle | sob consulta; mercado cita ~US$ 2.000/mês (governança) a 2.500/mês (gestão ou compras) por módulo; Capterra lista US$ 3/usuário/mês, não confirmado | módulos (AI Governance inclui tokens e budgets) | página oficial + terceiros |
| Torii | sob consulta | por funcionário; AI Management é oferta separada | página oficial |
| Zylo | sob consulta | tiers Core, Premium, Enterprise, contrato anual | página oficial |
| Credal | sob consulta; Vendr cita mediana de US$ 4 mil/ano em 3 compras | assentos de builder, assentos de usuário, indexação de dados e tokens | página oficial + terceiros |

## Três cenários de custo para comparar

Suposição: 30 funcionários, metade usando Claude e metade Gemini, mais um time de 5 desenvolvedores chamando API.

| Cenário | Composição | Custo mensal aproximado de licença e ferramenta | Visibilidade |
|---|---|---|---|
| A. Como está hoje | 15 Claude Pro (US$ 20) + 15 Google Business Standard (US$ 14) + API sem gateway | US$ 510 + consumo de API | Nenhuma por pessoa no Claude; Gemini só adoção |
| B. Consolidar no nativo | 15 Claude Team anual (US$ 20) + 15 Google Business Standard (US$ 14) + LiteLLM self-host (US$ 0 + ~US$ 30 de infra) | US$ 540 + consumo de API | Custo por pessoa no Claude; adoção no Gemini; custo por chave e time na API |
| C. Nativo + consolidador | Cenário B + Vantage Pro (US$ 30) ou Nudge Essential (US$ 750) | US$ 570 a 1.290 + consumo de API | Tudo do B num só painel; Nudge ainda descobre contas pessoais pagas no cartão |

O salto de A para B custa US$ 30 por mês e resolve a maior parte das perguntas. A camada 3 só compensa quando há dezenas de ferramentas de IA ou necessidade de chargeback formal por departamento.

## Observações

- Preços de mercado para ChatGPT Enterprise, CloudZero, CloudEagle e Credal vêm de blogs e agregadores, não dos fornecedores. Use como ordem de grandeza.
- Não consegui abrir a página de preços da OpenAI por bloqueio automatizado; os valores vêm da central de ajuda oficial da OpenAI.
- O Google não exibe o preço do AI Expanded Access fora do fluxo de compra do admin.
- O Claude Enterprise cobra o consumo à parte a preço de API, então o custo total depende do uso. O spend report mostra esse valor por pessoa.

## Fontes

- Claude: https://claude.com/pricing
- Google Workspace, atualização de preços e IA: https://support.google.com/a/answer/15400543
- Google, add-on AI Expanded Access: https://knowledge.workspace.google.com/admin/getting-started/editions/compare-google-ai-expansion-add-ons
- OpenAI, billing e assentos do ChatGPT Business: https://help.openai.com/en/articles/8792536-managing-billing-and-seats-in-chatgpt-business-4
- OpenAI, FAQ ChatGPT Business: https://help-lb.openai.com/en/articles/8542115-chatgpt-business-general-faq
- Microsoft 365 Copilot: https://www.microsoft.com/en-us/microsoft-365/copilot/pricing
- Microsoft 365 Copilot Enterprise: https://www.microsoft.com/microsoft-365/copilot/pricing/enterprise
- LiteLLM: https://www.litellm.ai/pricing
- Portkey: https://portkey.ai/pricing
- Helicone: https://www.helicone.ai/pricing
- Langfuse cloud: https://langfuse.com/pricing
- Langfuse self-host: https://langfuse.com/pricing-self-host
- OpenMeter: https://openmeter.io/pricing
- Vantage: https://www.vantage.sh/pricing
- Finout: https://www.finout.io/pricing
- CloudZero: https://www.cloudzero.com/pricing/
- Nudge Security: https://www.nudgesecurity.com/pricing
- CloudEagle: https://www.cloudeagle.ai/pricing
- Torii: https://www.toriihq.com/pricing
- Zylo: https://zylo.com/pricing/
- Credal: https://www.credal.ai/pricing
- Estimativas de mercado: https://coworker.ai/blog/enterprise-ai-pricing-comparison-2026 , https://www.spotsaas.com/blog/chatgpt-enterprise-pricing , https://www.pointfive.co/guides/best-finops-tools , https://www.rfp.wiki/it-security/saas-management-platforms/zylo/cloudeagle , https://www.vendr.com/marketplace/credal , https://www.buildmvpfast.com/api-costs/llm-ops
