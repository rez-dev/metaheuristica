def count_unique_edges(route1, route2):
    edges_route1 = set(route1)
    edges_route2 = set(route2)
    unique_edges_route1 = edges_route1.difference(edges_route2)
    count = len(unique_edges_route1)
    # reverse each edge
    reverse = set(map(lambda x: (x[1], x[0]), unique_edges_route1))
    for edge in reverse:
        if edge in edges_route2:
            count -= 1
    return count

def generate_edges_from_route(route):
    edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
    return edges

# ruta1 = [1,2,3,4,5,6]
# ruta2 = [1,3,2,5,4,6]
ruta1 = [1,14,13,12,7,6,15,5,11,9,10,16,3,2,4,8]
ruta2 = [1,14,13,12,15,5,7,6,11,9,10,16,3,2,4,8]

aristas_generadas1 = generate_edges_from_route(ruta1)
aristas_generadas2 = generate_edges_from_route(ruta2)

print(aristas_generadas1)
print(aristas_generadas2)


cantidad_aristas_distintas = count_unique_edges(aristas_generadas1, aristas_generadas2)

print(f"Cantidad de aristas distintas en la ruta1 respecto a la ruta2: {cantidad_aristas_distintas}")