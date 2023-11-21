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

    # generar lista de vecinos  ----------------------------------------
    # Funcion que genera un vecindario de tamaño NB_LIST_SIZE para cada nodo, ordenado de menor a mayor distancia_euc
    def gen_vecindario(self, cantidad_vecinos):
        self.vecinos = [[] for _ in range(self.num_nodos)]
        for i in range(self.num_nodos):
            temp = [(self.distancia_euc(i,j),j) for j in range(self.num_nodos) if j != i]
            temp.sort(key=lambda x: x[0])
            (self.vecinos)[i] = [temp[h][1] for h in range(min(cantidad_vecinos,self.num_nodos))]
        # print("Vecinos: " + str(self.vecinos))


class Firefly:
    # constructor ----------------------------------------------------
    def __init__(self):
        self.ruta = []
        self.recorrido_total = 0.0
        self.intensidad_luz = 0.0
        
    def costo_recorrido(self,tsp):
        largo = 0.0
        for i in range(len(self.ruta)):
            largo += tsp.distancia_euc((self.ruta)[i],(self.ruta)[(i+1) % len(self.ruta)])
        return largo
    
    def generar_aristas(self):
        aristas = [(self.ruta[i], self.ruta[i + 1]) for i in range(len(self.ruta) - 1)]
        return aristas
    
    def distancia_luciernaga(self, luciernaga_j):
        aristas_ruta1 = set(self.generar_aristas())
        aristas_ruta2 = set(luciernaga_j.generar_aristas())
        diferencias = aristas_ruta1.difference(aristas_ruta2)
        cantidad_aristas_distintas = len(diferencias)
        # reverse each edge
        aristas_inversas = set(map(lambda x: (x[1], x[0]), diferencias))
        for arista in aristas_inversas:
            if arista in aristas_ruta2:
                cantidad_aristas_distintas -= 1
        distancia = (cantidad_aristas_distintas/len(self.ruta))*10
        return distancia

    def calcular_atraccion(self, luciernaga_j, coef_absorcion):
        brillo_luciernaga_j = luciernaga_j.intensidad_luz
        distancia = self.distancia_luciernaga(luciernaga_j)
        atraccion = brillo_luciernaga_j * math.exp(-coef_absorcion * math.pow(distancia,2))
        return atraccion
    
    def obtener_luciernaga_mas_atractiva(self, poblacion, coef_absorcion):
        luciernaga_mas_atractiva = None
        max_atraccion = 0
        for luciernaga in poblacion:
            if luciernaga != self:
                atraccion = self.calcular_atraccion(luciernaga, coef_absorcion)
                if atraccion > max_atraccion:
                    max_atraccion = atraccion
                    luciernaga_mas_atractiva = luciernaga
        return luciernaga_mas_atractiva

def generar_poblacion_inicial(tsp, cant_luciernagas):
    poblacion = [Firefly(tsp) for _ in range(cant_luciernagas)]
    for i in range(cant_luciernagas):
        poblacion[i].ruta = random.sample(range(tsp.num_nodos), tsp.num_nodos)
        # poblacion[i].pos = [i for i in range(tsp.num_nodos)]
        poblacion[i].recorrido_total = poblacion[i].costo_recorrido(tsp)
        poblacion[i].intensidad_luz = 1.0 / poblacion[i].recorrido_total
    return poblacion

# def mutacion_inversa(tsp, luciernaga, m_luciernagas, cant_aristas_diferentes):
#     luciernagas = []
#     copia_ruta = luciernaga.ruta
    
#     for _ in range(m_luciernagas):
#         inicio = random.randint(0, len(copia_ruta) - 1)
#         longitud_seccion = round(random.uniform(2, cant_aristas_diferentes))
#         fin = min(inicio + longitud_seccion, len(copia_ruta))
        
#         seccion_reversa = copia_ruta[inicio:fin]
#         seccion_reversa.reverse()
#         nueva_luciernaga = Firefly(tsp)
#         nueva_luciernaga.ruta = copia_ruta[:inicio] + seccion_reversa + copia_ruta[fin:]
#         luciernagas.append(nueva_luciernaga)
#     return luciernagas

# Movimiento cuando hay luciernaga mas atractiva
def mutacion_inversa_movimiento(tsp,luciernaga, distancia):
    copia_ruta = luciernaga.ruta[:]  # Crear una copia de la ruta de la luciérnaga
    inicio = random.randint(0, len(copia_ruta) - distancia)  # Asegurar que hay espacio para una sección de tamaño distancia
    print("Inicio: " + str(inicio))
    fin = inicio + distancia
    print("Fin: " + str(fin))
    seccion_reversa = copia_ruta[inicio:fin][::-1]  # Invertir la sección de tamaño distancia seleccionada
    nueva_ruta = copia_ruta[:inicio] + seccion_reversa + copia_ruta[fin:]
    nueva_luciernaga = Firefly()  # Suponiendo que tienes una clase Firefly para manejar las luciérnagas
    nueva_luciernaga.ruta = nueva_ruta
    nueva_luciernaga.recorrido_total = nueva_luciernaga.costo_recorrido(tsp)
    nueva_luciernaga.intensidad_luz = 1.0 / nueva_luciernaga.recorrido_total
    return nueva_luciernaga

# Movimiento cuando no hay luciernaga mas atractiva
def mutacion_inversa_random(tsp, luciernaga, tamano_seccion_m):
    copia_ruta = luciernaga.ruta[:]  # Crear una copia de la ruta de la luciérnaga
    inicio = random.randint(0, len(copia_ruta) - tamano_seccion_m)  # Asegurar que hay espacio para una sección de tamaño 3
    fin = inicio + tamano_seccion_m
    seccion_reversa = copia_ruta[inicio:fin][::-1]  # Invertir la sección de tamaño 3 seleccionada
    nueva_ruta = copia_ruta[:inicio] + seccion_reversa + copia_ruta[fin:]
    nueva_luciernaga = Firefly()  # Suponiendo que tienes una clase Firefly para manejar las luciérnagas
    nueva_luciernaga.ruta = nueva_ruta
    nueva_luciernaga.recorrido_total = nueva_luciernaga.costo_recorrido(tsp)
    nueva_luciernaga.intensidad_luz = 1.0 / nueva_luciernaga.recorrido_total
    return nueva_luciernaga

def DFA(tsp, cant_luciernagas, max_call_objetive_function, coef_absorcion, tamano_seccion_m):
    print("\n[ DFA Algoritm ]")
    contador_llamados = 0
    poblacion_temporal = []
    historial = []

    # Generar luciernagas iniciales
    poblacion = generar_poblacion_inicial(tsp, cant_luciernagas)
    contador_llamados += cant_luciernagas
    poblacion_temporal = poblacion
   
    # Iterar hasta que se cumpla el criterio de parada
    while contador_llamados < max_call_objetive_function:
        for luciernaga in poblacion:
            luciernaga_mas_atractiva = luciernaga.obtener_luciernaga_mas_atractiva(poblacion, coef_absorcion)
            # Si hay luciernaga mas atractiva
            if luciernaga_mas_atractiva != None:
                print("Luciernaga actual: " + str(luciernaga.ruta) + " - " + str(luciernaga.recorrido_total) + " - " + str(luciernaga.intensidad_luz))
                print("Luciernaga mas atractiva: " + str(luciernaga_mas_atractiva.ruta) + " - " + str(luciernaga_mas_atractiva.recorrido_total) + " - " + str(luciernaga_mas_atractiva.intensidad_luz))

                # calcular distancia
                distancia = luciernaga.distancia_luciernaga(luciernaga_mas_atractiva)
                print("Distancia: " + str(distancia))

                # Mover luciernaga
                nueva_luciernaga = mutacion_inversa_movimiento(luciernaga, distancia)
                print("Nueva luciernaga: " + str(nueva_luciernaga))

                # Actualizar intensidad de luz
                for nueva_luciernaga in nuevas_luciernagas:
                    nueva_luciernaga.recorrido_total = nueva_luciernaga.costo_recorrido(tsp)
                    nueva_luciernaga.intensidad_luz = 1.0 / nueva_luciernaga.recorrido_total
                    # print("Luciernaga actualizada: " + str(nueva_luciernaga.ruta) + " - " + str(nueva_luciernaga.recorrido_total) + " - " + str(nueva_luciernaga.intensidad_luz))
                    # Agregar luciernaga a poblacion temporal
                    poblacion_temporal.append(nueva_luciernaga)
                    contador_llamados += 1
                poblacion_temporal.append(luciernaga)

            else:
                print("Luciernaga actual: " + str(luciernaga.ruta) + " - " + str(luciernaga.recorrido_total) + " - " + str(luciernaga.intensidad_luz))
                print("No hay luciernaga mas atractiva")
                nueva_luciernaga = mutacion_inversa_variable(tsp, luciernaga, 4)
                nueva_luciernaga.recorrido_total = nueva_luciernaga.costo_recorrido(tsp)
                nueva_luciernaga.intensidad_luz = 1.0 / nueva_luciernaga.recorrido_total
                # print("Luciernaga actualizada: " + str(nueva_luciernaga.ruta) + " - " + str(nueva_luciernaga.recorrido_total) + " - " + str(nueva_luciernaga.intensidad_luz))
                # Agregar luciernaga a poblacion temporal
                poblacion_temporal.append(nueva_luciernaga)
                contador_llamados += 1
                # poblacion_temporal.append(luciernaga) 
            # break
            # seleccionar mejores luciernagas
            poblacion_temporal.sort(key=lambda x: x.recorrido_total)
            poblacion_temporal = poblacion_temporal[:cant_luciernagas]
            poblacion = poblacion_temporal
            historial.append(poblacion[0].recorrido_total)
    
    # graficar historial
    plt.plot(historial)
    plt.ylabel('Costo')
    plt.xlabel('Iteraciones')
    plt.show()
    return poblacion
                

def main():
    # set random seed
    # random.seed(1)

    # set starting time
    tiempo_inicial = time.time()

    # leer instancia TSP
    tsp = Tsp()
    tsp.leer("./datasets/wi29.tsp")
    tsp.escribir()

    luciernaga = Firefly()
    luciernaga.ruta = [0, 1, 2, 3, 4, 5, 6]
    nueva_luciernaga = mutacion_inversa_movimiento(luciernaga, 3)
    print("Luciernaga: " + str(luciernaga.ruta))
    print("Nueva luciernaga: " + str(nueva_luciernaga.ruta))

    # cant_luciernagas = 100
    # max_call_objetive_function = 50000
    # coef_absorcion = 0.0001
    # # coef_absorcion = 0.001
    # # coef_absorcion = 0.1
    # tamano_seccion_m = 5

    # # Llamada DFA
    # poblacion = DFA(tsp, cant_luciernagas, max_call_objetive_function, coef_absorcion, tamano_seccion_m)
    # print("Poblacion final: ")
    # for i in range(cant_luciernagas):
    #     print("Luciernaga " + str(i) + ": " + str(poblacion[i].ruta) + " - " + str(poblacion[i].recorrido_total) + " - " + str(poblacion[i].intensidad_luz))
    # print("Contador llamados: " + str(max_call_objetive_function))

    # luciernaga = Firefly(tsp)
    # luciernaga.ruta = [0, 1, 2, 3, 4]
    # luciernaga.pos = [0, 1, 2, 3, 4]
    # luciernaga.recorrido_total = luciernaga.costo_recorrido(tsp)
    # luciernaga.intensidad_luz = 1.0 / luciernaga.recorrido_total







    # poblacion, contador = generar_poblacion_inicial(tsp, cant_luciernagas, 0)
    # # Imprimir poblacion
    # for i in range(cant_luciernagas):
    #     print("Luciernaga " + str(i) + ": " + str(poblacion[i].ruta) + " - " + str(poblacion[i].recorrido_total) + " - " + str(poblacion[i].intensidad_luz))
    # obtener luciernaga mas atractiva para luciernaga 3
    # luciernaga = poblacion[3]
    # luciernaga_mas_atractiva = luciernaga.obtener_luciernaga_mas_atractiva(poblacion, coef_absorcion)


    # set completion time
    end_time = time.time()
    # display computation time
    print('\nTotal time:\t%.3f sec' % (end_time - tiempo_inicial))

if __name__ == "__main__":
    main()

    # # DATASETS OPTIMUM VALUES
    # qa194 = 9352
    # wi29 = 27603
    # dj38 = 6656
    # uy734 = 79114
    # zi929 = 95345
    # lu980 = 11340