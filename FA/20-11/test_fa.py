# FA ALGORITHM FOR TSP
# Rodrigo Escobar Zamorano

import math
import random
import sys
import time

from matplotlib import pyplot as plt


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


class Firefly:
    # constructor ----------------------------------------------------
    def __init__(self):
        self.ruta = []
        self.costo = 0.0
        self.intensidad_luz = 0.0
    
    def copy(self):
        new_firefly = Firefly(None)
        new_firefly.ruta = self.ruta.copy()
        new_firefly.costo = self.costo
        new_firefly.intensidad_luz = self.intensidad_luz
        return new_firefly
        
    def costo_recorrido(self,tsp):
        largo = 0.0
        # self.call_count += 1
        for i in range(len(self.ruta)):
            largo += tsp.distancia_euc((self.ruta)[i],(self.ruta)[(i+1) % len(self.ruta)])
        return largo

    def calcular_intensidad_luz(self):
        intensidad_luz = 1 / self.costo
        return intensidad_luz
    
    def generar_aristas(self):
        aristas = [(self.ruta[i], self.ruta[i + 1]) for i in range(len(self.ruta) - 1)]
        return aristas
    
    # def distancia_luciernagas(self, luciernaga2):
    #     aristas_ruta1 = set(self.ruta)
    #     aristas_ruta2 = set(luciernaga2.ruta)
    #     diferencias = aristas_ruta1.difference(aristas_ruta2)
    #     cantidad_aristas_distintas = len(diferencias)
    #     # reverse each edge
    #     # aristas_inversas = set(map(lambda x: (x[1], x[0]), diferencias))
    #     # for arista in aristas_inversas:
    #     #     if arista in aristas_ruta2:
    #     #         cantidad_aristas_distintas -= 1
    #     return cantidad_aristas_distintas
    
    def distancia_swap(self, luciernaga_j):  
        ruta_self = self.ruta[:]  # Copia de la ruta de self
        ruta_j = luciernaga_j.ruta[:]  # Copia de la ruta de luciernaga_j
        # Creamos un diccionario para almacenar el índice de cada elemento en la otra ruta
        index_map = {val: i for i, val in enumerate(ruta_j)}
        distance = 0
        for i in range(len(ruta_self)):
            if ruta_self[i] != ruta_j[i]:
                # Buscamos el índice del elemento en la otra ruta que corresponde al elemento en ruta_self[i]
                idx = index_map[ruta_self[i]]
                # Intercambiamos los elementos en la ruta_j para que coincidan con ruta_self
                ruta_j[i], ruta_j[idx] = ruta_j[idx], ruta_j[i]
                # Actualizamos el índice del elemento movido en la ruta_j
                index_map[ruta_j[idx]] = idx
                # Incrementamos la distancia
                distance += 1
        return distance

    def distancia_hamming(self, luciernaga_j):    
        distancia = 0
        indices_diferencias = []
        for i in range(len(self.ruta)):
            if self.ruta[i] != luciernaga_j.ruta[i]:
                distancia += 1
                indices_diferencias.append(1)
            else:
                indices_diferencias.append(0)
        return distancia, indices_diferencias

    def calcular_atraccion(self, luciernaga, brillo_luciernagaB, coef_absorcion):
        distancia, _ = self.distancia_hamming(luciernaga)
        atraccion = brillo_luciernagaB * math.exp(-coef_absorcion * math.pow(distancia,2))
        return atraccion
    
    # def calcular_intensidad_luz(self, luciernaga_j, )
    
    def obtener_luciernaga_mas_atractiva(self, poblacion, coef_absorcion):
        luciernaga_mas_atractiva = None
        brillo_luciernaga_mas_atractiva = 0.0
        for luciernaga in poblacion:
            if luciernaga != self:
                brillo_luciernagaB = luciernaga.intensidad_luz
                atraccion = self.calcular_atraccion(luciernaga, brillo_luciernagaB, coef_absorcion)
                # print("Atraccion: " + str(atraccion))
                if atraccion > self.intensidad_luz:
                    luciernaga_mas_atractiva = luciernaga
                    # brillo_luciernaga_mas_atractiva = atraccion
                    # print("Ruta: " + str(self.ruta) +" Atraccion mayor " + str(atraccion) + " > " + str(self.intensidad_luz))
        # print("Luciernaga actual: " + str(self.ruta) + " - " + str(self.recorrido_total) + " - " + str(self.intensidad_luz))
        # if luciernaga_mas_atractiva != None:
        #     print("Luciernaga mas atractiva: " + str(luciernaga_mas_atractiva.ruta) + " - " + str(luciernaga_mas_atractiva.recorrido_total) + " - " + str(luciernaga_mas_atractiva.intensidad_luz))
        # else:
        #     print("No hay luciernaga mas atractiva")
            
        return luciernaga_mas_atractiva

    def mutacion_inversa(self, distancia_luciernaga):
        largo_mutacion = random.randint(1, distancia_luciernaga)
        # print("Largo mutacion: " + str(largo_mutacion))
        largo_maximo = len(self.ruta) - largo_mutacion
        # print("Largo maximo: " + str(largo_maximo))
        inicio_mutacion = random.randint(0, largo_maximo - 1)
        fin_mutacion = inicio_mutacion + largo_mutacion
        ruta_mutada = self.ruta[:]
        ruta_mutada = ruta_mutada[:inicio_mutacion] + list(reversed(ruta_mutada[inicio_mutacion:fin_mutacion])) + ruta_mutada[fin_mutacion:]
        # print("Ruta mutada: " + str(ruta_mutada))
        lucierna_mutada = Firefly()
        lucierna_mutada.ruta = ruta_mutada
        return lucierna_mutada

    def mover_luciernaga(self, luciernaga_j, distancia_luciernaga):
        print("[ Mover ]")
        cantidad_swap = random.randint(1, distancia_luciernaga)
        # print("Cantidad swap: " + str(cantidad_swap))
        distancia, indices_diferencias = self.distancia_hamming(luciernaga_j)
        # print("Distancia: " + str(distancia))
        # print("Indices diferencias: " + str(indices_diferencias))
        while cantidad_swap > 0:
            # recalcular distancia
            distancia, indices_diferencias = self.distancia_hamming(luciernaga_j)
            # print("Distancia: " + str(distancia))
            # print("Indices diferencias: " + str(indices_diferencias))
            # indice random
            indices_with_difference = [i for i, val in enumerate(indices_diferencias) if val]
            random_index = random.choice(indices_with_difference)
            value_to_copy = luciernaga_j.ruta[random_index]
            # print("Indice random: " + str(random_index))
            # print("Valor a copiar: " + str(value_to_copy))
            index_to_move = next((i for i, val in enumerate(self.ruta) if val == value_to_copy), None)
            if cantidad_swap == 1 and self.ruta[index_to_move] == luciernaga_j.ruta[random_index] and self.ruta[random_index] == luciernaga_j.ruta[index_to_move]:
                break
            self.ruta[random_index], self.ruta[index_to_move] = self.ruta[index_to_move], self.ruta[random_index]
            if self.ruta[index_to_move] == luciernaga_j.ruta[index_to_move]:
                cantidad_swap -= 1
            cantidad_swap -= 1
        print("Ruta: " + str(self.ruta))

def generar_poblacion_inicial(tsp, tamano_poblacion):
    poblacion = []
    for i in range(tamano_poblacion):
        luciernaga = Firefly()
        luciernaga.ruta = list(range(1, tsp.num_nodos))
        random.shuffle(luciernaga.ruta)
        luciernaga.costo = luciernaga.costo_recorrido(tsp)
        luciernaga.calcular_intensidad_luz()
        poblacion.append(luciernaga)
    return poblacion

def two_opt(luciernaga, tsp, num_attempts=5):
    improved = False
    best_luciernaga = luciernaga
    for attempt in range(num_attempts):
        current_route = best_luciernaga.ruta[:]
        for i in range(len(current_route) - 1):
            for j in range(i + 1, len(current_route)):
                new_route = current_route[:i] + current_route[i:j + 1][::-1] + current_route[j + 1:]
                # Calcula el costo de la nueva ruta utilizando la función de costo del TSP
                new_cost = sum(tsp.distancia_euc(new_route[k], new_route[k + 1]) for k in range(len(new_route) - 1))
                new_cost += tsp.distancia_euc(new_route[-1], new_route[0])  # Agrega el costo del último al primer nodo     
                # Si la nueva ruta es mejor, actualiza la ruta de la luciérnaga y el costo
                if new_cost < best_luciernaga.costo:
                    best_luciernaga.ruta = new_route[:]
                    best_luciernaga.costo = new_cost
                    improved = True
        if not improved:
            break  # Si no hay mejora, termina los intentos
    return best_luciernaga  # Devuelve la luciérnaga mejorada o igual si no se logra mejorar



def FA(tsp, max_call_count, tamano_poblacion, coef_absorcion):
    print("[ FA Algorithm ]")
    contador_llamados = 0
    poblacion_temporal = []
    historial = []
    # generar poblacion inicial
    poblacion = generar_poblacion_inicial(tsp, tamano_poblacion)
    contador_llamados += tamano_poblacion
    while contador_llamados < max_call_count:
        for luciernaga in poblacion:
            # print("Ruta: " + str(luciernaga.ruta) + " - " + str(luciernaga.costo))
            # obtener lucieraga mas atractiva
            luciernaga_mas_atractiva = luciernaga.obtener_luciernaga_mas_atractiva(poblacion, coef_absorcion)
            if luciernaga_mas_atractiva != None:
                # mover luciernaga
                luciernaga.mover_luciernaga(luciernaga_mas_atractiva, luciernaga.distancia_swap(luciernaga_mas_atractiva))
                luciernaga.costo = luciernaga.costo_recorrido(tsp)
                luciernaga.intensidad_luz = luciernaga.calcular_intensidad_luz()
                print("Luciernaga mas atractiva: " + str(luciernaga_mas_atractiva.ruta) + " - " + str(luciernaga_mas_atractiva.costo) + " - " + str(luciernaga_mas_atractiva.intensidad_luz))
                # print("Ruta: " + str(luciernaga.ruta) + " - " + str(luciernaga.costo) + " - " + str(luciernaga.intensidad_luz))
                # agregar luciernaga a poblacion temporal
                poblacion_temporal.append(luciernaga)
                contador_llamados += 1
                # historial.append(luciernaga.costo)
            else:
                print("No hay luciernaga mas atractiva")
                # mover random
                luciernaga.mutacion_inversa(random.randint(1, 5))
                luciernaga.costo = luciernaga.costo_recorrido(tsp)
                luciernaga.intensidad_luz = luciernaga.calcular_intensidad_luz()
                poblacion_temporal.append(luciernaga)
                historial.append(luciernaga.costo)
        
        # seleccionar mejores luciernagas
        poblacion_temporal.sort(key=lambda x: x.costo)
        poblacion_temporal = poblacion_temporal[:tamano_poblacion]
        historial.append(poblacion[0].costo)
        # actualizar poblacion
        poblacion = poblacion_temporal.copy()
        poblacion_temporal.clear()
        print("contador_llamados: " + str(contador_llamados))
    return poblacion


def main():
    print("[ Main ]")
    tiempo_inicial = time.time()

    # leer instancia TSP
    tsp = Tsp()
    # tsp.leer("./datasets/dj38.tsp")
    tsp.leer("./datasets/qa194.tsp")
    # tsp.leer(nombre_entrada)
    tsp.escribir()

    # generar poblacion inicial
    poblacion = generar_poblacion_inicial(tsp, 1)

    # variables
    max_call_count = 10
    tamano_poblacion = 2
    coef_absorcion = 0.0001

    # FA
    poblacion = FA(tsp, max_call_count, tamano_poblacion, coef_absorcion)





    # set completion time
    end_time = time.time()
    # display computation time
    print('\nTotal time:\t%.3f sec' % (end_time - tiempo_inicial))

if __name__ == "__main__":
    main()  