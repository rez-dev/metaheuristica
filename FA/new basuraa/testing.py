from typing import List
from math import sqrt
from random import randint, shuffle

class Node:
    def __init__(self, node_id: int, x: float, y: float):
        self.id = node_id
        self.x = x
        self.y = y

class Firefly:
    def __init__(self, path: List[Node], cost: float):
        self.path = path
        self.cost = cost

def euclidean_distance(n1: Node, n2: Node) -> float:
    return sqrt((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2)

def create_distance_matrix(nodes: List[Node]) -> List[List[float]]:
    node_num = len(nodes)
    result_matrix = [[0.0] * node_num for _ in range(node_num)]

    for n1 in nodes:
        for n2 in nodes:
            result_matrix[n1.id - 1][n2.id - 1] = euclidean_distance(n1, n2)

    return result_matrix

def inversion_mutation(firefly: Firefly, distance_matrix: List[List[float]], r: int) -> Firefly:
    length_of_mutation = min(randint(2, r), len(firefly.path))
    max_len = len(firefly.path) - length_of_mutation + 1
    if max_len <= 1:
        max_len = 2
    
    index1 = randint(0, max_len - 1)
    index2 = index1 + length_of_mutation
    
    mutated_path = list(reversed(firefly.path[index1:index2]))
    
    new_f = Firefly(mutated_path, path_cost(Firefly(mutated_path, -1.0), distance_matrix))
    return new_f

def path_cost(firefly: Firefly, distance_matrix: List[List[float]]) -> float:
    path = firefly.path
    path_len = len(path) - 1
    p_cost = distance_matrix[path[-1].id - 1][path[0].id - 1]

    for i in range(path_len):
        p_cost += distance_matrix[path[i].id - 1][path[i + 1].id - 1]

    return p_cost

def read_tsp_file(file_name: str) -> List[Node]:
    nodes = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        node_section = False
        for line in lines:
            line = line.strip()
            if line.startswith("NODE_COORD_SECTION"):
                node_section = True
                continue
            if node_section and line != "EOF" and line != "":
                data = line.split()
                node_id = int(data[0])
                x_coord = float(data[1])
                y_coord = float(data[2])
                nodes.append(Node(node_id, x_coord, y_coord))
    return nodes


# Lectura del archivo TSP y preparación para el algoritmo de luciérnagas
file_name = "berlin52.tsp"  # Cambiar al nombre del archivo correcto si es diferente
nodes = read_tsp_file(file_name)
distance_matrix = create_distance_matrix(nodes)
# print(distance_matrix)

# Aquí puedes aplicar el algoritmo de luciérnagas con los nodos y la matriz de distancias
# Asegúrate de llamar a las funciones y clases según sea necesario con los datos leídos del archivo TSP
# Por ejemplo:
firefly = Firefly(nodes, 0.0)
mutated_firefly = inversion_mutation(firefly, distance_matrix, 3)
cost = path_cost(firefly, distance_matrix)
print(f"Costo de ruta: {cost}")
