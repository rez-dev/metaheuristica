# GLS
# Rodrigo Escobar Zamorano

####################################################################################################
# IMPORTACION DE LIBRERIAS
####################################################################################################
import math
import random
import time
import matplotlib.pyplot as plt

####################################################################################################
# CLASE SOLUCION
####################################################################################################
class Solucion:
  def __init__(self, ruta=None):
    if ruta is None: #Si no se especifica una ruta se crea una ruta vacía
        self.ruta = [0]
        self.costo = 0
    else:
        self.ruta = ruta
        self.costo = calcular_costo(self, matriz_distancias)

  def swap(self, i, j): #Definición función swap
    nueva_ruta = self.ruta[:]
    nueva_ruta[i], nueva_ruta[j] = nueva_ruta[j], nueva_ruta[i]
    return Solucion(nueva_ruta)
####################################################################################################
# BUSQUEDA MEJOR VECINO
####################################################################################################
def two_opt(sol):
    best_sol = Solucion(sol.ruta)
    # new_sol = Solucion()
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best_sol.ruta) - 2):
            for j in range(i + 2, len(best_sol.ruta)):
                if j - i == 1:
                    continue
                new_sol = two_opt_swap(best_sol, i, j)
                if new_sol.costo < best_sol.costo:
                    best_sol.ruta = new_sol.ruta
                    best_sol.costo = new_sol.costo
                    improved = True
    return best_sol

def two_opt_swap(sol, i, j):
    new_sol = Solucion(sol.ruta[:i] + sol.ruta[i:j][::-1] + sol.ruta[j:])
    return new_sol
####################################################################################################
# CALCULO DE COSTO
####################################################################################################
def calcular_costo(sol, matriz_distancias):
  costo = 0
  for i in range(len(sol.ruta) - 1):
    costo += matriz_distancias[sol.ruta[i]][sol.ruta[i + 1]]
  costo += matriz_distancias[sol.ruta[-1]][sol.ruta[0]]
  return costo

####################################################################################################
# GENERAR SOLUCION INICIAL
####################################################################################################
def generar_solucion_inicial(matriz_distancias):
    # Inicializamos la solución con un recorrido circular aleatorio.
    sol = Solucion()
    datos = list(range(1,len(matriz_distancias)))
    random.shuffle(datos)
    sol.ruta = datos
    sol.ruta.insert(0, 0)
    sol.costo = calcular_costo(sol, matriz_distancias)
    return sol
#####################################################################################################
# BUSQUEDA LOCAL GUIADA
#####################################################################################################        
def busqueda_local_guiada(matriz_distancias, max_iteraciones):
  # Inicializamos la solución con un recorrido circular aleatorio.
  sol = generar_solucion_inicial(matriz_distancias)
  # Bucle hasta que se alcance el número máximo de iteraciones.
  for _ in range(max_iteraciones):
    # Encontramos el vecino mejor de la solución actual.
    mejor_vecino = two_opt(sol)
    # Si el vecino mejor es mejor que la solución actual, lo reemplazamos.
    if mejor_vecino.costo < sol.costo:
      sol = mejor_vecino
  return sol
####################################################################################################
# LECTURA DE DATOS
####################################################################################################
def lectura_archivo(nombre_archivo):
    puntos = []
    try:
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                partes = linea.strip().split()
                if len(partes) == 3:
                    punto_id = int(partes[0])
                    x = float(partes[1])
                    y = float(partes[2])
                    puntos.append((punto_id, x, y))
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")
    return puntos
#####################################################################################################
# CALCULAR MATRIZ DE DISTANCIAS
##################################################################################################### 
def calcular_distancia(puntos):
    n = len(puntos)
    matriz_distancias = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i == j:
                matriz_distancias[i][j] = 0.0
            else:
                x1, y1 = puntos[i][1], puntos[i][2]
                x2, y2 = puntos[j][1], puntos[j][2]
                distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                matriz_distancias[i][j] = int(distancia)
                matriz_distancias[j][i] = int(distancia)
    return matriz_distancias
#####################################################################################################
# EJECUCION
#####################################################################################################
coordenadas = lectura_archivo("wi29.tsp")
matriz_distancias = calcular_distancia(coordenadas)
# matriz_distancias = [[0.0,3.0,4.0,2.0,7.0], [3.0,0.0,4.0,6.0,3.0],[4.0 , 4.0 , 0.0 , 5.0 , 8.0],[2.0 , 6.0 , 5.0 , 0.0 , 6.0],[7.0 , 3.0 , 8.0 , 6.0  ,0.0]]
# # Ejecutar 10 veces el mismo algoritmo y quedarnos con la mejor solución.
historial_soluciones = []
historial_costos = []
inicio = time.time()
best_solution = generar_solucion_inicial(matriz_distancias)
historial_soluciones.append(best_solution.ruta)
historial_costos.append(best_solution.costo)
for _ in range(100):
    sol = busqueda_local_guiada(matriz_distancias, 1000)
    historial_soluciones.append(sol.ruta)
    historial_costos.append(sol.costo)
    # print("hola")
    if sol.costo < best_solution.costo:
        best_solution = sol
        # print(sol.costo)
fin = time.time()

for i in range(len(best_solution.ruta)):
    print(best_solution.ruta[i] + 1, end=' ')
print()
print("Costo: ", best_solution.costo)
print("Tiempo: ", fin - inicio)

# Arreglo de costos (ejemplo)
# costos = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]

# # Crear el gráfico
plt.plot(historial_costos, marker='o', linestyle='-')

# # Configurar etiquetas y título
plt.xlabel('Iteración')
plt.ylabel('Costo')
plt.title('Gráfico de Costos a lo largo de las Iteraciones')

# Mostrar el gráfico
plt.grid(True)  # Agregar una cuadrícula
plt.show()

# matriz_distancias = [[0.0,3.0,4.0,2.0,7.0], [3.0,0.0,4.0,6.0,3.0],[4.0 , 4.0 , 0.0 , 5.0 , 8.0],[2.0 , 6.0 , 5.0 , 0.0 , 6.0],[7.0 , 3.0 , 8.0 , 6.0  ,0.0]]
# sol = Solucion([0,2,1,4,3])
# print(calcular_costo(sol, matriz_distancias))
