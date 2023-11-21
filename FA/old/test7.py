def explorar_izquierda(nodo, luciernaga_i, luciernaga_j):
    indice = luciernaga_i.index(nodo)
    nodos_coincidentes = [nodo]
    
    while indice > 0 and luciernaga_i[indice-1:indice+1] in [luciernaga_j[i:i+2] for i in range(len(luciernaga_j) - 1)]:
        indice -= 1
        nodos_coincidentes.insert(0, luciernaga_i[indice])

    return nodos_coincidentes

def explorar_derecha(nodo, luciernaga_i, luciernaga_j):
    indice = luciernaga_i.index(nodo)
    nodos_coincidentes = [nodo]
    
    while indice < len(luciernaga_i) - 1 and luciernaga_i[indice:indice+2] in [luciernaga_j[i:i+2] for i in range(len(luciernaga_j) - 1)]:
        indice += 1
        nodos_coincidentes.append(luciernaga_i[indice])

    return nodos_coincidentes

# Ejemplo de uso:
luciernaga_i = [6, 7, 8, 4, 2, 1, 5, 15, 12, 3, 16, 11, 9, 10, 13, 14]
luciernaga_j = [6, 7, 12, 13, 14, 1, 8, 4, 2, 3, 16, 11, 9, 10, 15, 5]
nodo_inicial = 3

# nodos_coincidentes = explorar_derecha(nodo_inicial, luciernaga_i, luciernaga_j)
nodos_coincidentes = explorar_izquierda(nodo_inicial, luciernaga_i, luciernaga_j)
print(f"Nodos coincidentes hacia la derecha: {nodos_coincidentes}")


# firefly_i = [6, 7, 8, 4, 2, 1, 5, 15, 12, 3, 16, 11, 9, 10, 13, 14]
# firefly_j = [6, 7, 12, 13, 14, 1, 8, 4, 2, 3, 16, 11, 9, 10, 15, 5]
# node_x = 2
# node_y = 3

# # explorar_izquierda(node_x, firefly_i, firefly_j)
# # explorar_izquierda(node_y, firefly_i, firefly_j)
# explorar_derecha(node_y, firefly_i, firefly_j)
    
