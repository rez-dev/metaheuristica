def distancia_luciernagas(luciernaga1, luciernaga2):
    aristas_ruta1 = set(luciernaga1)
    aristas_ruta2 = set(luciernaga2)
    diferencias = aristas_ruta1.difference(aristas_ruta2)
    cantidad_aristas_distintas = len(diferencias)
    # reverse each edge
    aristas_inversas = set(map(lambda x: (x[1], x[0]), diferencias))
    for arista in aristas_inversas:
        if arista in aristas_ruta2:
            cantidad_aristas_distintas -= 1
    return cantidad_aristas_distintas

def generar_aristas(luciernaga):
    aristas = [(luciernaga[i], luciernaga[i + 1]) for i in range(len(luciernaga) - 1)]
    return aristas

ruta1 = [1,2,3,4,5,6]
ruta2 = [1,3,2,5,4,6]
# ruta2 = [1,2,3,4,5,6]
# ruta1 = [1,3,2,5,4,6]
# ruta1 = [1,14,13,12,7,6,15,5,11,9,10,16,3,2,4,8]
# ruta2 = [1,14,13,12,15,5,7,6,11,9,10,16,3,2,4,8]

aristas_generadas1 = generar_aristas(ruta1)
aristas_generadas2 = generar_aristas(ruta2)

print(aristas_generadas1)
print(aristas_generadas2)


cantidad_aristas_distintas = distancia_luciernagas(aristas_generadas1, aristas_generadas2)

print(f"Cantidad de aristas distintas en la ruta1 respecto a la ruta2: {cantidad_aristas_distintas}")