from pathlib import Path
import pandas as pd

# Caminho dinamico que localiza a pasta 'dados' a partir da posicao deste script
DIRETORIO_ATUAL = Path(__file__).resolve().parent
PASTA_DADOS = DIRETORIO_ATUAL.parent / "dados"

# 1. Carregar as bases
df_veiculos = pd.read_csv(PASTA_DADOS / "veiculos.csv")
df_manutencoes = pd.read_csv(PASTA_DADOS / "manutencoes.csv")

# Converter a coluna de data
df_manutencoes["data"] = pd.to_datetime(df_manutencoes["data"])

# 2. Unir as duas tabelas pela chave 'veiculo_id'
df_completo = pd.merge(df_manutencoes, df_veiculos, on="veiculo_id", how="left")

print("=" * 60)
print("       RELATÓRIO GERENCIAL - MANUTENÇÃO DE FROTA")
print("=" * 60)

# Indicadores Gerais
custo_total = df_completo["custo_total"].sum()
tempo_parado_total = df_completo["tempo_parado_horas"].sum()
print(f"Custo Financeiro Total:    R$ {custo_total:,.2f}")
print(f"Tempo Total de Parada:     {tempo_parado_total:,.1f} horas")
print(f"Total de Intervenções:     {len(df_completo)}")
print("-" * 60)

# Top 5 pecas com maior custo acumulado
print("\n--- TOP 5 PEÇAS COM MAIOR CUSTO ---")
top_pecas = (
    df_completo.groupby("peca_substituida")["custo_total"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)
print(top_pecas.map("R$ {:,.2f}".format))

# Custo e tempo parado por Tipo de Manutencao
print("\n--- RESUMO POR TIPO DE MANUTENÇÃO ---")
resumo_tipo = df_completo.groupby("tipo_manutencao").agg(
    qtd=("manutencao_id", "count"),
    custo_total=("custo_total", "sum"),
    media_parado_h=("tempo_parado_horas", "mean"),
)
print(resumo_tipo)

print("=" * 60)