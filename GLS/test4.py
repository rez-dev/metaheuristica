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
def encontrar_mejor_vecino(sol, matriz_distancias):
  mejor_vecino = sol
  mejor_costo = sol.costo

  for i in range(1, len(sol.ruta)):
    for j in range(i + 1, len(sol.ruta)):
      vecino = sol.swap(i, j)
      costo = calcular_costo(vecino, matriz_distancias)
      if costo < mejor_costo:
        mejor_vecino = vecino
        mejor_costo = costo
  return mejor_vecino

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
    mejor_vecino = encontrar_mejor_vecino(sol, matriz_distancias)
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
                matriz_distancias[i][j] = distancia
                matriz_distancias[j][i] = distancia
    return matriz_distancias
#####################################################################################################
# EJECUCION
#####################################################################################################
coordenadas = lectura_archivo("dj38.tsp")
matriz_distancias = calcular_distancia(coordenadas)
# Ejecutar 10 veces el mismo algoritmo y quedarnos con la mejor solución.
# historial_soluciones = []
# historial_costos = []
inicio = time.time()
best_solution = generar_solucion_inicial(matriz_distancias)
# historial_soluciones.append(best_solution.ruta)
# historial_costos.append(best_solution.costo)
for _ in range(10):
    sol = busqueda_local_guiada(matriz_distancias, 1000)
    # historial_soluciones.append(sol.ruta)
    # historial_costos.append(sol.costo)
    if sol.costo < best_solution.costo:
        best_solution = sol
fin = time.time()

# print("Ruta: ", best_solution.ruta)
for i in range(len(best_solution.ruta)):
    print(best_solution.ruta[i] + 1, end=' ')
print()
# solucion_original = [1,13,2,15,9,5,7,3,12,14,10,8,6,4,11,1]
# solucion_original = [1,4,13,7,8,6,17,14,15,3,11,10,2,5,9,12,16]
# for i in range(len(solucion_original)):
#     print(solucion_original[i], end=' ')
# print()
# print("Costo Original: ", 2085)
# print("Costo Original: ", 699)
print("Costo: ", best_solution.costo)
print("Tiempo: ", fin - inicio)

# print("##############################################")
# print("##############################################")
# for fila in historial_soluciones:
#     for i in range(len(fila)):
#         print(fila[i] + 1, end=' ')
#     print()
#####################################################################################################
# calcular costos
# sol = Solucion([0,15,11,8,4,1,9,10,2,14,13,16,5,7,6,12,3])
# costos = calcular_costo(sol, matriz_distancias)
# print(costos)
# solucion_original = Solucion([0,3,12,6,7,5,16,13,14,2,10,9,1,4,8,11,15])
# calcular_costo = calcular_costo(solucion_original, matriz_distancias)
# print(calcular_costo)



# Arreglo de costos (ejemplo)
# costos = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]

# # Crear el gráfico
# plt.plot(historial_costos, marker='o', linestyle='-')

# # Configurar etiquetas y título
# plt.xlabel('Iteración')
# plt.ylabel('Costo')
# plt.title('Gráfico de Costos a lo largo de las Iteraciones')

# # Mostrar el gráfico
# plt.grid(True)  # Agregar una cuadrícula
# plt.show()
