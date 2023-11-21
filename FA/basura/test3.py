def count_unique_edges(route1, route2):
    edges_route1 = set(route1)
    edges_route2 = set(route2)

    unique_edges_route1 = edges_route1.difference(edges_route2)
    # print(unique_edges_route1)
    count1 = len(unique_edges_route1)
    # print(count1)

    # reverse each edge
    unique_edges_route2 = set(map(lambda x: (x[1], x[0]), unique_edges_route1))
    # print(unique_edges_route2)
    for edge in unique_edges_route2:
        if edge in edges_route2:
            count1 -= 1
    # print(count1)
    return count1

def generate_edges_from_route(route):
    edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
    # edges.append((route[-1], route[0]))
    return edges

# Ejemplo de uso
# ruta_ejemplo = [1, 2, 3, 4]


# print("Aristas generadas:")
# for arista in aristas_generadas:
#     print(arista)


# ruta1 = [(1, 2), (2, 3), (3, 4)]
# ruta2 = [(1, 3), (3, 2), (2, 4)]
ruta1 = [1,2,3,4,5,6]
ruta2 = [1,3,2,5,4,6]

aristas_generadas1 = generate_edges_from_route(ruta1)
aristas_generadas2 = generate_edges_from_route(ruta2)

print(aristas_generadas1)
print(aristas_generadas2)


cantidad_aristas_distintas = count_unique_edges(aristas_generadas1, aristas_generadas2)

print(f"Cantidad de aristas distintas en la ruta1 respecto a la ruta2: {cantidad_aristas_distintas}")
