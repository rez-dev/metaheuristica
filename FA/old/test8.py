def explorar_lados(nodo, luciernaga_i, luciernaga_j):
    indice = luciernaga_i.index(nodo)
    nodos_coincidentes_izquierda = [nodo]
    nodos_coincidentes_derecha = [nodo]
    
    # Explorar hacia la izquierda
    while indice > 0 and luciernaga_i[indice-1:indice+1] in [luciernaga_j[i:i+2] for i in range(len(luciernaga_j) - 1)]:
        indice -= 1
        nodos_coincidentes_izquierda.insert(0, luciernaga_i[indice])

    indice = luciernaga_i.index(nodo)
    
    # Explorar hacia la derecha
    while indice < len(luciernaga_i) - 1 and luciernaga_i[indice:indice+2] in [luciernaga_j[i:i+2] for i in range(len(luciernaga_j) - 1)]:
        indice += 1
        nodos_coincidentes_derecha.append(luciernaga_i[indice])

    # Combinar nodos coincidentes hacia la izquierda y derecha en un solo arreglo
    nodos_coincidentes = nodos_coincidentes_izquierda + nodos_coincidentes_derecha[1:]  # Excluir nodo duplicado
    return nodos_coincidentes

# Ejemplo de uso:
luciernaga_i = [6, 7, 8, 4, 2, 1, 5, 15, 12, 3, 16, 11, 9, 10, 13, 14]
luciernaga_j = [6, 7, 12, 13, 14, 1, 8, 4, 2, 3, 16, 11, 9, 10, 15, 5]
nodo_x = 2
nodo_y = 3

nodos_coincidentes_x = explorar_lados(nodo_x, luciernaga_i, luciernaga_j)
nodos_coincidentes_y = explorar_lados(nodo_y, luciernaga_i, luciernaga_j)

# print(f"Nodos coincidentes hacia la izquierda y derecha de x: {nodos_coincidentes_x}")
# print(f"Nodos coincidentes hacia la izquierda y derecha de y: {nodos_coincidentes_y}")

# Ejemplo de uso:

nodos_coincidentes_x = [8, 4, 2]
nodos_coincidentes_y = [3, 16, 11, 9, 10]
# originales
# firefly_i = [6, 7, 8, 4, 2, 1, 5, 15, 12, 3, 16, 11, 9, 10, 13, 14]

firefly_i1 = [6, 7, 1, 5, 15, 12, 8, 4, 2, 3, 16, 11, 9, 10, 13, 14]
firefly_i1 = [6, 7, 1, 5, 15, 12, 8, 4, 2, 3, 16, 11, 9, 10, 13, 14]

firefly_i2 = [6, 7, 1, 5, 15, 12, 10, 9, 11, 16, 3, 2, 4, 8, 13, 14]
firefly_i2 = [6, 7, 1, 5, 15, 12, 10, 9, 11, 16, 3, 2, 4, 8, 13, 14]

firefly_i3 = [6, 7, 10, 9, 11, 16, 3, 2, 4, 8, 1, 5, 15, 12, 13, 14]
firefly_i3 = [6, 7, 8, 3, 16, 11, 9, 10, 8, 4, 2, 4, 2, 1, 5, 15, 12, 13, 14]

firefly_i4 = [6, 7, 8, 4, 2, 3, 16, 11, 9, 10, 1, 5, 15, 12, 13, 14]



def generar_nuevas_soluciones(firefly_i, nodos_coincidentes_x, nodos_coincidentes_y):
    nuevas_soluciones = []

    # Generar solución i1
    nueva_solucion_i1 = firefly_i.copy()
    for nodo in nodos_coincidentes_x:
        nueva_solucion_i1.remove(nodo)
    indice_y = nueva_solucion_i1.index(nodos_coincidentes_y[0])
    nueva_solucion_i1 = (
        nueva_solucion_i1[:indice_y] + nodos_coincidentes_x + nodos_coincidentes_y + nueva_solucion_i1[indice_y + len(nodos_coincidentes_y):]
    )
    nuevas_soluciones.append(nueva_solucion_i1)

    # Generar solución i2
    nueva_solucion_i2 = firefly_i.copy()
    for nodo in nodos_coincidentes_x:
        nueva_solucion_i2.remove(nodo)
    indice_y = nueva_solucion_i2.index(nodos_coincidentes_y[0])
    nodos_coincidentes_x.reverse()  # Invertir el orden de los nodos coincidentes de x
    nodos_coincidentes_y.reverse()  # Invertir el orden de los nodos coincidentes de y
    nueva_solucion_i2 = (
        nueva_solucion_i2[:indice_y] + nodos_coincidentes_y + nodos_coincidentes_x + nueva_solucion_i2[indice_y + len(nodos_coincidentes_y):]
    )
    nuevas_soluciones.append(nueva_solucion_i2)

    # Generar solución i3
    nueva_solucion_i3 = firefly_i.copy()
    for nodo in nodos_coincidentes_y:
        nueva_solucion_i3.remove(nodo)
    indice_x = nueva_solucion_i3.index(nodos_coincidentes_x[-1])
    nueva_solucion_i3 = (
        nueva_solucion_i3[:indice_x + 1] + nodos_coincidentes_y[::-1] + nodos_coincidentes_x[::-1] + nueva_solucion_i3[indice_x + 1:]
    )
    nuevas_soluciones.append(nueva_solucion_i3)

    # Generar solución i4
    nueva_solucion_i4 = firefly_i.copy()
    for nodo in nodos_coincidentes_y:
        nueva_solucion_i4.remove(nodo)
    indice_x = nueva_solucion_i4.index(nodos_coincidentes_x[-1])
    nueva_solucion_i4 = (
        nueva_solucion_i4[:indice_x + 1] + nodos_coincidentes_y + nodos_coincidentes_x + nueva_solucion_i4[indice_x + 1:]
    )
    nuevas_soluciones.append(nueva_solucion_i4)

    return nuevas_soluciones

# Ejemplo de uso:
firefly_i = [6, 7, 8, 4, 2, 1, 5, 15, 12, 3, 16, 11, 9, 10, 13, 14]
nodos_coincidentes_x = [8, 4, 2]
nodos_coincidentes_y = [3, 16, 11, 9, 10]

nuevas_soluciones = generar_nuevas_soluciones(firefly_i, nodos_coincidentes_x, nodos_coincidentes_y)
for idx, solucion in enumerate(nuevas_soluciones, start=1):
    print(f"firefly_i{idx} = {solucion}")











