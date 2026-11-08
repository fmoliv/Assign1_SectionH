# Documento de produto: Otimizador de Licenças e Orçamento de IA

Nome provisório. Versão 0.1, 01/11/2026. Baseado na pesquisa em `RELATORIO.md`, `COMPARATIVO_PRECOS.md` e `FINOPS_SIMPLES.md`.

## 1. Em uma frase

Um produto que junta o uso de Copilot, Claude, Gemini e ChatGPT por pessoa, define um orçamento de IA por funcionário em real, encontra licenças ociosas e contas pessoais pagas pela empresa, e executa a correção com aprovação do gestor, cobrando só sobre a economia que entregou.

## 2. O problema

- **Ninguém vê o todo.** Cada fornecedor tem um console, cada um mede de um jeito. Claude dá dólar por pessoa só no Enterprise. Gemini e Copilot dão "nível de uso", nunca custo. Nenhum mostra o concorrente.
- **Assento parado é o maior desperdício.** Copilot custa US$ 30, Claude Team US$ 20, Gemini Standard US$ 14 por pessoa por mês. Os relatórios nativos mostram "uso baixo" e param. Ninguém calcula quanto isso custa nem age.
- **Contas pessoais escapam.** Claude Pro, ChatGPT Plus e Gemini Advanced no cartão corporativo são invisíveis para o fornecedor e aparecem só na despesa, meses depois.
- **A empresa não consegue dizer "você tem R$ 400 de IA por mês".** Limite por usuário existe só dentro de cada fornecedor, e em poucos planos.
- **Finanças fecha o mês na planilha.** Tudo chega em dólar, sem IOF, sem centro de custo, sem reconciliar com a fatura.

## 3. Para quem

| Papel | Quem é | O que ganha |
|---|---|---|
| Comprador | CFO, controladoria ou líder de FinOps de empresa com 50 a 2.000 funcionários e dois ou mais fornecedores de IA | Economia mensurável em real no primeiro mês e fechamento mensal sem planilha |
| Administrador | TI ou governança de SaaS | Um console para licenças, orçamentos e contas fora da política |
| Usuário diário | Gestor de equipe | Aprovação em um clique no Slack ou Teams: rebaixar, trocar, remover ou aumentar o limite de alguém |
| Funcionário | Qualquer pessoa com licença de IA | Vê o próprio consumo e orçamento, pede aumento sem abrir chamado |

Foco inicial: Brasil e América Latina. A combinação de preço em real, IOF e integração com ERP local não existe em nenhum concorrente.

## 4. Diferenciais

| Contra | O que eles fazem | O que este produto faz a mais |
|---|---|---|
| Painéis nativos (Claude, Google Admin, Microsoft 365) | Uso dentro do próprio fornecedor, custo só no Claude Enterprise | Soma os fornecedores, orçamento único por pessoa, compara e recomenda o concorrente quando sai mais barato, age |
| CloudEagle, Torii, Zylo | SaaS management genérico; IA é mais um app; preço sob consulta, na casa de R$ 10 mil por mês | Só IA: entende assento versus consumo, token, modelo e agente; cobra sobre a economia, sem risco para o cliente |
| Vantage, Finout, CloudZero | FinOps de nuvem com conector de IA; mostra, não age; em dólar | Ação com aprovação, orçamento por pessoa, real com IOF e reconciliação de fatura |
| Nudge Security | Descobre a conta pessoal e para | Fecha o ciclo: mostra o custo da migração para a conta corporativa, convida e cancela o reembolso |

O diferencial que os fornecedores nunca vão copiar: recomendar cortar a própria licença ou trocar pelo concorrente.

## 5. O que o produto faz

**5.1 Inventário vivo de IA.** Quem tem o quê, pago por quem, custando quanto em real. Fontes: Analytics API do Claude, Graph API do Microsoft 365, Reports API do Google Workspace, gateway LiteLLM para APIs, despesas do ERP ou cartão para contas pessoais, SSO para departamento e gestor.

**5.2 Orçamento de IA por pessoa, atravessando fornecedores.** O admin define um valor em real por cargo ou por pessoa. O produto soma assento rateado e consumo medido de todos os fornecedores, projeta o fim do mês e avisa a pessoa e o gestor em 75% e 90%. Onde o fornecedor tem API de limite (Claude Enterprise, LiteLLM), aplica o corte. Onde não tem (Copilot, Gemini), avisa e registra.

**5.3 Motor de recomendações.** Regras que rodam toda noite e geram uma fila de ações com a economia calculada em real:

| Regra | Condição | Ação proposta |
|---|---|---|
| Assento ocioso | 30 dias sem atividade | Remover a licença |
| Assento subutilizado | menos de 4 dias ativos em 30, custo por dia ativo acima de R$ 25 | Rebaixar de plano ou trocar por Copilot Chat gratuito ou Gemini incluso no Workspace |
| Duplicidade | mesma pessoa com Copilot, Claude e Gemini, usando só um | Manter o mais usado, remover os outros |
| Conta pessoal | despesa de Anthropic, OpenAI ou Google no cartão fora da conta central | Migrar para a conta corporativa e cancelar o reembolso |
| Fornecedor mais caro para o perfil | custo por sessão útil 40% acima do equivalente em outro fornecedor | Trocar de fornecedor para o perfil |
| Estouro de orçamento | projeção acima do limite da pessoa | Limitar ou aumentar o orçamento com aprovação |
| Power user em plano errado | consumo acima do assento premium | Subir de plano, sai mais barato que o excedente |

**5.4 Ação com aprovação.** Cada recomendação vira um cartão no Slack ou Teams para o gestor: economia em real, risco, botão de aprovar ou recusar. Aprovado, o produto executa pela API de administração do fornecedor (remoção de licença no Microsoft 365 e no Google Workspace, remoção de membro no Claude, limite no LiteLLM) e registra a trilha de auditoria. Toda ação é reversível por 30 dias.

**5.5 Fechamento em real.** Converte pela PTAX do dia da fatura, soma IOF e spread configuráveis, reconcilia com a fatura ou nota fiscal que chegou, e exporta o rateio por centro de custo para o ERP (TOTVS, SAP, Omie, planilha). Relatório mensal: gasto real, economia realizada, orçamento versus realizado por departamento.

## 6. Como funciona

```
Fontes                          Núcleo                               Saídas
Claude Analytics API  ─┐   coleta diária ─► fato_uso_ia ─► motor de regras ─► fila de ações ─► Slack/Teams (aprovar)
Graph API (Copilot)   ─┤                    dim_usuario                                          │
Google Reports API    ─┼─►                  dim_assento                                          ▼
LiteLLM (APIs)        ─┤                    dim_cambio                                    executor via APIs admin
ERP / cartão          ─┤                                           painel web (pessoa, depto, fornecedor, orçamento)
SSO / RH              ─┘                                           export ERP, relatório mensal em real
```

O modelo de dados é o de `FINOPS_SIMPLES.md`: assento rateado por dia para Copilot, Gemini e Claude Team; custo medido para Claude Enterprise, APIs e agentes. O percentual de uso é relativo dentro de cada produto. Os números derivados que movem as regras são custo por dia ativo e dias sem uso.

Entrega como SaaS multi-tenant. Dados sensíveis: só metadados de uso, nunca prompts nem respostas. Chaves dos fornecedores em cofre, somente leitura na coleta e escopo mínimo de escrita na execução.

## 7. Uma jornada

Segunda-feira, 7h. O produto coletou domingo. Encontrou 23 licenças Copilot sem uso há 30 dias, 4 pessoas com Copilot e Claude usando só o Claude, uma despesa nova de Claude Max no cartão de um gerente e 3 desenvolvedores projetados para estourar o orçamento de API. Gera 31 cartões no Teams para 9 gestores, com economia total de R$ 6.200 por mês.

9h. Sete gestores aprovam em um clique. Duas licenças são mantidas com justificativa. O gerente do Claude Max recebe convite para o Claude Team da empresa e o reembolso é marcado para cancelar no próximo ciclo.

Dia 1 do mês seguinte. Finanças recebe o fechamento: gasto de IA em real por departamento, economia realizada, fatura de cada fornecedor reconciliada, arquivo de rateio importado no ERP. A cobrança do produto vem calculada sobre a economia confirmada.

## 8. MVP e roteiro

**MVP, quatro semanas, com três clientes de design:**

| Semana | Entrega |
|---|---|
| 1 | Conectores Claude e Microsoft 365, importação de usuários do SSO e dos assentos, painel por pessoa e departamento em real |
| 2 | Regras de assento ocioso, subutilizado e duplicidade; fila de ações; cartão no Slack e Teams |
| 3 | Executor de remoção de licença no Microsoft 365 e no Claude, com reversão; conector Google Workspace |
| 4 | Relatório mensal em real com PTAX e IOF, cálculo da economia realizada, importação de despesas por CSV para conta pessoal |

**90 dias:** orçamento por pessoa com projeção e alertas; LiteLLM para APIs; recomendação de troca de fornecedor por perfil; export para ERP; portal do funcionário.

**180 dias:** agentes como centro de custo (Copilot Studio, Managed Agents); ChatGPT Enterprise via Compliance API; benchmark anônimo entre clientes ("empresas do seu porte gastam X por pessoa").

## 9. Modelo de cobrança

**Principal: percentual da economia realizada.** 25% da economia confirmada nos primeiros 12 meses de cada ação, medida contra a fatura do fornecedor. Mínimo mensal de R$ 1.500 para cobrir o custo de servir. Sem economia além do mínimo, o cliente paga só o mínimo.

Por que assim: o cliente não tem risco, a venda vira uma conta simples, e o incentivo do produto é o mesmo do CFO. O ponto fraco é a receita cair quando a empresa já está otimizada; por isso o mínimo e, a partir do segundo ano, a migração para assinatura.

**Alternativa para contas grandes:** R$ 12 por funcionário monitorado por mês, sem percentual.

**Exemplo com 300 funcionários:**

| Item | Valor |
|---|---|
| Licenças de IA hoje | 150 Copilot (US$ 30) + 300 Gemini Standard (US$ 14) + 60 Claude Team (US$ 20) = US$ 9.900/mês |
| Ociosidade típica encontrada | 25%, US$ 2.475/mês, cerca de R$ 13.400 |
| Cobrança do produto (25%) | cerca de R$ 3.350/mês |
| Economia líquida do cliente | cerca de R$ 10.000/mês, R$ 120 mil/ano |

## 10. Métricas de sucesso

- Economia realizada por cliente nos primeiros 90 dias (meta: 15% do gasto com licenças de IA).
- Percentual de recomendações aprovadas (meta: acima de 60%).
- Tempo de fechamento mensal de IA em Finanças (meta: de dias para uma hora).
- Contas pessoais migradas para corporativas por mês.
- Retenção líquida de receita no segundo ano.

## 11. Riscos e como tratar

| Risco | Mitigação |
|---|---|
| Fornecedores melhoram os painéis e adicionam limites | Concentrar no que eles não fazem: multi-fornecedor, comparação, ação, real. A Anthropic entregou limites e alertas em quatro meses; a janela é curta |
| CloudEagle ou Torii lançam módulo de IA forte | Vencer em profundidade (assento versus consumo, agente, token) e em preço por resultado |
| APIs de admin mudam ou são beta (Graph Copilot ainda é beta) | Camada de conectores isolada, testes diários contra cada fornecedor, degradação para modo "só recomendar" |
| Gestor não aprova por medo de tirar ferramenta de alguém | Reversão em 30 dias, licença volta em um clique, mensagem automática ao funcionário |
| Privacidade: monitorar uso individual | Só metadados, nunca conteúdo; agregação mínima configurável; conformidade com LGPD, com base legal de legítimo interesse documentada |
| Dependência do cliente ter Claude Enterprise para custo por pessoa | Para Team, importar o CSV mensal; para contas Pro, tratar como conta pessoal a migrar |

## 12. Perguntas em aberto

- A cobrança por economia se sustenta depois que o cliente estabiliza, ou a assinatura deve entrar já no mês 7?
- Vale abrir com Microsoft 365 e Claude só, ou o Google Workspace é obrigatório no MVP por ser o mais comum no Brasil?
- Integração com ERP é exportação de arquivo no MVP ou conector nativo com TOTVS desde o início?
- Quem assina a execução de remoção de licença: o gestor direto ou TI, com o gestor só recomendando?

## Fontes dos dados citados

- Preços e planos: `COMPARATIVO_PRECOS.md` e `COMPARATIVO_PRECOS_BRL.md`
- APIs e limites de cada fornecedor: `FINOPS_SIMPLES.md`
- Ferramentas concorrentes e prints: `RELATORIO.md`
- Câmbio: PTAX de venda de 30/10/2026, R$ 5,4212
