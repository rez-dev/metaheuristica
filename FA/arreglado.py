# FA ALGORITHM FOR TSP
# Rodrigo Escobar Zamorano

import copy
import math
import random
import sys
import time

from matplotlib import pyplot as plt
import numpy as np
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
        self.pos = []
        self.recorrido_total = 0.0
        self.intensidad_luz = 0.0
        
    def costo_recorrido(self,tsp):
        largo = 0.0
        for i in range(len(self.ruta)):
            largo += tsp.distancia_euc((self.ruta)[i],(self.ruta)[(i+1) % len(self.ruta)])
        return largo
    
    def copiar(self):
        copia = Firefly()
        copia.ruta = self.ruta[:]
        copia.recorrido_total = self.recorrido_total
        copia.intensidad_luz = self.intensidad_luz
        copia.pos = self.pos[:]
        return copia
    
    def generar_aristas(self):
        aristas = [(self.ruta[i], self.ruta[i + 1]) for i in range(len(self.ruta) - 1)]
        return aristas

    # distancia entre luciernagas con hamming
    def distancia_luciernaga(self, luciernaga_j):
        distancia = 0
        for i in range(len(self.ruta)):
            if self.ruta[i] != luciernaga_j.ruta[i]:
                distancia += 1
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
                # print("Atraccion: " + str(atraccion))
                if atraccion > self.intensidad_luz:
                    if atraccion > max_atraccion:
                        max_atraccion = atraccion
                        luciernaga_mas_atractiva = luciernaga.copiar()
        return luciernaga_mas_atractiva
    

    # definir posiciones de ciudades en ruta ---------------------------------------------------
    def definir_pos(self):
        self.pos = [0] * len(self.ruta)
        for i in range(len(self.ruta)):
            # print("iteracion: " + str(i) + " - " + str((self.ruta)[i]))
            (self.pos)[(self.ruta)[i]] = i
        # print("Posiciones: " + str(self.pos))

    # siguiente node in ruta ----------------------------------------------
    def siguiente(self,v):
        return (self.ruta)[((self.pos)[v]+1) % len(self.ruta)]
    
        # previous node in ruta ------------------------------------------
    def anterior(self,v):
        return (self.ruta)[((self.pos)[v]-1) % len(self.ruta)]
    
def calcular_recorrido(luciernaga,tsp):
    largo = 0.0
    for i in range(len(luciernaga.ruta)):
        largo += tsp.distancia_euc((luciernaga.ruta)[i],(luciernaga.ruta)[(i+1) % len(luciernaga.ruta)])
    return largo

def generar_poblacion_inicial(tsp, cant_luciernagas):
    poblacion = [Firefly() for _ in range(cant_luciernagas)]
    for i in range(cant_luciernagas):
        poblacion[i].ruta = random.sample(range(tsp.num_nodos), tsp.num_nodos)
        poblacion[i].definir_pos()
        poblacion[i].recorrido_total = poblacion[i].costo_recorrido(tsp)
        poblacion[i].intensidad_luz = 1.0 / poblacion[i].recorrido_total
    return poblacion

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

def generar_luciernagas_nn(tsp, n):
    luciernagas = []
    for _ in range(n):
        ruta = nearest_neighbor(tsp)
        luciernaga = Firefly()
        luciernaga.ruta = ruta
        luciernaga.recorrido_total = luciernaga.costo_recorrido(tsp)
        luciernaga.intensidad_luz = 1.0 / luciernaga.recorrido_total
        luciernagas.append(luciernaga)
    return luciernagas

def mutacion_inversa_movimiento(tsp, luciernaga, distancia, tamano_seccion_m):
    nuevas_luciernagas = []
    nueva_ruta = luciernaga.ruta[:]

    for i in range(tamano_seccion_m):
        nueva_luciernaga = Firefly()  # Crear una nueva instancia en cada iteración
        inicio = random.randint(0, len(nueva_ruta) - distancia)
        tamano_seccion = random.randint(2, distancia)  # Longitud aleatoria del segmento entre 2 y la distancia
        fin = inicio + tamano_seccion
        seccion_reversa = nueva_ruta[inicio:fin][::-1]
        nueva_ruta = nueva_ruta[:inicio] + seccion_reversa + nueva_ruta[fin:]
        nueva_luciernaga = Firefly()
        nueva_luciernaga.ruta = nueva_ruta[:]
        nueva_luciernaga.recorrido_total = nueva_luciernaga.costo_recorrido(tsp)
        nueva_luciernaga.definir_pos()
        nueva_luciernaga.intensidad_luz = 1.0 / nueva_luciernaga.recorrido_total
        nuevas_luciernagas.append(nueva_luciernaga)
    # print("Nueva luciernaga mov: " + str(nueva_luciernaga.ruta) + " - " + str(nueva_luciernaga.recorrido_total) + " - " + str(nueva_luciernaga.intensidad_luz))
    return nuevas_luciernagas

# Movimiento cuando no hay luciernaga mas atractiva
def mutacion_inversa_random(tsp, luciernaga, tamano_seccion_m):
    nuevas_luciernagas = []
    copia_ruta = luciernaga.ruta[:]

    for i in range(tamano_seccion_m):
        nueva_luciernaga = Firefly()  # Crear una nueva instancia en cada iteración
        inicio = random.randint(0, len(copia_ruta) - tamano_seccion_m)
        fin = inicio + tamano_seccion_m
        seccion_reversa = copia_ruta[inicio:fin][::-1]
        nueva_ruta = copia_ruta[:inicio] + seccion_reversa + copia_ruta[fin:]
        nueva_luciernaga.ruta = nueva_ruta[:]
        nueva_luciernaga.definir_pos()
        nueva_luciernaga.recorrido_total = nueva_luciernaga.costo_recorrido(tsp)
        nueva_luciernaga.intensidad_luz = 1.0 / nueva_luciernaga.recorrido_total
        # print("Nueva luciernaga ran: " + str(nueva_luciernaga.ruta) + " - " + str(nueva_luciernaga.recorrido_total) + " - " + str(nueva_luciernaga.intensidad_luz))
        nuevas_luciernagas.append(nueva_luciernaga)
    return nuevas_luciernagas

def evaluar_mejora(tsp, luciernaga, u, v, flag):
    actual = tsp.distancia_euc(u,luciernaga.siguiente(u)) + tsp.distancia_euc(v,luciernaga.siguiente(v))
    nueva = tsp.distancia_euc(u,v) + tsp.distancia_euc(luciernaga.siguiente(u),luciernaga.siguiente(v))
    return nueva - actual

def cambiar_ruta(tsp, luciernaga, u, v):
    if (luciernaga.pos)[u] < (luciernaga.pos)[v]:
        i, j = (luciernaga.pos)[u], (luciernaga.pos)[v]
    else:
        i, j = (luciernaga.pos)[v], (luciernaga.pos)[u]
    # reverse sub-path [i+1,...,j]
    (luciernaga.ruta)[i+1:j+1] = list(reversed((luciernaga.ruta)[i+1:j+1]))
    # actualizar posiciones
    luciernaga.definir_pos()
    # llamar a la FUNCION OBJETIVO para calcular la longitud del ruta
    luciernaga.recorrido_total = luciernaga.costo_recorrido(tsp)
    # print("call_count: " + str(luciernaga.call_count))

def dos_opt(tsp, luciernaga):
    contador = 0
    # generar vecindario
    tsp.gen_vecindario(2)
    NUM_EPSILON = 1e-9  # Define el valor epsilon
    luciernaga.definir_pos()
    # print("Posiciones: " + str(luciernaga.pos))
    luciernaga_actual = luciernaga.copiar()  # Se clona la luciernaga original para trabajar sobre ella
    mejora_encontrada = False
    reiniciar = True
    mejor_luciernaga = None
    while reiniciar and not mejora_encontrada:
        reiniciar = False
        # Generador bajo demanda de vecinos (tuplas de nodos)
        vecindario = ((u, v)
                      for u in luciernaga.ruta
                      for v in tsp.vecinos[u])
        for u, v in vecindario:
            # evaluar mejora con costo normal
            delta = evaluar_mejora(tsp, luciernaga_actual, u, v, 'distancia_euc')
            contador += 1
            if luciernaga_actual.recorrido_total + delta < luciernaga.recorrido_total - NUM_EPSILON:
                mejor_luciernaga = luciernaga_actual.copiar()
                cambiar_ruta(tsp, mejor_luciernaga, u, v)
                mejora_encontrada = True  # Se encontró una mejora, salir del bucle
                break  # Salir del bucle interno

            # evaluar mejora con costo penalizado
            delta = evaluar_mejora(tsp, luciernaga_actual, u, v, 'distancia_penalizada')
            contador += 1
            if delta < -NUM_EPSILON:
                cambiar_ruta(tsp, luciernaga_actual, u, v)
                mejora_encontrada = True  # Se encontró una mejora, salir del bucle
                break  # Salir del bucle interno
        # print("deberia salir solo una vez")
    return mejor_luciernaga, contador



def DFA(tsp, cant_luciernagas, max_call_objetive_function, coef_absorcion, tamano_seccion_m):
    print("\n[ DFA Algoritm ]")
    contador_llamados = 0
    poblacion_temporal = []
    historial = []
    contador_sin_mejora = 0
    historial_completo = []
    temporal = []

    # Generar luciernagas iniciales
    poblacion = generar_luciernagas_nn(tsp, cant_luciernagas)
    # for luciernaga in poblacion:
        # print("Luciernaga inicial: " + str(luciernaga.ruta) + " - " + str(luciernaga.recorrido_total) + " - " + str(luciernaga.intensidad_luz))
    contador_llamados += cant_luciernagas

    # Iterar hasta que se cumpla el criterio de parada
    while contador_llamados < max_call_objetive_function:
        for luciernaga in poblacion:
            luciernaga_mas_atractiva = luciernaga.obtener_luciernaga_mas_atractiva(poblacion, coef_absorcion)
            # Si hay luciernaga mas atractiva
            if luciernaga_mas_atractiva != None:
                # print("Luciernaga actual: " + str(luciernaga.ruta) + " - " + str(luciernaga.recorrido_total) + " - " + str(luciernaga.intensidad_luz))
                # print("Luciernaga mas atractiva: " + str(luciernaga_mas_atractiva.ruta) + " - " + str(luciernaga_mas_atractiva.recorrido_total) + " - " + str(luciernaga_mas_atractiva.intensidad_luz))

                # calcular distancia
                distancia = luciernaga.distancia_luciernaga(luciernaga_mas_atractiva)
                # print("Distancia: " + str(distancia))

                # Mover luciernaga
                nuevas_luciernagas = mutacion_inversa_movimiento(tsp, luciernaga, distancia, tamano_seccion_m)
                # print("Nueva luciernaga: " + str(nueva_luciernaga.ruta) + " - " + str(nueva_luciernaga.recorrido_total) + " - " + str(nueva_luciernaga.intensidad_luz))
                contador_llamados += 1

                poblacion_temporal.append(luciernaga)
                # poblacion_temporal.append(nueva_luciernaga)
                for nueva_luciernaga in nuevas_luciernagas:
                    poblacion_temporal.append(nueva_luciernaga)
            else:
                # print("Luciernaga actual: " + str(luciernaga.ruta) + " - " + str(luciernaga.recorrido_total) + " - " + str(luciernaga.intensidad_luz))
                # print("No hay luciernaga mas atractiva")
                # nuevas_luciernagas = mutacion_inversa_random(tsp, luciernaga, tamano_seccion_m)
                # contador_llamados += tamano_seccion_m
                # busqueda local
                nueva_luciernaga, contador = dos_opt(tsp, luciernaga)
                contador_llamados += contador
                if nueva_luciernaga != None:
                    poblacion_temporal.append(luciernaga)
                    poblacion_temporal.append(nueva_luciernaga)
                else:
                    poblacion_temporal.append(luciernaga)
                # for nueva_luciernaga in nuevas_luciernagas:
                #     poblacion_temporal.append(nueva_luciernaga)
        # break
        # seleccionar mejores luciernagas
        poblacion_temporal.sort(key=lambda x: x.recorrido_total)
        poblacion_temporal = poblacion_temporal[:cant_luciernagas]
        poblacion = poblacion_temporal[:cant_luciernagas]
        poblacion_temporal = []
        historial.append(poblacion[0].recorrido_total)
        for luciernaga in poblacion:
            temporal.append(luciernaga.recorrido_total)
        historial_completo.append(temporal)
        temporal = []
        # print("Mejor recorrido: " + str(poblacion[0].ruta) + " - " + str(poblacion[0].recorrido_total) + " - " + str(poblacion[0].intensidad_luz))
        print("mejor recorrido total: " + str(poblacion[0].recorrido_total))
        print("contador_llamados: " + str(contador_llamados))
    # print("Llamados a funcion objetivo: " + str(contador_llamados))
    # graficar historial
    # plt.plot(historial)
    # plt.ylabel('Costo')
    # plt.xlabel('Iteraciones')
    # plt.show()
    # historial_completo = historial_completo[::25]
    plt.figure(figsize=(14, 12))
    plt.boxplot(historial_completo)
    plt.title('Convergencia de población')
    plt.xlabel('Distribución de población')
    plt.ylabel('Costos de recorrido')
    # plt.xticks(ticks=np.arange(1, len(historial_completo) + 1), labels=[f'iter {i}' for i in range(1, len(historial_completo) + 1)])
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return poblacion

def objective(trial):
    # Define los rangos para los hiperparámetros que quieres optimizar
    cant_luciernagas = trial.suggest_int('cant_luciernagas', 2, 5)
    coef_absorcion = trial.suggest_float('coef_absorcion', 0.00001, 0.21)
    tamano_seccion_m = trial.suggest_int('tamano_seccion_m', 2, 11)

    # leer tsp
    tsp = Tsp()
    tsp.leer("./datasets/qa194.tsp")
    tsp.escribir()
    
    # Crear una instancia de DFA con los parámetros optimizados
    poblacion = DFA(tsp, cant_luciernagas, 5000, coef_absorcion, tamano_seccion_m)
    
    # Ejecutar tu función de objetivo con la población creada
    result = calcular_recorrido(poblacion[0], tsp)  # Reemplaza 'your_objective_function' con tu función de objetivo
    
    return result

def correr_optuna():
    # Ejecutar la optimización con Optuna
    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=100)  # Cambia 'n_trials' al número deseado de intentos de optimización

    # Obtener los mejores parámetros encontrados
    best_params = study.best_params
    print("Mejores parámetros:", best_params)
                

def main(nombre_entrada):
    # set random seed
    # random.seed(1)

    # set starting time
    tiempo_inicial = time.time()

    # leer instancia TSP
    tsp = Tsp()
    tsp.leer(nombre_entrada)
    tsp.escribir()

    # Variables
    cant_luciernagas = 2
    max_call_objetive_function = 100000
    coef_absorcion = 0.1324801200969674
    tamano_seccion_m = 10

    # Llamada DFA
    poblacion = DFA(tsp, cant_luciernagas, max_call_objetive_function, coef_absorcion, tamano_seccion_m)
    # print("Mejor recorrido FINAL : " + str(poblacion[0].ruta) + " - " + str(poblacion[0].recorrido_total) + " - " + str(poblacion[0].intensidad_luz))
    # print("Llamados a funcion objetivo: " + str(poblacion[0].call_count))
    # print costos
    # for luciernaga in poblacion:
    #     print("Costo recorrido: " + str(luciernaga.recorrido_total))

    # set completion time
    end_time = time.time()
    # display computation time
    print('\nTotal time:\t%.3f sec' % (end_time - tiempo_inicial))

    return poblacion

def escribir_en_archivo(arreglos, nombre_entrada):
    try:
        with open("new_salida.txt", 'a') as archivo:
            archivo.write('\n'+ "### " + nombre_entrada + " ###" + '\n')
            for arreglo in arreglos:
                archivo.write(str(arreglo) + '\n')
            # archivo.write(str(arreglo) + '\n\n')
                
        print(f"El arreglo se ha escrito exitosamente en salida.txt.")
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")

if __name__ == "__main__":
    # main()
    # correr_optuna()

    # # DATASETS OPTIMUM VALUES
    # qa194 = 9352
    # wi29 = 27603
    # dj38 = 6656
    # uy734 = 79114
    # zi929 = 95345
    # lu980 = 11340

    # Ciclo de ejecuciones

    num_executions = 21  # Número de ejecuciones
    results = []  # Almacenar resultados
    lengths = []
    all_lengths = []
    # datasets = ["./datasets/uy734.tsp", "./datasets/zi929.tsp", "./datasets/lu980.tsp"]
    # datasets = ["./datasets/qa194.tsp"]
    datasets = ["./datasets/wi29.tsp"]
    # datasets = ["./datasets/wi29.tsp", "./datasets/dj38.tsp", "./datasets/uy734.tsp", "./datasets/zi929.tsp", "./datasets/lu980.tsp"]

    for dataset in datasets:
        for i in range(num_executions):
            # Establecer una semilla aleatoria diferente en cada ejecución
            random.seed(i)
            # Realizar la ejecución
            print(f"\nEjecución {i + 1} con semilla {i}:")
            poblacion = main(dataset)
            for luciernaga in poblacion:
                lengths.append(luciernaga.recorrido_total)
            all_lengths.append(lengths)
            lengths = []
        # escribir
        escribir_en_archivo(all_lengths, dataset)
        all_lengths = []
        lengths = []

    # correr instancias
    # dataset = "./datasets/lu980.tsp"
    # # mejor solucion
    # random.seed(0)
    # poblacion = main(dataset)

    # # peor solucion
    # random.seed(16)
    # poblacion = main(dataset)


