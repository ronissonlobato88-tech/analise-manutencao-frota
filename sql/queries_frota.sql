-- ====================================================================
-- PROJETO: GESTÃO E MANUTENÇÃO DE FROTA
-- ====================================================================

-- 1. CRIAÇÃO DAS TABELAS (DDL)
CREATE TABLE IF NOT EXISTS veiculos (
    veiculo_id VARCHAR(10) PRIMARY KEY,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    ano_fabricacao INT,
    tipo_combustivel VARCHAR(30),
    status_veiculo VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS manutencoes (
    manutencao_id VARCHAR(10) PRIMARY KEY,
    veiculo_id VARCHAR(10),
    data DATE,
    tipo_manutencao VARCHAR(50),
    quilometragem INT,
    peca_substituida VARCHAR(100),
    custo_pecas DECIMAL(10, 2),
    custo_mao_obra DECIMAL(10, 2),
    custo_total DECIMAL(10, 2),
    tempo_parado_horas DECIMAL(5, 1),
    CONSTRAINT fk_veiculo FOREIGN KEY (veiculo_id) REFERENCES veiculos(veiculo_id)
);

-- ====================================================================
-- 2. CONSULTAS ANALÍTICAS DE NEGÓCIO (DQL)
-- ====================================================================

-- Pergunta 1: Custo total e horas de imobilização por Marca
SELECT 
    v.marca,
    COUNT(m.manutencao_id) AS total_intervencoes,
    SUM(m.custo_total) AS custo_total_acumulado,
    ROUND(AVG(m.custo_total), 2) AS ticket_medio_manutencao,
    ROUND(SUM(m.tempo_parado_horas), 1) AS total_horas_parado
FROM manutencoes m
INNER JOIN veiculos v ON m.veiculo_id = v.veiculo_id
GROUP BY v.marca
ORDER BY custo_total_acumulado DESC;

-- Pergunta 2: Eficiência Operacional - Distribuição Preventiva vs Corretiva
SELECT 
    tipo_manutencao,
    COUNT(*) AS volume_intervencoes,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentual_volume,
    SUM(custo_total) AS custo_total,
    ROUND(AVG(tempo_parado_horas), 1) AS media_horas_indisponivel
FROM manutencoes
GROUP BY tipo_manutencao
ORDER BY custo_total DESC;

-- Pergunta 3: Veículos Críticos (Top 5 com maior custo acumulado)
SELECT 
    v.veiculo_id,
    v.marca,
    v.modelo,
    v.ano_fabricacao,
    COUNT(m.manutencao_id) AS qtd_intervencoes,
    SUM(m.custo_total) AS gasto_total_acumulado,
    SUM(m.tempo_parado_horas) AS tempo_total_imobilizado_h
FROM manutencoes m
INNER JOIN veiculos v ON m.veiculo_id = v.veiculo_id
GROUP BY v.veiculo_id, v.marca, v.modelo, v.ano_fabricacao
ORDER BY gasto_total_acumulado DESC
LIMIT 5;

-- Pergunta 4: Peças mais substituídas e o gasto associado
SELECT 
    peca_substituida,
    COUNT(*) AS total_trocas,
    SUM(custo_pecas) AS gasto_total_pecas,
    ROUND(AVG(custo_pecas), 2) AS custo_medio_peca
FROM manutencoes
GROUP BY peca_substituida
ORDER BY total_trocas DESC
LIMIT 5;