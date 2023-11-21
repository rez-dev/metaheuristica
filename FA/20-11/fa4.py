# FA ALGORITHM FOR TSP
# Rodrigo Escobar Zamorano

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

    # generar lista de vecinos  ----------------------------------------
    # Funcion que genera un vecindario de tamaño NB_LIST_SIZE para cada nodo, ordenado de menor a mayor distancia_euc
    def gen_vecindario(self, cantidad_vecinos=5):
        self.vecinos = [[] for _ in range(self.num_nodos)]
        for i in range(self.num_nodos):
            temp = [(self.distancia_euc(i,j),j) for j in range(self.num_nodos) if j != i]
            temp.sort(key=lambda x: x[0])
            (self.vecinos)[i] = [temp[h][1] for h in range(min(cantidad_vecinos,self.num_nodos))]
        # print("Vecinos: " + str(self.vecinos))


class Firefly:
    # constructor ----------------------------------------------------
    def __init__(self, tsp):
        self.ruta = []  # ruta del firefly
        self.pos = []  # posiciones de las ciudades en la ruta
        # self.recorrido_total = self.costo_recorrido(tsp)
        self.recorrido_total = 0.0
        # self.intensidad_luz = 1.0 / self.recorrido_total
        self.intensidad_luz = 0.0
        
    def costo_recorrido(self,tsp):
        largo = 0.0
        # self.call_count += 1
        for i in range(len(self.ruta)):
            largo += tsp.distancia_euc((self.ruta)[i],(self.ruta)[(i+1) % len(self.ruta)])
        return largo
    
    def generar_aristas(self):
        aristas = [(self.ruta[i], self.ruta[i + 1]) for i in range(len(self.ruta) - 1)]
        return aristas
    
    def distancia_luciernaga(self, luciernaga):
        aristas_ruta1 = set(self.generar_aristas())
        aristas_ruta2 = set(luciernaga.generar_aristas())
        diferencias = aristas_ruta1.difference(aristas_ruta2)
        cantidad_aristas_distintas = len(diferencias)
        # reverse each edge
        aristas_inversas = set(map(lambda x: (x[1], x[0]), diferencias))
        for arista in aristas_inversas:
            if arista in aristas_ruta2:
                cantidad_aristas_distintas -= 1
        distancia = (cantidad_aristas_distintas/len(self.ruta))*10
        return distancia

    def calcular_atraccion(self, luciernaga, brillo_luciernagaB, coef_absorcion):
        distancia = self.distancia_luciernaga(luciernaga)
        atraccion = brillo_luciernagaB * math.exp(-coef_absorcion * math.pow(distancia,2))
        return atraccion
    
    def obtener_luciernaga_mas_atractiva(self, poblacion, coef_absorcion):
        print("[ Obtener luciernaga mas atractiva ]")
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
    

def generar_poblacion_inicial(tsp, cant_luciernagas, contador_llamados):
    print("[ Generar soluciones iniciales ]")
    copia_contador = contador_llamados
    poblacion = [Firefly(tsp) for _ in range(cant_luciernagas)]
    for i in range(cant_luciernagas):
        poblacion[i].ruta = random.sample(range(tsp.num_nodos), tsp.num_nodos)
        poblacion[i].pos = [i for i in range(tsp.num_nodos)]
        poblacion[i].recorrido_total = poblacion[i].costo_recorrido(tsp)
        poblacion[i].intensidad_luz = 1.0 / poblacion[i].recorrido_total
        copia_contador += 1
    return poblacion, copia_contador
import random

def costo_recorrido(luciernaga,tsp):
    largo = 0.0
    # self.call_count += 1
    for i in range(len(luciernaga.ruta)):
        largo += tsp.distancia_euc((luciernaga.ruta)[i],(luciernaga.ruta)[(i+1) % len(luciernaga.ruta)])
    return largo

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


def generar_luciernagas_nn(tsp, n, contador_llamados):
    luciernagas = []
    for _ in range(n):
        ruta = nearest_neighbor(tsp)
        luciernaga = Firefly(tsp)
        luciernaga.ruta = ruta
        luciernaga.recorrido_total = luciernaga.costo_recorrido(tsp)
        luciernaga.intensidad_luz = 1.0 / luciernaga.recorrido_total
        luciernagas.append(luciernaga)
    contador_llamados += n
    return luciernagas, contador_llamados

def mutacion_inversa(tsp, luciernaga, m_luciernagas, cant_aristas_diferentes):
    print("[ Mutacion inversa ]")
    luciernagas = []
    copia_ruta = luciernaga.ruta
    
    for _ in range(m_luciernagas):
        inicio = random.randint(0, len(copia_ruta) - 1)
        longitud_seccion = round(random.uniform(2, cant_aristas_diferentes))
        fin = min(inicio + longitud_seccion, len(copia_ruta))
        
        seccion_reversa = copia_ruta[inicio:fin]
        seccion_reversa.reverse()
        nueva_luciernaga = Firefly(tsp)
        nueva_luciernaga.ruta = copia_ruta[:inicio] + seccion_reversa + copia_ruta[fin:]
        luciernagas.append(nueva_luciernaga)
    return luciernagas

def mutacion_inversa_variable(tsp, luciernaga, tamano_seccion):
    print("[ Mutacion inversa variable ]")
    copia_ruta = luciernaga.ruta[:]  # Crear una copia de la ruta de la luciérnaga
    inicio = random.randint(0, len(copia_ruta) - tamano_seccion)  # Asegurar que hay espacio para una sección de tamaño 3
    fin = inicio + tamano_seccion
    seccion_reversa = copia_ruta[inicio:fin][::-1]  # Invertir la sección de tamaño 3 seleccionada
    nueva_ruta = copia_ruta[:inicio] + seccion_reversa + copia_ruta[fin:]
    nueva_luciernaga = Firefly(tsp)  # Suponiendo que tienes una clase Firefly para manejar las luciérnagas
    nueva_luciernaga.ruta = nueva_ruta
    return nueva_luciernaga

def generar_mejores_luciernagas(tsp, n, contador_llamados):
    print("[ Generar mejores soluciones ]")
    poblacion = []
    for _ in range(n):
        mejor_vecino = None
        mejor_costo = float('inf')
        # Generar una ruta aleatoria inicial para la luciérnaga
        ruta_inicial = list(range(tsp.num_nodos))
        random.shuffle(ruta_inicial)
        # Intentar mejorar la ruta utilizando el mejor vecino
        for i in range(tsp.num_nodos - 1):
            for j in range(i + 1, tsp.num_nodos):
                # Intercambiar dos nodos para obtener un vecino
                vecino = ruta_inicial[:]
                vecino[i], vecino[j] = vecino[j], vecino[i]
                
                # Calcular el costo del vecino utilizando la función de distancia del TSP
                costo_vecino = sum(tsp.distancia_euc(vecino[k], vecino[k + 1]) for k in range(tsp.num_nodos - 1))
                costo_vecino += tsp.distancia_euc(vecino[-1], vecino[0])  # Agregar el costo del último al primer nodo
                
                # Actualizar el mejor vecino y su costo si es mejor que el anterior
                if costo_vecino < mejor_costo:
                    mejor_vecino = vecino[:]
                    mejor_costo = costo_vecino
        # Crear una luciérnaga con la mejor ruta encontrada
        luciernaga = Firefly(tsp)  # Suponiendo que tienes una clase Firefly para manejar las luciérnagas
        luciernaga.ruta = mejor_vecino
        luciernaga.recorrido_total = mejor_costo
        luciernaga.intensidad_luz = 1.0 / mejor_costo
        poblacion.append(luciernaga)
    contador_llamados += n
    return poblacion, contador_llamados


def DFA(tsp, cant_luciernagas, max_call_objetive_function, coef_absorcion, indice_actualizacion, tamano_seccion):
    print("\n[ DFA Algoritm ]")
    contador_llamados = 0
    poblacion_temporal = []
    historial = []

    # Generar luciernagas iniciales
    poblacion, contador_llamados = generar_luciernagas_nn(tsp, cant_luciernagas, contador_llamados)
    # poblacion, contador_llamados = generar_poblacion_inicial(tsp, cant_luciernagas, contador_llamados)
    # poblacion, contador_llamados = generar_mejores_luciernagas(tsp, cant_luciernagas, contador_llamados)
    # Imprimir luciernagas iniciales
    # for i in range(cant_luciernagas):
    #     print("Luciernaga " + str(i) + ": " + str(poblacion[i].ruta) + " - " + str(poblacion[i].recorrido_total) + " - " + str(poblacion[i].intensidad_luz)) 
    # print("Contador llamados: " + str(contador_llamados))
    poblacion_temporal = poblacion
   
    # Iterar hasta que se cumpla el criterio de parada
    while contador_llamados < max_call_objetive_function:
        # break
        # print("Llamados " + str(contador_llamados))
        # Obtener luciernaga mas atractiva para cada luciernaga
        for luciernaga in poblacion:
            luciernaga_mas_atractiva = luciernaga.obtener_luciernaga_mas_atractiva(poblacion, coef_absorcion)
            if luciernaga_mas_atractiva != None:
                # print("Luciernaga actual: " + str(luciernaga.ruta) + " - " + str(luciernaga.recorrido_total) + " - " + str(luciernaga.intensidad_luz))
                # print("Luciernaga mas atractiva: " + str(luciernaga_mas_atractiva.ruta) + " - " + str(luciernaga_mas_atractiva.recorrido_total) + " - " + str(luciernaga_mas_atractiva.intensidad_luz))

                # calcular distancia
                distancia = luciernaga.distancia_luciernaga(luciernaga_mas_atractiva)
                # print("Distancia: " + str(distancia))

                # Mover luciernaga
                nuevas_luciernagas = mutacion_inversa(tsp, luciernaga, indice_actualizacion, distancia)
                # print("Nuevas luciernagas: " + str(nuevas_luciernagas))
                # Actualizar intensidad de luz
                for nueva_luciernaga in nuevas_luciernagas:
                    nueva_luciernaga.recorrido_total = nueva_luciernaga.costo_recorrido(tsp)
                    nueva_luciernaga.intensidad_luz = 1.0 / nueva_luciernaga.recorrido_total
                    # print("Luciernaga nueva: " + str(nueva_luciernaga.ruta) + " - " + str(nueva_luciernaga.recorrido_total) + " - " + str(nueva_luciernaga.intensidad_luz))
                    # Agregar luciernaga a poblacion temporal
                    poblacion_temporal.append(nueva_luciernaga)
                    contador_llamados += 1
                poblacion_temporal.append(luciernaga)

            else:
                # print("Luciernaga actual: " + str(luciernaga.ruta) + " - " + str(luciernaga.recorrido_total) + " - " + str(luciernaga.intensidad_luz))
                # print("No hay luciernaga mas atractiva")
                nueva_luciernaga = mutacion_inversa_variable(tsp, luciernaga, tamano_seccion)
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
            # print("Mejor ruta: " + str(poblacion[0].ruta) + " - " + str(poblacion[0].recorrido_total) + " - " + str(poblacion[0].intensidad_luz))
            print("                                 Mejor costo: " + str(poblacion[0].recorrido_total))
    
    # # graficar historial
    plt.plot(historial)
    plt.ylabel('Costo')
    plt.xlabel('Iteraciones')
    plt.show()
    return poblacion

def objective(trial):
    # Define los rangos para los hiperparámetros que quieres optimizar
    cant_luciernagas = trial.suggest_int('cant_luciernagas', 50, 200)
    # max_call_objetive_function = trial.suggest_int('max_call_objetive_function', 10000, 100000)
    coef_absorcion = trial.suggest_float('coef_absorcion', 0.00001, 0.1)
    indice_actualizacion = trial.suggest_int('indice_actualizacion', 1, 10)
    tamano_seccion = trial.suggest_int('tamano_seccion', 2, 10)

    # leer tsp
    tsp = Tsp()
    tsp.leer("./datasets/wi29.tsp")
    tsp.escribir()
    
    # Crear una instancia de DFA con los parámetros optimizados
    poblacion = DFA(tsp, cant_luciernagas, 5000, coef_absorcion, indice_actualizacion, tamano_seccion)
    
    # Ejecutar tu función de objetivo con la población creada
    result = costo_recorrido(poblacion[0], tsp)  # Reemplaza 'your_objective_function' con tu función de objetivo
    
    return result

def correr_optuna():
    # Ejecutar la optimización con Optuna
    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=100)  # Cambia 'n_trials' al número deseado de intentos de optimización

    # Obtener los mejores parámetros encontrados
    best_params = study.best_params
    print("Mejores parámetros:", best_params)

def es_solucion_valida(solucion, cantidad_nodos):
    # Verificar si la solución contiene todos los números de 0 hasta cantidad de nodos - 1
    numeros_esperados = set(range(cantidad_nodos))
    if set(solucion) != numeros_esperados:
        return False
    
    # Verificar si el tamaño de la solución es igual a la cantidad de nodos
    if len(solucion) != cantidad_nodos:
        return False
    
    # Verificar si no hay números repetidos en la solución
    if len(solucion) != len(set(solucion)):
        return False
    
    return True

def main():
    # set random seed
    random.seed(1)

    # set starting time
    tiempo_inicial = time.time()

    # leer instancia TSP
    tsp = Tsp()
    tsp.leer("./datasets/wi29.tsp")
    tsp.escribir()

    # Mejores variables
    cant_luciernagas = 140
    coef_absorcion = 0.0888790460875098
    # coef_absorcion = 0.0001

    indice_actualizacion = 2
    tamano_seccion = 8
    max_call_objetive_function = 20000

    # FA
    poblacion = DFA(tsp, cant_luciernagas, max_call_objetive_function, coef_absorcion, indice_actualizacion, tamano_seccion)

    # set completion time
    end_time = time.time()
    # display computation time
    print('\nTotal time:\t%.3f sec' % (end_time - tiempo_inicial))



if __name__ == "__main__":
    main()
    # correr_optuna()

    # # DATASETS OPTIMUM VALUES
    # qa194 = 9352
    # wi29 = 27603
    # dj38 = 6656
    # uy734 = 79114
    # zi929 = 95345
    # lu980 = 11340