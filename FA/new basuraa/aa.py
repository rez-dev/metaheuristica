import random
import numpy as np
import matplotlib.pyplot as plt
import math

class Tsp:
    # constructor ----------------------------------------------------
    def __init__(self):
        self.nombre = '' # nombre archivo
        self.num_nodos = 0  # cantidad de nodos
        self.coord = []  # coordenadas de nodos
        self.vecinos = []  # lista de vecinos
    # lectura TSP --------------------------------------------------
    def leer(self, filename):
        # abrir archivo
        input_file = open(filename, 'r')
        data = input_file.readlines()
        input_file.close()

        # leer informacion
        for i in range(len(data)):
            data[i] = (data[i].rstrip()).split()
            data[i] = list(filter(lambda str:str != ':', data[i]))  # remove colon
            if len(data[i]) > 0:
                data[i][0] = data[i][0].rstrip(':')
                if data[i][0] == 'NAME':
                    self.nombre = data[i][1]
                elif data[i][0] == 'TYPE':
                    if data[i][1] != 'TSP':
                        print('Problem type is not TSP!')
                        sys.exit(1)
                elif data[i][0] == 'DIMENSION':
                    self.num_nodos = int(data[i][1])
                elif data[i][0] == 'EDGE_WEIGHT_TYPE':  # NOTE: accept only EUC_2D
                    if data[i][1] != 'EUC_2D':
                        print('Edge weight type is not EUC_2D')
                        sys.exit(1)
                elif data[i][0] == 'NODE_COORD_SECTION':
                    sec_coord = i

        # obtencion de coordenadas
        self.coord = [(0.0, 0.0)] * self.num_nodos
        line_cnt = sec_coord+1
        for i in range(self.num_nodos):
            (self.coord)[int(data[line_cnt][0])-1] = (float(data[line_cnt][1]),float(data[line_cnt][2]))
            line_cnt += 1

    # imprimir info TSP -------------------------------------------------
    def escribir(self):
        print('\n[TSP data]')
        print('nombre:\t{}'.format(self.nombre))
        print('#nodo:\t{}'.format(self.num_nodos))
        # print('coord:\t{}'.format(self.coord))

    # calcular distancia_euc (rounded euclidian distance in 2D) ----------
    def distancia_euc(self,v1,v2):
        xd = float((self.coord)[v1][0] - (self.coord)[v2][0])
        yd = float((self.coord)[v1][1] - (self.coord)[v2][1])
        return float(int(math.sqrt(xd * xd + yd * yd)+0.5))

# Función para calcular la distancia euclidiana entre dos puntos
def distance(point1, point2):
    return np.linalg.norm(point1 - point2)

# Función para calcular la distancia total del recorrido
def total_distance(path, tsp_instance):
    total = 0
    for i in range(len(path) - 1):
        total += tsp_instance.distancia_euc(path[i], path[i+1])
    total += tsp_instance.distancia_euc(path[-1], path[0])  # Volver al inicio
    return total

# Función para inicializar las luciérnagas (puntos) en el espacio de búsqueda
def initialize_fireflies(num_fireflies, num_cities):
    return np.random.permutation(num_cities)[:num_fireflies]

# Función para actualizar el brillo (intensidad luminosa) de las luciérnagas
def update_fireflies_intensity(fireflies, tsp_instance):
    intensities = [total_distance(firefly, tsp_instance) for firefly in fireflies]
    return intensities

# Función para el movimiento de las luciérnagas basado en el Edge Based Movement
def move_fireflies(fireflies, intensities, tsp_instance):
    for i in range(len(fireflies)):
        for j in range(len(fireflies)):
            if intensities[i] > intensities[j]:
                temp = fireflies[i].copy()
                for k in range(len(fireflies[i])):
                    diff_idx = np.where(fireflies[i] != fireflies[j][k])[0]
                    if len(diff_idx) > 0:
                        idx = diff_idx[0]
                        fireflies[i][k], fireflies[i][idx] = fireflies[i][idx], fireflies[i][k]
                intensities[i] = total_distance(fireflies[i], tsp_instance)
                if intensities[i] < intensities[j]:
                    fireflies[i] = temp.copy()
                    intensities[i] = total_distance(fireflies[i], tsp_instance)
    return fireflies, intensities

# Crear una instancia de Tsp y leer datos desde el archivo
tsp_instance = Tsp()
tsp_instance.leer('./datasets/wi29.tsp')  # Reemplaza 'archivo.tsp' con el nombre de tu archivo TSP

# Parámetros del algoritmo
random.seed(42)  # Establece la semilla para reproducibilidad
num_fireflies = 10
iterations = 100000

# Inicializa las luciérnagas
num_cities = tsp_instance.num_nodos
fireflies = [initialize_fireflies(num_cities, num_cities) for _ in range(num_fireflies)]

# Optimización
for _ in range(iterations):
    intensities = update_fireflies_intensity(fireflies, tsp_instance)
    fireflies, intensities = move_fireflies(fireflies, intensities, tsp_instance)

# Encuentra la mejor solución
best_index = np.argmin(intensities)
best_path = fireflies[best_index]

# Muestra el mejor recorrido encontrado
plt.figure(figsize=(6, 6))
for i in range(len(best_path) - 1):
    plt.plot([tsp_instance.coord[best_path[i]][0], tsp_instance.coord[best_path[i+1]][0]],
             [tsp_instance.coord[best_path[i]][1], tsp_instance.coord[best_path[i+1]][1]], 'blue')
plt.plot([tsp_instance.coord[best_path[-1]][0], tsp_instance.coord[best_path[0]][0]],
         [tsp_instance.coord[best_path[-1]][1], tsp_instance.coord[best_path[0]][1]], 'blue')
plt.scatter([coord[0] for coord in tsp_instance.coord], [coord[1] for coord in tsp_instance.coord], c='red')
plt.title(f"Mejor recorrido: {intensities[best_index]:.2f}")
plt.show()

    # # DATASETS OPTIMUM VALUES
    # qa194 = 9352
    # wi29 = 27603
    # dj38 = 6656
    # uy734 = 79114
    # zi929 = 95345
    # lu980 = 11340
