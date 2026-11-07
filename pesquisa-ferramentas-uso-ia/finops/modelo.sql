-- Modelo de dados do FinOps simples de IA (Postgres; ajuste tipos para BigQuery)

CREATE TABLE IF NOT EXISTS fato_uso_ia (
  data            DATE NOT NULL,
  email           TEXT NOT NULL,
  fornecedor      TEXT NOT NULL,          -- anthropic | google | microsoft
  produto         TEXT NOT NULL,          -- claude_chat | claude_code | cowork | claude_api | gemini_workspace | gemini_api | copilot_m365 | copilot_agentes | azure_openai
  canal           TEXT NOT NULL,          -- chat | api
  atividade       NUMERIC NOT NULL DEFAULT 0,
  unidade         TEXT NOT NULL,          -- tokens | eventos | prompts | dia_ativo
  custo_usd       NUMERIC(12,4) NOT NULL DEFAULT 0,
  metodo_custo    TEXT NOT NULL,          -- medido | assento_rateado
  origem          TEXT NOT NULL,          -- claude_analytics_api | graph_api | google_reports_api | litellm | azure_cost_export | csv_manual
  PRIMARY KEY (data, email, produto, canal, origem)
);

CREATE TABLE IF NOT EXISTS dim_usuario (
  email TEXT PRIMARY KEY, nome TEXT, departamento TEXT, centro_custo TEXT, gestor TEXT, ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS dim_cambio (
  data DATE PRIMARY KEY, usd_brl NUMERIC(10,4) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_assento (
  email TEXT NOT NULL, produto TEXT NOT NULL, preco_usd_mes NUMERIC(10,2) NOT NULL,
  inicio DATE NOT NULL, fim DATE,
  PRIMARY KEY (email, produto, inicio)
);

-- Rateio diário dos assentos ativos (rodar uma vez por dia para a data de ontem)
INSERT INTO fato_uso_ia (data, email, fornecedor, produto, canal, atividade, unidade, custo_usd, metodo_custo, origem)
SELECT (CURRENT_DATE - 1), a.email,
       CASE WHEN a.produto LIKE 'copilot%' THEN 'microsoft' WHEN a.produto LIKE 'gemini%' THEN 'google' ELSE 'anthropic' END,
       a.produto, 'chat', 0, 'dia_ativo',
       a.preco_usd_mes / EXTRACT(DAY FROM (DATE_TRUNC('month', CURRENT_DATE - 1) + INTERVAL '1 month - 1 day')),
       'assento_rateado', 'rateio_assento'
FROM dim_assento a
WHERE a.inicio <= CURRENT_DATE - 1 AND (a.fim IS NULL OR a.fim >= CURRENT_DATE - 1)
ON CONFLICT DO NOTHING;

-- Percentual de uso e de custo por pessoa e produto no mês corrente
WITH base AS (
  SELECT f.email, f.produto, f.canal,
         SUM(f.atividade) AS atividade,
         SUM(f.custo_usd) AS custo_usd,
         SUM(f.custo_usd * c.usd_brl) AS custo_brl
  FROM fato_uso_ia f
  JOIN dim_cambio c ON c.data = f.data
  WHERE f.data >= DATE_TRUNC('month', CURRENT_DATE)
  GROUP BY 1,2,3
)
SELECT b.email, u.departamento, b.produto, b.canal, b.atividade,
       ROUND(100.0 * b.atividade / NULLIF(SUM(b.atividade) OVER (PARTITION BY b.produto),0), 1) AS pct_uso_no_produto,
       ROUND(b.custo_usd, 2) AS custo_usd,
       ROUND(b.custo_brl, 2) AS custo_brl,
       ROUND(100.0 * b.custo_usd / NULLIF(SUM(b.custo_usd) OVER (),0), 1) AS pct_custo_total
FROM base b LEFT JOIN dim_usuario u ON u.email = b.email
ORDER BY custo_usd DESC;

-- Custo por departamento no mês
SELECT u.departamento, f.produto,
       ROUND(SUM(f.custo_usd),2) AS custo_usd,
       ROUND(SUM(f.custo_usd * c.usd_brl),2) AS custo_brl,
       COUNT(DISTINCT f.email) AS pessoas
FROM fato_uso_ia f JOIN dim_cambio c ON c.data=f.data LEFT JOIN dim_usuario u ON u.email=f.email
WHERE f.data >= DATE_TRUNC('month', CURRENT_DATE)
GROUP BY 1,2 ORDER BY custo_usd DESC;

-- Assentos ociosos e custo por dia ativo (últimos 30 dias)
SELECT a.email, a.produto, a.preco_usd_mes,
       COALESCE(SUM(CASE WHEN f.unidade='dia_ativo' AND f.origem<>'rateio_assento' THEN f.atividade END),0) AS dias_ativos_30d,
       ROUND(a.preco_usd_mes / NULLIF(SUM(CASE WHEN f.unidade='dia_ativo' AND f.origem<>'rateio_assento' THEN f.atividade END),0), 2) AS usd_por_dia_ativo
FROM dim_assento a
LEFT JOIN fato_uso_ia f ON f.email=a.email AND f.produto=a.produto AND f.data >= CURRENT_DATE - 30
WHERE a.fim IS NULL
GROUP BY 1,2,3
ORDER BY dias_ativos_30d ASC, a.preco_usd_mes DESC;

-- Alerta: pessoa com mais de 20% do custo de um produto no mês
WITH t AS (
  SELECT email, produto, SUM(custo_usd) c FROM fato_uso_ia
  WHERE data >= DATE_TRUNC('month', CURRENT_DATE) AND metodo_custo='medido' GROUP BY 1,2)
SELECT email, produto, ROUND(c,2) custo_usd, ROUND(100*c/SUM(c) OVER (PARTITION BY produto),1) pct
FROM t WHERE c / SUM(c) OVER (PARTITION BY produto) > 0.20;
