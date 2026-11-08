# Comparativo de preços em reais: ferramentas de uso e custo de IA

Conversão feita em 01/11/2026 com a PTAX de venda do Banco Central de 30/10/2026: **US$ 1 = R$ 5.4212**. Os valores em dólar são os da lista oficial em `COMPARATIVO_PRECOS.md`. Valores arredondados.

Dois avisos antes de usar os números:

- **Cobrança em cartão internacional** acrescenta IOF e o spread do banco, normalmente entre 4% e 7% sobre o valor convertido. Some isso aos preços abaixo quando a fatura vier em dólar.
- **Alguns fornecedores têm preço local em real** (Google Workspace, Microsoft 365 e, em alguns casos, OpenAI). Esses preços locais podem ser diferentes da conversão direta. Confira no fluxo de compra com conta brasileira.

## Resumo em uma tabela

| Camada | Ferramenta | Preço de entrada em reais | Como cobra | Preço publicado? |
|---|---|---|---|---|
| 1. Nativo | Claude Team | R$ 108 a R$ 136/usuário/mês (padrão); R$ 542 a R$ 678 (premium) | por assento, mín. 2, máx. 150 | Sim |
| 1. Nativo | Claude Enterprise | R$ 108/usuário/mês de assento + uso cobrado a preço de API | assento anual, mín. 20 | Sim (assento) |
| 1. Nativo | Google Workspace (Gemini incluso) | R$ 38 / R$ 76 / R$ 119/usuário/mês (anual) | por assento, máx. 300 nos Business | Sim |
| 1. Nativo | Google AI Expanded Access | sob consulta | add-on por usuário | Não |
| 1. Nativo | ChatGPT Business | R$ 108/usuário/mês (anual) ou R$ 136 (mensal); premium R$ 542 a R$ 678 | por assento, mín. 2 | Sim |
| 1. Nativo | ChatGPT Enterprise | sob consulta (mercado: R$ 244 a R$ 407/usuário/mês, mín. ~150) | por assento + créditos | Não |
| 1. Nativo | Microsoft 365 Copilot | R$ 163/usuário/mês (Enterprise); R$ 114 Business (promo R$ 98) | add-on anual sobre licença M365 | Sim |
| 2. Gateway | LiteLLM | R$ 0 (open source) | infra própria; Enterprise sob consulta | Só o grátis |
| 2. Gateway | Portkey | R$ 0 (10 mil logs/mês) ou R$ 266/mês (100 mil logs) | por volume de logs | Sim |
| 2. Gateway | Helicone | R$ 0 (10 mil req/mês); R$ 428/mês Pro; R$ 4.332/mês Team | por volume de requisições | Sim |
| 2. Observab. | Langfuse | R$ 0 (50 mil unidades); R$ 157 Core; R$ 1.079 Pro; R$ 13.548 Enterprise | por volume; self-host grátis | Sim |
| 2. Medição | OpenMeter | open source grátis; nuvem sob consulta | eventos | Não |
| 3. FinOps | Vantage | R$ 0 (até R$ 13.553/mês rastreados); R$ 163; R$ 1.084/mês | por gasto rastreado e usuários | Sim |
| 3. FinOps | Finout | sob consulta | taxa fixa por faixa de gasto | Não |
| 3. FinOps | CloudZero | sob consulta (mercado: mínimo R$ 8.132 a R$ 13.553/mês) | assinatura única | Não |
| 3. Governança SaaS | Nudge Security | R$ 4.066/mês até 150 usuários; R$ 27,11/usuário/mês de 150 a 1.500 | flat ou por caixa de e-mail, anual | Sim |
| 3. Governança SaaS | CloudEagle | sob consulta (mercado: ~R$ 10.842 a R$ 13.553/mês por módulo) | módulos | Não |
| 3. Governança SaaS | Torii | sob consulta | por funcionário | Não |
| 3. Governança SaaS | Zylo | sob consulta | 3 tiers anuais | Não |
| 3. Governança | Credal | sob consulta (mercado: mediana ~R$ 21.685/ano) | assentos + indexação + tokens | Não |

## Camada 1: planos corporativos dos fornecedores de IA

### Claude (Anthropic)

| Plano | Mensal | Anual (por mês) | Mínimo |
|---|---|---|---|
| Pro (individual) | R$ 108 | R$ 92 | 1 |
| Max (individual) | R$ 542 | não há | 1 |
| Ultra (individual) | R$ 1.084 | não há | 1 |
| Team, assento padrão | R$ 136 | R$ 108 | 2 (máx. 150) |
| Team, assento premium | R$ 678 | R$ 542 | 2 |
| Enterprise | não há | R$ 108 + consumo a preço de API | 20 |

Conta: 10 pessoas no Team padrão anual custam R$ 1.084/mês. As mesmas 10 em Pro individual custam R$ 922/mês, sem visibilidade. O Enterprise fica em R$ 2.168/mês de assento (mínimo 20) mais o consumo real.

### Google Workspace (Gemini incluso)

| Edição | Flexível (mensal) | Anual (por mês) | Anual (por ano) |
|---|---|---|---|
| Business Starter | R$ 45,54 | R$ 37,95 | R$ 455 |
| Business Standard | R$ 91,08 | R$ 75,90 | R$ 911 |
| Business Plus | R$ 143,12 | R$ 119,27 | R$ 1.431 |
| Enterprise | sob consulta | sob consulta | sob consulta |
| AI Expanded Access (add-on) | sob consulta | sob consulta | sob consulta |

O Google vende o Workspace em real no Brasil, com preço local. Confira em workspace.google.com/intl/pt-BR/pricing com conta brasileira, porque o valor pode diferir desta conversão.

### ChatGPT (OpenAI)

| Plano | Mensal | Anual (por mês) | Mínimo |
|---|---|---|---|
| Business, assento padrão | R$ 136 | R$ 108 | 2 |
| Business, assento premium | R$ 678 | R$ 542 | 2 |
| Enterprise | sob consulta | mercado: R$ 244 a R$ 407 | ~150 |

### Microsoft 365 Copilot

| Plano | Preço por usuário/mês | Observação |
|---|---|---|
| Copilot Chat | R$ 0 | Incluído em licenças M365 elegíveis; agentes por consumo |
| Microsoft 365 Copilot (Enterprise) | R$ 163 | Add-on anual sobre E3, E5 ou similar |
| Microsoft 365 Copilot Business (add-on) | R$ 114, promo R$ 98 no 1º ano | Até 300 usuários; promo até 31/12/2026 |
| Business Standard com Copilot | R$ 127,40 | Licença + Copilot |
| Business Premium com Copilot | R$ 173 | Licença + Copilot |
| Créditos de agentes | mercado: R$ 0,054 por crédito ou R$ 1.084 por 25 mil/mês | Exige assinatura Azure |

A Microsoft também tem tabela em real no Brasil. Confira o preço local com conta brasileira.

## Camada 2: gateways e observabilidade de API

| Ferramenta | Grátis | Pago por mês | Enterprise |
|---|---|---|---|
| LiteLLM | Open source completo | não há plano intermediário | anual, sob consulta |
| Portkey | 10 mil logs/mês | R$ 266 com 100 mil logs, +R$ 49 a cada 100 mil | sob consulta |
| Helicone | 10 mil requisições/mês | Pro R$ 428; Team R$ 4.332 | sob consulta |
| Langfuse | 50 mil unidades/mês ou self-host MIT | Core R$ 157; Pro R$ 1.079; Enterprise R$ 13.548; +R$ 43 por 100 mil unidades extras; Teams add-on R$ 1.626 | self-host sob consulta |
| OpenMeter | Open source | sob consulta | sob consulta |

LiteLLM self-hosted custa zero de licença. Uma VM pequena com Postgres sai entre R$ 108 e R$ 325/mês num provedor de nuvem.

## Camada 3: FinOps e governança de SaaS

| Ferramenta | Preço em reais | Base de cobrança |
|---|---|---|
| Vantage | Starter grátis (até R$ 13.553/mês rastreados, 3 usuários); Pro R$ 163/mês (até R$ 40.659, 5 usuários); Business R$ 1.084/mês (até R$ 108.424, 10 usuários); Enterprise sob consulta | gasto rastreado e usuários |
| Finout | sob consulta | taxa fixa por faixa de gasto comprometido |
| CloudZero | sob consulta; mercado: mínimo R$ 8.132 a R$ 13.553/mês ou R$ 54.212 a R$ 379.484/ano | assinatura única |
| Nudge Security | Essential R$ 4.066/mês até 150 usuários (R$ 48.791/ano); Growth R$ 27,11/usuário/mês de 150 a 1.500; Enterprise sob consulta | flat ou por caixa de e-mail, anual |
| CloudEagle | sob consulta; mercado: ~R$ 10.842/mês (governança) a R$ 13.553/mês (gestão ou compras) por módulo; Capterra lista R$ 16,26/usuário/mês, não confirmado | módulos |
| Torii | sob consulta | por funcionário |
| Zylo | sob consulta | tiers anuais |
| Credal | sob consulta; Vendr cita mediana de R$ 21.685/ano | assentos + indexação + tokens |

## Três cenários de custo em reais

Suposição: 30 funcionários, metade usando Claude e metade Gemini, mais 5 desenvolvedores chamando API.

| Cenário | Composição | Custo mensal aproximado | Custo anual aproximado | Visibilidade |
|---|---|---|---|---|
| A. Como está hoje | 15 Claude Pro (R$ 108) + 15 Google Business Standard (R$ 76) + API sem gateway | R$ 2.765 + consumo de API | R$ 33.178 + API | Nenhuma por pessoa no Claude; Gemini só adoção |
| B. Consolidar no nativo | 15 Claude Team anual (R$ 108) + 15 Google Business Standard (R$ 76) + LiteLLM self-host (~R$ 163 de infra) | R$ 2.927 + consumo de API | R$ 35.129 + API | Custo por pessoa no Claude; adoção no Gemini; custo por chave e time na API |
| C. Nativo + consolidador | Cenário B + Vantage Pro (R$ 163) ou Nudge Essential (R$ 4.066) | R$ 3.090 a R$ 6.993 + consumo de API | R$ 37.081 a R$ 83.920 + API | Tudo do B num só painel; Nudge descobre contas pessoais no cartão |

O salto de A para B custa cerca de R$ 163 por mês e resolve a maior parte das perguntas. A camada 3 só compensa com dezenas de ferramentas de IA ou chargeback formal por departamento.

## Fonte da cotação

- Banco Central do Brasil, PTAX de venda de 30/10/2026, R$ 5.4212: https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='10-25-2026'&@dataFinalCotacao='11-01-2026'&$format=json
- Preços em dólar e fontes de cada fornecedor: ver `COMPARATIVO_PRECOS.md`.
