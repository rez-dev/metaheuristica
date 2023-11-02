# GLS
# Rodrigo Escobar Zamorano

# IMPORTACIÓN DE LIBRERIAS
import math
import random

# LECTURA DE DATOS
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

# CALCULAR DISTANCIA
def calcular_matriz_distancias(coordenadas):
    n = len(coordenadas)
    matriz = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                distancia = math.sqrt((coordenadas[j][1] - coordenadas[i][1]) ** 2 + (coordenadas[j][2] - coordenadas[i][2]) ** 2)
                matriz[i][j] = distancia
    return matriz

# GENERAR SOLUCION INICIAL
def generar_solucion_inicial(matriz_distancias):
    solucion_inicial = list(range(1,len(matriz_distancias)))
    random.shuffle(solucion_inicial)
    solucion_inicial.insert(0, 0)
    return solucion_inicial

# CALCULAR COSTO
def calcular_costo(solucion, matriz_distancias):
    costo = 0
    for i in range(len(solucion) - 1):
        costo += matriz_distancias[solucion[i]][solucion[i + 1]]
    costo += matriz_distancias[solucion[-1]][solucion[0]]
    return costo

# BUSQUEDA LOCAL
# Dada una solucion busca la mejor solucion en su vecindario, si esta es mejor pasa a ser la solucion actual, si no, se termina la busqueda,
# si la encuentra, se repite el proceso hasta que no se encuentre una mejor solucion
def local_search(current_solution, cost_function):
    improved = True
    best_solution = current_solution
    best_cost = cost_function(current_solution)
    while improved:
        improved = False

        for i in range(1,len(current_solution) - 2):
            for j in range(i + 2, len(current_solution)):
                new_solution = current_solution[:i] + current_solution[i:j][::-1] + current_solution[j:]
                new_cost = cost_function(new_solution)
                if new_cost < best_cost:
                    best_solution = new_solution
                    best_cost = new_cost
                    improved = True
                    # print("mejora: ",i,j)
                    break  # Break the inner loop, start over with a new i
        current_solution = best_solution
        # print(current_solution)
        # print("hola")
    return best_solution

# ACTUALIZAR PENALIZACIONES
def actualizar_penalizaciones(solucion,diferencia_soluciones, penalizaciones):
    for i in range(len(solucion)-1):
        penalizaciones[solucion[i]][solucion[i + 1]] += diferencia_soluciones
    return penalizaciones

# APLICAR PENALIZACIONES A SOLUCION
def aplicar_penalizaciones(solucion_actual, penalizaciones):
    new_solucion = solucion_actual[:]
    # Encontrar la arista con la mayor penalización
    max_penalizacion = -1
    ciudad_a = -1
    ciudad_b = -1
    # Se busca la maxima penalizacion en la solucion actual
    for i in range(len(new_solucion)):
        for j in range(i + 1, len(new_solucion)):
            if penalizaciones[new_solucion[i]][new_solucion[j]] > max_penalizacion:
                max_penalizacion = penalizaciones[new_solucion[i]][new_solucion[j]]
                ciudad_a = i
                ciudad_b = j

    # Realizar un 2-opt swap para invertir la arista con la mayor penalización
    while ciudad_a < ciudad_b:
        new_solucion[ciudad_a], new_solucion[ciudad_b] = new_solucion[ciudad_b], new_solucion[ciudad_a]
        ciudad_a += 1
        ciudad_b -= 1

    return new_solucion

# ACTUALIZAR ESTRUCTURA DE PENALIZACION
def actualizar_estructura_penalizacion(penalizaciones, factor_enfriamiento):
    # Reducir todas las penalizaciones con un factor de enfriamiento
    for i in range(len(penalizaciones)):
        for j in range(len(penalizaciones[i])):
            penalizaciones[i][j] = penalizaciones[i][j] * factor_enfriamiento
    return penalizaciones

# GUIDED LOCAL SEARCH
def guided_local_search(alpha, max_iteraciones,matriz_distancias):
    # Generar solucion inicial
    solucion_inicial = generar_solucion_inicial(matriz_distancias)
    solucion_actual = solucion_inicial
    costo_actual = calcular_costo(solucion_actual, matriz_distancias)
    # Inicializar matriz de penalizaciones (matriz de 0s)
    penalizaciones = [[0 for _ in range(len(matriz_distancias))] for _ in range(len(matriz_distancias))]
    
    for _ in range(max_iteraciones):
        # Se genera una nueva solucion a partir de la solucion actual
        nueva_solucion = local_search(solucion_actual, lambda x: calcular_costo(x, matriz_distancias))
        nuevo_costo = calcular_costo(nueva_solucion, matriz_distancias)
        # Se actualiza la solucion actual si la nueva solucion es mejor
        if nuevo_costo < costo_actual:
            solucion_actual = nueva_solucion
            costo_actual = nuevo_costo
        # Si no, se penaliza la solucion actual y se genera una nueva solucion inicial
        else:
            # Se actualizan las penalizaciones en base a la nueva solucion
            penalizaciones = actualizar_penalizaciones(nueva_solucion, nuevo_costo-costo_actual, penalizaciones)
            # Se aplica la penalizacion a la solucion actual
            nueva_solucion = aplicar_penalizaciones(nueva_solucion, penalizaciones)
            # Actualizar estructura de penalizaciones (enfriamiento)
            penalizaciones = actualizar_estructura_penalizacion(penalizaciones, alpha)
        print(nueva_solucion)
        print(nuevo_costo)
    
    return solucion_actual









#####################################################################################################
# EJECUCION
#####################################################################################################
# random.seed(1)
# archivo = "./datasets/wi29.tsp"
# coordenadas = lectura_archivo(archivo)
# matriz_distancias = calcular_matriz_distancias(coordenadas)
# solucion_inicial = generar_solucion_inicial(matriz_distancias)
# print(solucion_inicial)
# print(calcular_costo(solucion_inicial, matriz_distancias))
# solucion_inicial = [0, 1, 2, 3, 4, 5, 6]
# prueba = local_search(solucion_inicial, lambda x: calcular_costo(x, matriz_distancias))
# print(prueba)
# print(calcular_costo(prueba, matriz_distancias))

# penalizaciones = [[0 for _ in range(10)] for _ in range(10)]
# for i in range(1,10):
#     print(penalizaciones[i])

# solucion = [0,1,2,3]
# penalizaciones = [[0 for _ in range(4)] for _ in range(4)]
# for i in range(len(solucion)):
#     print(penalizaciones[i])
# penalizaciones = actualizar_penalizaciones(solucion, 6, penalizaciones)
# for i in range(len(solucion)):
#     print(penalizaciones[i])

# solucion = [0,1,3,2]
# penalizaciones = actualizar_penalizaciones(solucion, 6, penalizaciones)
# for i in range(len(solucion)):
#     print(penalizaciones[i])

# solucion = [0,1,2,3]
# # new_solucion = two_opt_swap(solucion, 1, 3)
# print(solucion)
# print(new_solucion)

solucion = [0,1,2,3]

penalizaciones = [[0 for _ in range(4)] for _ in range(4)]
penalizaciones[1][2] = 6
# for i in range(len(solucion)):
#     print(penalizaciones[i])
new_solucion = aplicar_penalizaciones(solucion, penalizaciones)
print(solucion, new_solucion)