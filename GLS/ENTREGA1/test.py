# GLS
# Rodrigo Escobar Zamorano

####################################################################################################
# IMPORTACION DE LIBRERIAS
####################################################################################################
import random
import time

####################################################################################################
# CLASE SOLUCION
####################################################################################################
class Solucion:
  def __init__(self, ruta=None):
    if ruta is None:
        self.ruta = []  # Si no se proporciona una ruta, inicializa como una lista vacía
        self.costo = 0
    else:
        self.ruta = ruta
        self.costo = calcular_costo(self, matriz_distancias)

  def swap(self, i, j):
    nueva_ruta = self.ruta[:]
    nueva_ruta[i], nueva_ruta[j] = nueva_ruta[j], nueva_ruta[i]
    return Solucion(nueva_ruta)

####################################################################################################
# LECTURA DE DATOS
####################################################################################################
matriz_distancias = []
with open('p01_d.txt', 'r') as archivo:
    for linea in archivo:
        valores = [int(valor) for valor in linea.split()]
        matriz_distancias.append(valores)

####################################################################################################
# BUSQUEDA MEJOR VECINO
####################################################################################################
def encontrar_mejor_vecino(sol, matriz_distancias):
  mejor_vecino = sol
  mejor_costo = sol.costo

  for i in range(len(sol.ruta)):
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
    sol.ruta = list(range(len(matriz_distancias)))
    random.shuffle(sol.ruta)
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
#####################################################################################################
# EJECUCION
#####################################################################################################   
# Ejecutar 10 veces el mismo algoritmo y quedarnos con la mejor solución.
inicio = time.time()
best_solution = generar_solucion_inicial(matriz_distancias)
for _ in range(100):
    sol = busqueda_local_guiada(matriz_distancias, 100)
    if sol.costo < best_solution.costo:
        best_solution = sol
fin = time.time()

print("Ruta: ", best_solution.ruta)
print("Costo: ", best_solution.costo)
print("Tiempo: ", fin - inicio)
#####################################################################################################

