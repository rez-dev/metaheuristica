import numpy as np
# DATASETS OPTIMUM VALUES
optimos = {
    'wi29': 27603,
    'dj38': 6656,
    'uy734': 79114,
    'zi929': 95345,
    'lu980': 11340,
    'qa194': 9352
}

# DATASETS
datasets = {
    'wi29': [27750.0, 27603.0, 27603.0, 27603.0, 28779.0, 27750.0, 27750.0, 27750.0, 30176.0, 30376.0, 28292.0, 27603.0, 29942.0, 27750.0, 27603.0, 27603.0, 30408.0, 27603.0, 27603.0, 27750.0, 27750.0],
    'dj38': [6691.0, 6808.0, 6808.0, 6783.0, 6908.0, 6808.0, 6808.0, 6783.0, 6808.0, 6766.0, 6808.0, 6808.0, 6921.0, 6808.0, 6808.0, 6884.0, 6808.0, 6808.0, 7075.0, 6656.0, 6808.0],
    'uy734': [83091.0, 82185.0, 83053.0, 82531.0, 82199.0, 82947.0, 82609.0, 84360.0, 86999.0, 82785.0, 85218.0, 83576.0, 83325.0, 84424.0, 82616.0, 82797.0, 86010.0, 82158.0, 84034.0, 83046.0, 85676.0],
    'zi929': [101212.0, 100391.0, 106693.0, 101809.0, 99440.0, 105788.0, 102694.0, 100554.0, 102925.0, 100686.0, 103373.0, 102616.0, 104565.0, 101563.0, 100052.0, 101341.0, 100336.0, 103557.0, 103120.0, 99005.0, 103734.0],
    'lu980': [11870.0, 12203.0, 12859.0, 12443.0, 12162.0, 12425.0, 12257.0, 12679.0, 11938.0, 12217.0, 12769.0, 12102.0, 12287.0, 12525.0, 12687.0, 11951.0, 12550.0, 12450.0, 12348.0, 12085.0, 12202.0],
    'qa194': [9389.0, 9403.0, 9361.0, 9352.0, 9417.0, 9410.0, 9353.0, 9442.0, 9447.0, 9522.0, 9452.0, 9354.0, 9551.0, 9360.0, 9414.0, 9432.0, 9410.0, 9415.0, 9527.0, 9494.0, 9360.0]
}

# Calcular el gap para cada conjunto de datos
gaps = {}

for nombre, datos in datasets.items():
    valor_optimo = optimos.get(nombre, None)
    if valor_optimo is not None:
        gap_max = ((max(datos) - valor_optimo)/valor_optimo)*100
        gap_min = ((min(datos) - valor_optimo)/valor_optimo)*100
        mediana = np.median(np.sort(datos))
        print(mediana)
        gap_mediana = ((mediana - valor_optimo)/valor_optimo)*100
        gaps[nombre] = {'Gap Mejor Solución': gap_min,'Gap Peor Solución': gap_max, 'Gap Mediana': gap_mediana}

# Imprimir los resultados
for nombre, resultado in gaps.items():
    print(f"Conjunto de Datos: {nombre}")
    print(f"Gap Mínimo: {resultado['Gap Mejor Solución']}")
    print(f"Gap Mediana: {resultado['Gap Mediana']}")
    print(f"Gap Máximo: {resultado['Gap Peor Solución']}")
    print()
