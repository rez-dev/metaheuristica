import math
from typing import List
from random import shuffle, uniform

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
    return ((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2) ** 0.5

def create_distance_matrix(nodes: List[Node]) -> List[List[float]]:
    node_num = len(nodes)
    result_matrix = [[0.0] * node_num for _ in range(node_num)]

    for i in range(node_num):
        for j in range(node_num):
            result_matrix[i][j] = euclidean_distance(nodes[i], nodes[j])

    return result_matrix

def initialize_fireflies(nodes: List[Node], population_size: int) -> List[Firefly]:
    fireflies = []
    for _ in range(population_size):
        path = nodes[:]
        shuffle(path)
        fireflies.append(Firefly(path, path_cost(path)))
    return fireflies

def path_cost(path: List[Node]) -> float:
    total_distance = sum(euclidean_distance(path[i], path[i + 1]) for i in range(len(path) - 1))
    return total_distance + euclidean_distance(path[-1], path[0])

def move_fireflies(fireflies: List[Firefly], distance_matrix: List[List[float]], attractiveness: float) -> List[Firefly]:
    for i in range(len(fireflies)):
        for j in range(len(fireflies)):
            if fireflies[j].cost < fireflies[i].cost:  # Compara la intensidad de la luciérnaga j con la i
                r = euclidean_distance(fireflies[i].path[0], fireflies[j].path[0])
                beta = 1.0
                attractiveness = 0.2
                exp_value = -beta * (r ** 2)
                attractiveness *= math.exp(exp_value)
                if attractiveness > uniform(0, 1):  # Compara la intensidad con una probabilidad aleatoria
                    fireflies[i].path = fireflies[j].path[:]  # Mueve la luciérnaga i hacia la j
                    fireflies[i].cost = fireflies[j].cost
    return fireflies

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

# Leer datos del archivo TSP
file_name = "berlin52.tsp"  # Cambiar al nombre del archivo correcto si es diferente
nodes = read_tsp_file(file_name)
distance_matrix = create_distance_matrix(nodes)

# Inicializar luciérnagas
population_size = 50
fireflies = initialize_fireflies(nodes, population_size)

# Algoritmo de Luciérnagas (Firefly Algorithm)
max_generations = 100
for generation in range(max_generations):
    fireflies = move_fireflies(fireflies, distance_matrix, 0.2)  # Mover las luciérnagas hacia las más brillantes

# Seleccionar la mejor solución después de las generaciones
best_firefly = min(fireflies, key=lambda x: x.cost)

# Imprimir el resultado
print("Mejor costo encontrado:", best_firefly.cost)
print("Mejor ruta encontrada:", [node.id for node in best_firefly.path])
