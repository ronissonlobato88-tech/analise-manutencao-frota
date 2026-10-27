import random
from datetime import date, timedelta
import pandas as pd

# 1. Configuracoes
random.seed(42)

DATA_INICIAL = date(2023, 1, 1)
DATA_FINAL = date(2026, 10, 26)

QUANTIDADE_VEICULOS = 50
QUANTIDADE_MANUTENCOES = 500

# 2. Cadastro de Modelos
modelos = [
    ("Honda", "HR-V"),
    ("Honda", "Prelude"),
    ("Volvo", "EX30"),
    ("Volvo", "XC60"),
    ("Audi", "Q5"),
    ("Audi", "Q5 Sportback"),
    ("BMW", "iX3"),
    ("Hyundai", "Creta"),
    ("Audi", "Q3"),
    ("BMW", "X1"),
    ("BMW", "X2"),
    ("BMW", "320i"),
    ("BMW", "X6"),
    ("BMW", "530 M Sport"),
    ("Renault", "Kardian"),
    ("Honda", "Civic G9"),
    ("Honda", "Civic G10"),
    ("Honda", "Civic G11"),
    ("BYD", "Seal"),
    ("Volkswagen", "Nivus Comfort"),
    ("Volkswagen", "Nivus Highline"),
    ("Mercedes-Benz", "C180 Avantgarde"),
]

veiculos = []
for i in range(1, QUANTIDADE_VEICULOS + 1):
    marca, modelo = random.choice(modelos)
    ano = random.randint(2018, 2026)
    idade = max(0, 2026 - ano)
    km_base = (idade * random.randint(8000, 18000)) + random.randint(500, 12000)

    veiculos.append({
        "veiculo_id": f"V{i:03d}",
        "marca": marca,
        "modelo": modelo,
        "ano": ano,
        "quilometragem_inicial": km_base,
    })

df_veiculos = pd.DataFrame(veiculos)

# 3. Tabela de Pecas e Custos
pecas_por_tipo = {
    "Preventiva": [
        ("Oleo do motor", 180, 450),
        ("Filtro de oleo", 35, 100),
        ("Filtro de ar", 50, 180),
        ("Pastilhas de freio", 180, 650),
    ],
    "Corretiva": [
        ("Bomba d'agua", 250, 1100),
        ("Alternador", 450, 1800),
        ("Sensor automotivo", 120, 750),
        ("Radiador", 400, 1600),
        ("Bateria", 350, 1200),
    ],
    "Pneus e suspensao": [
        ("Pneu", 400, 1600),
        ("Amortecedor", 300, 1100),
        ("Bieleta", 80, 300),
        ("Bucha de suspensao", 70, 350),
    ],
}

# 4. Geracao das Manutencoes
manutencoes = []
dias_no_periodo = (DATA_FINAL - DATA_INICIAL).days

for i in range(1, QUANTIDADE_MANUTENCOES + 1):
    veiculo = random.choice(veiculos)
    tipo = random.choices(
        ["Preventiva", "Corretiva", "Pneus e suspensao"], weights=[50, 30, 20], k=1
    )[0]
    peca, custo_min, custo_max = random.choice(pecas_por_tipo[tipo])

    custo_pecas = round(random.uniform(custo_min, custo_max), 2)
    horas = round(random.uniform(0.5, 8), 1)
    valor_hora = random.uniform(90, 180)
    custo_mao_obra = round(horas * valor_hora, 2)

    if tipo == "Preventiva":
        tempo_parado = round(random.uniform(1, 4), 1)
    elif tipo == "Corretiva":
        tempo_parado = round(random.uniform(3, 24), 1)
    else:
        tempo_parado = round(random.uniform(2, 10), 1)

    custo_total = round(custo_pecas + custo_mao_obra, 2)
    data_manutencao = DATA_INICIAL + timedelta(
        days=random.randint(0, dias_no_periodo)
    )
    km_atual = veiculo["quilometragem_inicial"] + random.randint(0, 60000)

    manutencoes.append({
        "manutencao_id": f"M{i:04d}",
        "veiculo_id": veiculo["veiculo_id"],
        "data": data_manutencao.isoformat(),
        "quilometragem": km_atual,
        "tipo_manutencao": tipo,
        "peca_substituida": peca,
        "custo_pecas": custo_pecas,
        "horas_mao_de_obra": horas,
        "custo_mao_de_obra": custo_mao_obra,
        "tempo_parado_horas": tempo_parado,
        "custo_total": custo_total,
    })

df_manutencoes = pd.DataFrame(manutencoes)

# 5. Exportacao dos CSVs
df_veiculos.to_csv("veiculos.csv", index=False, encoding="utf-8-sig")
df_manutencoes.to_csv("manutencoes.csv", index=False, encoding="utf-8-sig")

# 6. Validacao no Terminal
print("\n=== BASE GERADA COM SUCESSO! ===")
print(f"Total de veiculos cadastrados: {len(df_veiculos)}")
print(f"Total de manutencoes registradas: {len(df_manutencoes)}")
print(f"Custo total acumulado da frota: R$ {df_manutencoes['custo_total'].sum():,.2f}")
print("\nPrimeiros registros de manutencao:")
print(
    df_manutencoes[[
        "manutencao_id",
        "veiculo_id",
        "peca_substituida",
        "custo_total",
    ]].head()
)