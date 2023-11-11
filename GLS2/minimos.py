### ./datasets/wi29.tsp ###
wi29 = [27750.0, 27603.0, 27603.0, 27603.0, 28779.0, 27750.0, 27750.0, 27750.0, 30176.0, 30376.0, 28292.0, 27603.0, 29942.0, 27750.0, 27603.0, 27603.0, 30408.0, 27603.0, 27603.0, 27750.0, 27750.0]

### ./datasets/dj38.tsp ###
dj38 = [6691.0, 6808.0, 6808.0, 6783.0, 6908.0, 6808.0, 6808.0, 6783.0, 6808.0, 6766.0, 6808.0, 6808.0, 6921.0, 6808.0, 6808.0, 6884.0, 6808.0, 6808.0, 7075.0, 6656.0, 6808.0]

### ./datasets/uy734.tsp ###
uy734 = [83091.0, 82185.0, 83053.0, 82531.0, 82199.0, 82947.0, 82609.0, 84360.0, 86999.0, 82785.0, 85218.0, 83576.0, 83325.0, 84424.0, 82616.0, 82797.0, 86010.0, 82158.0, 84034.0, 83046.0, 85676.0]

### ./datasets/zi929.tsp ### 
zi929 = [101212.0, 100391.0, 106693.0, 101809.0, 99440.0, 105788.0, 102694.0, 100554.0, 102925.0, 100686.0, 103373.0, 102616.0, 104565.0, 101563.0, 100052.0, 101341.0, 100336.0, 103557.0, 103120.0, 99005.0, 103734.0]

### ./datasets/lu980.tsp ###
lu980 = [11870.0, 12203.0, 12859.0, 12443.0, 12162.0, 12425.0, 12257.0, 12679.0, 11938.0, 12217.0, 12769.0, 12102.0, 12287.0, 12525.0, 12687.0, 11951.0, 12550.0, 12450.0, 12348.0, 12085.0, 12202.0]

def indice_del_minimo(lista):
    # Usamos la función index para obtener el índice del mínimo
    indice_minimo = lista.index(min(lista))
    return indice_minimo
def indice_del_maximo(lista):
    # Usamos la función index para obtener el índice del máximo
    indice_maximo = lista.index(max(lista))
    return indice_maximo

# Imprimir los índices de los mínimos
print("Índice del mínimo en arreglo_wi29:", indice_del_minimo(wi29))
print("Índice del maximo en arreglo_wi29:", indice_del_maximo(wi29))

# print("Índice del mínimo en arreglo_dj38:", indice_del_minimo(dj38))
# print("Índice del máximo en arreglo_dj38:", indice_del_maximo(dj38))

# print("Índice del mínimo en arreglo_uy734:", indice_del_minimo(uy734))
# print("Índice del máximo en arreglo_uy734:", indice_del_maximo(uy734))

# print("Índice del mínimo en arreglo_zi929:", indice_del_minimo(zi929))
# print("Índice del máximo en arreglo_zi929:", indice_del_maximo(zi929))

# print("Índice del mínimo en arreglo_lu980:", indice_del_minimo(lu980))
# print("Índice del máximo en arreglo_lu980:", indice_del_maximo(lu980))

# print("Índice del mínimo en arreglo_wi29:", indice_del_minimo(wi29))
# print("Índice del maximo en arreglo_wi29:", indice_del_maximo(dj38))
