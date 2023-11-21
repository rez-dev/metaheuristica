import numpy as np
import matplotlib.pyplot as plt

# Función para calcular la distancia euclidiana entre dos puntos
def distance(point1, point2):
    return np.linalg.norm(point1 - point2)

# Función para calcular la distancia total del recorrido
def total_distance(path, cities):
    total = 0
    for i in range(len(path) - 1):
        total += distance(cities[path[i]], cities[path[i+1]])
    total += distance(cities[path[-1]], cities[path[0]])  # Volver al inicio
    return total

# Función para inicializar las luciérnagas (puntos) en el espacio de búsqueda
def initialize_fireflies(num_fireflies, num_cities):
    return np.random.permutation(num_cities)[:num_fireflies]

# Función para actualizar el brillo (intensidad luminosa) de las luciérnagas
def update_fireflies_intensity(fireflies, cities):
    intensities = [total_distance(firefly, cities) for firefly in fireflies]
    return intensities

# Función para el movimiento de las luciérnagas basado en el Edge Based Movement
def move_fireflies(fireflies, intensities):
    for i in range(len(fireflies)):
        for j in range(len(fireflies)):
            if intensities[i] > intensities[j]:
                temp = fireflies[i].copy()
                for k in range(len(fireflies[i])):
                    diff_idx = np.where(fireflies[i] != fireflies[j][k])[0]
                    if len(diff_idx) > 0:
                        idx = diff_idx[0]
                        fireflies[i][k], fireflies[i][idx] = fireflies[i][idx], fireflies[i][k]
                intensities[i] = total_distance(fireflies[i], cities)
                if intensities[i] < intensities[j]:
                    fireflies[i] = temp.copy()
                    intensities[i] = total_distance(fireflies[i], cities)
    return fireflies, intensities


# Genera ciudades aleatorias en un espacio 2D
np.random.seed(42)  # Establece la semilla para reproducibilidad
num_cities = 20
cities = np.random.rand(num_cities, 2)  # Coordenadas (x, y) de las ciudades

# Parámetros del algoritmo
num_fireflies = 10
iterations = 100

# Inicializa las luciérnagas
fireflies = [initialize_fireflies(num_cities, num_cities) for _ in range(num_fireflies)]

# Optimización
for _ in range(iterations):
    intensities = update_fireflies_intensity(fireflies, cities)
    fireflies, intensities = move_fireflies(fireflies, intensities)

# Encuentra la mejor solución
best_index = np.argmin(intensities)
best_path = fireflies[best_index]

# Muestra el mejor recorrido encontrado
plt.figure(figsize=(6, 6))
plt.scatter(cities[:, 0], cities[:, 1], c='red')
for i in range(len(best_path) - 1):
    plt.plot([cities[best_path[i]][0], cities[best_path[i+1]][0]],
             [cities[best_path[i]][1], cities[best_path[i+1]][1]], 'blue')
plt.plot([cities[best_path[-1]][0], cities[best_path[0]][0]],
         [cities[best_path[-1]][1], cities[best_path[0]][1]], 'blue')
plt.title(f"Mejor recorrido: {intensities[best_index]:.2f}")
plt.show()
