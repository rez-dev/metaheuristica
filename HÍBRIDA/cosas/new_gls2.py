# GLS FOR TSP
# Rodrigo Escobar Zamorano

import copy
import math
import random
import sys
import time

from matplotlib import pyplot as plt
import optuna


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
    

class Solucion:
    # constructor ----------------------------------------------------
    def __init__(self):
        self.ruta = []  # ruta
        self.recorrido_total = 0  # recorrido total
        self.penalizaciones = {} # penalizaciones
        self.grado_penalizacion = 0
    
    def calcular_costo_recorrido(self,tsp):
        largo = 0.0
        for i in range(len(self.ruta)):
            largo += tsp.distancia_euc((self.ruta)[i],(self.ruta)[(i+1) % len(self.ruta)])
        self.recorrido_total = largo

    def costo_recorrido(self,tsp):
        largo = 0.0
        for i in range(len(self.ruta)):
            largo += tsp.distancia_euc((self.ruta)[i],(self.ruta)[(i+1) % len(self.ruta)])
        return largo
    
    def distancia_penalizada(self,tsp,v1,v2):
        if (v1,v2) in self.penalizaciones:
            return tsp.distancia_euc(v1,v2) + self.grado_penalizacion * (self.penalizaciones)[v1,v2]
        else:
            return tsp.distancia_euc(v1,v2)
        
    def costo_recorrido_penalizado(self,tsp):
        largo = 0.0
        for i in range(len(self.ruta)):
            largo += self.distancia_penalizada(tsp,(self.ruta)[i],(self.ruta)[(i+1) % len(self.ruta)])
        return largo
    
def costo_recorrido(ruta,tsp):
    largo = 0.0
    for i in range(len(ruta)):
        largo += tsp.distancia_euc((ruta)[i],(ruta)[(i+1) % len(ruta)])
    return largo

 
        
def dos_opt(solucion, tsp):
    # Aplicar el algoritmo 2-opt a la ruta actual
    mejor_mejora = 0
    mejor_ruta = solucion.ruta
    for i in range(len(solucion.ruta) - 1):
        for j in range(i + 2, len(solucion.ruta) - 1):
            nueva_ruta = solucion.ruta[:]
            nueva_ruta[i+1:j+1] = nueva_ruta[j:i:-1]
            nueva_solucion = Solucion()
            nueva_solucion.ruta = nueva_ruta
            nueva_solucion.calcular_costo_recorrido(tsp)
            mejora = solucion.recorrido_total - nueva_solucion.recorrido_total
            if mejora > mejor_mejora:
                mejor_mejora = mejora
                mejor_ruta = nueva_ruta
    solucion.ruta = mejor_ruta
    solucion.calcular_costo_recorrido(tsp)

# def guided_local_search(tsp, max_call_count):
#     print("[Guided Local Search]")
#     contador = 0
#     # generar solucion inicial
#     solucion = Solucion()
#     solucion.ruta = nearest_neighbor(tsp)
#     solucion.calcular_costo_recorrido(tsp)
#     # imprimir solucion inicial
#     print('\n[Initial solution]')
#     print('ruta:\t{}'.format(solucion.ruta))
#     print('recorrido:\t{}'.format(solucion.recorrido_total))
#     # max_call_count
#     while contador < max_call_count:
#         # actualizar penalizaciones
#         # actualizar_penalizacion(tsp,solucion)
#         # aplicar 2-opt
#         dos_opt(solucion, tsp)
#         # imprimir solucion
#         print('\n[Iteration {}]'.format(contador))
#         print('ruta:\t{}'.format(solucion.ruta))
#         print('recorrido:\t{}'.format(solucion.recorrido_total))
#         # actualizar contador
#         contador += 1
#     return solucion
def guided_local_search(tsp, max_call_count):
    print("[Guided Local Search]")
    contador = 0
    # generar solucion inicial
    solucion = Solucion()
    solucion.ruta = nearest_neighbor(tsp)
    solucion.calcular_costo_recorrido(tsp)
    solucion.grado_penalizacion = 5.0
    # imprimir solucion inicial
    print('\n[Initial solution]')
    print('ruta:\t{}'.format(solucion.ruta))
    print('recorrido:\t{}'.format(solucion.recorrido_total))
    # max_call_count
    while contador < max_call_count:
        # actualizar penalizaciones
        # actualizar_penalizacion(tsp,solucion)
        # aplicar 2-opt
        solucion = fast_local_search(tsp, solucion)
        # aplicar penalizaciones
        actualizar_penalizacion(tsp,solucion)
        # mostrar penalizaciones
        print('\n[Penalties]')
        print('penalizaciones:\t{}'.format(solucion.penalizaciones))
        # imprimir solucion
        print('\n[Iteration {}]'.format(contador))
        print('ruta:\t{}'.format(solucion.ruta))
        print('recorrido:\t{}'.format(solucion.recorrido_total))
        # actualizar contador
        contador += 1
    return solucion

def fast_local_search(tsp, solucion_inicial):
    solucion_actual = solucion_inicial
    solucion_actual.calcular_costo_recorrido(tsp)
    mejorado = True
    contador_mejoras = 0  # Contador para las mejoras

    while mejorado and contador_mejoras < 2:
        mejorado = False
        mejor_costo = solucion_actual.recorrido_total

        for i in range(len(solucion_actual.ruta) - 1):
            for j in range(i + 2, len(solucion_actual.ruta) - 1):
                if j - i == 1: continue  # Saltar adyacentes, ya están en la ruta
                nueva_ruta = solucion_actual.ruta[:]
                nueva_ruta[i + 1:j + 1] = nueva_ruta[j:i:-1]  # Realizar intercambio 2-opt
                solucion_temporal = Solucion()
                solucion_temporal.ruta = nueva_ruta
                solucion_temporal.grado_penalizacion = solucion_actual.grado_penalizacion
                nuevo_costo = solucion_temporal.costo_recorrido_penalizado(tsp)  
                if nuevo_costo < mejor_costo:  # Si se encuentra un costo penalizado mejor se actualiza
                    mejor_ruta = nueva_ruta
                    mejor_costo = nuevo_costo
                    mejorado = True

        if mejorado:
            contador_mejoras += 1  # Incrementar el contador de mejoras
            solucion_actual.ruta = mejor_ruta
            solucion_actual.recorrido_total = mejor_costo
            print("Mejora " + str(contador_mejoras) + ": " + str(mejor_costo)
                    + " Ruta: " + str(solucion_actual.ruta))

    return solucion_actual


def nearest_neighbor(tsp):
    num_nodes = tsp.num_nodos
    tour = list(range(num_nodes))  # Crear un tour inicial [0, 1, 2, ..., num_nodes - 1]
    nodo_inicial = random.randint(0, num_nodes - 1)  # Elegir un nodo inicial aleatorio
    route = [nodo_inicial]  # Inicializar la ruta con el nodo inicial aleatorio

    # nearest neighbor
    for i in range(1, num_nodes):
        # Encontrar el nodo no visitado más cercano
        current_node = route[-1]
        min_dist = float('inf')
        arg_min_dist = None
        for j in range(num_nodes):
            if j not in route:
                dist = tsp.distancia_euc(current_node, j)
                if dist < min_dist:
                    min_dist = dist
                    arg_min_dist = j
        # Agregar el nodo no visitado más cercano a la ruta
        route.append(arg_min_dist)
    return route

    
def solucion_inicial(tsp):
    solucion = Solucion()
    # crear sucesion de nodos
    solucion.ruta = list(range(tsp.num_nodos))
    solucion.ruta = random.sample(range(tsp.num_nodos), tsp.num_nodos)
    # calcular recorrido total
    solucion.recorrido_total = solucion.costo_recorrido(tsp)
    return solucion

# Funcion que actualiza las penalizaciones de las aristas del ruta
def actualizar_penalizacion(tsp,solucion):
    max_val = 0.0
    arg_max_val = None
    for i in range(len(solucion.ruta)): # Se recorre el ruta
        v = (solucion.ruta)[i]
        next_v = (solucion.ruta)[(i+1) % len(solucion.ruta)]
        if (v,next_v) in solucion.penalizaciones: # Se evalua si la arista ya tiene penalizaciones
            val = float(tsp.distancia_euc(v,next_v)) / float(1.0 + (solucion.penalizaciones)[v,next_v]) # Se calcula (Ci / 1 + Pi) => util
        else:
            val = float(tsp.distancia_euc(v,next_v)) # Si la arista no tiene penalizaciones se calcula la distancia_euc normal
        if val > max_val:
            max_val = val
            arg_max_val = (v,next_v)
    v, next_v = arg_max_val
    if (v,next_v) in solucion.penalizaciones: # Si la arista ya tiene penalizaciones se aumenta en 1
        (solucion.penalizaciones)[v,next_v] += 1.0
    else:
        (solucion.penalizaciones)[v,next_v] = 1.0 # Si la arista no tiene penalizaciones se crea con valor 1
    if (next_v,v) in solucion.penalizaciones:
        (solucion.penalizaciones)[next_v,v] += 1.0 # Se hace lo mismo para la arista inversa
    else:
        (solucion.penalizaciones)[next_v,v] = 1.0 # Se hace lo mismo para la arista inversa

# def evaluar_mejora(tsp, solucion, u, v, flag):
#     # Se evalua la mejora del ruta con el posible swap de los nodos
#     if flag == 'distancia_penalizada':
#         actual = solucion.distancia_penalizada(tsp,u,solucion.siguiente(u)) + solucion.distancia_penalizada(tsp,v,solucion.siguiente(v))
#         nueva = solucion.distancia_penalizada(tsp,u,v) + solucion.distancia_penalizada(tsp,solucion.siguiente(u),solucion.siguiente(v))
#         return nueva - actual
#     # Se evalua la mejora del ruta con el posible swap de los nodos penalizados
#     else:
#         actual = tsp.distancia_euc(u,solucion.siguiente(u)) + tsp.distancia_euc(v,solucion.siguiente(v))
#         nueva = tsp.distancia_euc(u,v) + tsp.distancia_euc(solucion.siguiente(u),solucion.siguiente(v))
#         return nueva - actual

# def cambiar_ruta(tsp, solucion, u, v):
#     if (solucion.pos)[u] < (solucion.pos)[v]:
#         i, j = (solucion.pos)[u], (solucion.pos)[v]
#     else:
#         i, j = (solucion.pos)[v], (solucion.pos)[u]
#     # reverse sub-path [i+1,...,j]
#     (solucion.ruta)[i+1:j+1] = list(reversed((solucion.ruta)[i+1:j+1]))
#     # actualizar posiciones
#     solucion.definir_pos()
#     # llamar a la FUNCION OBJETIVO para calcular la longitud del ruta
#     solucion.recorrido_total = solucion.largo(tsp)
#     # print("call_count: " + str(solucion.call_count))
        
def main():
    # seed
    random.seed(0)
    # set starting time
    tiempo_inicial = time.time()

    print('GLS for TSP')
    # leer archivo
    tsp = Tsp()
    tsp.leer('./datasets/qa194.tsp')
    tsp.escribir()

    # ruta = nearest_neighbor(tsp)
    # solucion_inicial = Solucion()
    # solucion_inicial.ruta = ruta
    # solucion_inicial.calcular_costo_recorrido(tsp)
    # solucion = fast_local_search(tsp, solucion_inicial)
    # guided local search
    solucion = guided_local_search(tsp, 50)
    # imprimir solucion
    print('\n[Final solution]')
    print('ruta final: \t{}'.format(solucion.ruta))
    print('recorrido final: \t{}'.format(solucion.recorrido_total))

    # set completion time
    end_time = time.time()
    # display computation time
    print('\nTotal time:\t%.3f sec' % (end_time - tiempo_inicial))

if __name__ == "__main__":
    main()