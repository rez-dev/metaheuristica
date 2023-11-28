# FA ALGORITHM FOR TSP
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
    
    def copiar(self):
        copia = Firefly()
        copia.ruta = self.ruta[:]
        copia.recorrido_total = self.recorrido_total
        copia.intensidad_luz = self.intensidad_luz
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
    
def calcular_recorrido(luciernaga,tsp):
    largo = 0.0
    for i in range(len(luciernaga.ruta)):
        largo += tsp.distancia_euc((luciernaga.ruta)[i],(luciernaga.ruta)[(i+1) % len(luciernaga.ruta)])
    return largo

def generar_poblacion_inicial(tsp, cant_luciernagas):
    poblacion = [Firefly() for _ in range(cant_luciernagas)]
    for i in range(cant_luciernagas):
        poblacion[i].ruta = random.sample(range(tsp.num_nodos), tsp.num_nodos)
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

def mutacion_inversa_movimiento(tsp, luciernaga, distancia, cant_nuevas_luciernagas):
    nuevas_luciernagas = []
    nueva_ruta = luciernaga.ruta[:]

    for i in range(cant_nuevas_luciernagas):
        nueva_luciernaga = Firefly()  # Crear una nueva instancia en cada iteración
        inicio = random.randint(0, len(nueva_ruta) - distancia)
        tamano_seccion = random.randint(2, distancia)  # Longitud aleatoria del segmento entre 2 y la distancia
        fin = inicio + tamano_seccion
        seccion_reversa = nueva_ruta[inicio:fin][::-1]
        nueva_ruta = nueva_ruta[:inicio] + seccion_reversa + nueva_ruta[fin:]
        nueva_luciernaga = Firefly()
        nueva_luciernaga.ruta = nueva_ruta[:]
        nueva_luciernaga.recorrido_total = nueva_luciernaga.costo_recorrido(tsp)
        nueva_luciernaga.intensidad_luz = 1.0 / nueva_luciernaga.recorrido_total
        nuevas_luciernagas.append(nueva_luciernaga)
    # print("Nueva luciernaga mov: " + str(nueva_luciernaga.ruta) + " - " + str(nueva_luciernaga.recorrido_total) + " - " + str(nueva_luciernaga.intensidad_luz))
    return nuevas_luciernagas

# Movimiento cuando no hay luciernaga mas atractiva
def mutacion_inversa_random(tsp, luciernaga, cant_nuevas_luciernagas):
    nuevas_luciernagas = []
    copia_ruta = luciernaga.ruta[:]
    # print("Ruta original: " + str(copia_ruta) + " - " + str(luciernaga.recorrido_total) + " - " + str(luciernaga.intensidad_luz))

    for i in range(cant_nuevas_luciernagas):
        nueva_luciernaga = Firefly()
        # generar mutacion inversa de tamaño random
        tamano_seccion = random.randint(2, len(copia_ruta) - 1)
        inicio = random.randint(0, len(copia_ruta) - tamano_seccion)
        fin = inicio + tamano_seccion
        seccion_reversa = copia_ruta[inicio:fin][::-1]
        copia_ruta = copia_ruta[:inicio] + seccion_reversa + copia_ruta[fin:]
        nueva_luciernaga.ruta = copia_ruta[:]
        nueva_luciernaga.recorrido_total = nueva_luciernaga.costo_recorrido(tsp)
        nueva_luciernaga.intensidad_luz = 1.0 / nueva_luciernaga.recorrido_total
        nuevas_luciernagas.append(nueva_luciernaga)
        # print("inicio: " + str(inicio) + " - fin: " + str(fin) + " - tamano_seccion: " + str(tamano_seccion))
        # print("Nueva luciernaga random: " + str(nueva_luciernaga.ruta) + " - " + str(nueva_luciernaga.recorrido_total) + " - " + str(nueva_luciernaga.intensidad_luz))
    return nuevas_luciernagas


def DFA(tsp, cant_luciernagas, max_call_objetive_function, coef_absorcion, cant_nuevas_luciernagas):
    print("\n[ DFA Algoritm ]")
    contador_llamados = 0
    poblacion_temporal = []
    historial = []
    historial_completo = []
    temporal = []

    # Generar luciernagas iniciales
    poblacion = generar_luciernagas_nn(tsp, cant_luciernagas)
    contador_llamados += cant_luciernagas

    # Iterar hasta que se cumpla el criterio de parada
    while contador_llamados < max_call_objetive_function:
        for luciernaga in poblacion:
            luciernaga_mas_atractiva = luciernaga.obtener_luciernaga_mas_atractiva(poblacion, coef_absorcion)

            # Si hay luciernaga mas atractiva, se mueve hacia ella = mutacion inversa de tamaño [2, distancia]
            if luciernaga_mas_atractiva != None:

                # Calcular distancia
                distancia = luciernaga.distancia_luciernaga(luciernaga_mas_atractiva)

                # Mover luciernaga
                nuevas_luciernagas = mutacion_inversa_movimiento(tsp, luciernaga, distancia, cant_nuevas_luciernagas)
                contador_llamados += cant_nuevas_luciernagas

                poblacion_temporal.append(luciernaga)
                for nueva_luciernaga in nuevas_luciernagas:
                    poblacion_temporal.append(nueva_luciernaga)

            # Si es la luciernaga mas brillante, se mueve random = mutacion inversa de tamaño n
            else:
                nuevas_luciernagas = mutacion_inversa_random(tsp, luciernaga, cant_nuevas_luciernagas)
                contador_llamados += cant_nuevas_luciernagas

                poblacion_temporal.append(luciernaga)
                for nueva_luciernaga in nuevas_luciernagas:
                    poblacion_temporal.append(nueva_luciernaga)

        # Seleccionar mejores luciernagas
        # Ordenar poblacion por recorrido total
        poblacion_temporal.sort(key=lambda x: x.recorrido_total)

        # Seleccionar las mejores luciernagas
        poblacion_temporal = poblacion_temporal[:cant_luciernagas]
        poblacion = poblacion_temporal[:cant_luciernagas]

        # Se reinicia la poblacion temporal
        poblacion_temporal = []

        # Guardar mejor recorrido
        historial.append(poblacion[0].recorrido_total)
        for luciernaga in poblacion:
            temporal.append(luciernaga.recorrido_total)
        historial_completo.append(temporal)
        temporal = []

        # print("Mejor recorrido: " + str(poblacion[0].ruta) + " - " + str(poblacion[0].recorrido_total) + " - " + str(poblacion[0].intensidad_luz))
        print("mejor recorrido: " + str(poblacion[0].recorrido_total))
        # print("mejor recorrido total: " + str(poblacion[0].recorrido_total))
        print("contador_llamados: " + str(contador_llamados))
    
    # graficar historial
    # plt.plot(historial)
    # plt.ylabel('Costo')
    # plt.xlabel('Iteraciones')
    # plt.show()

    historial_completo = historial_completo[::50]
    plt.figure(figsize=(14, 12))
    plt.boxplot(historial_completo)
    plt.title('Convergencia de población')
    plt.xlabel('Distribución de población')
    plt.ylabel('Costos de recorrido')
    # plt.xticks(ticks=np.arange(1, len(historial_completo) + 1), labels=[f'iter {i}' for i in range(1, len(historial_completo) + 1)])
    # plt.grid(True)
    plt.tight_layout()
    plt.show()
    return poblacion

def objective(trial):
    # Define los rangos para los hiperparámetros que quieres optimizar
    cant_luciernagas = trial.suggest_int('cant_luciernagas', 3, 10)
    coef_absorcion = trial.suggest_float('coef_absorcion', 0.0001, 0.21)
    cant_nuevas_luciernagas = trial.suggest_int('cant_nuevas_luciernagas', 2, 11)

    # leer tsp
    tsp = Tsp()
    tsp.leer("./datasets/qa194.tsp")
    tsp.escribir()
    
    # Crear una instancia de DFA con los parámetros optimizados
    poblacion = DFA(tsp, cant_luciernagas, 5000, coef_absorcion, cant_nuevas_luciernagas)
    
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

def escribir_en_archivo(arreglos, nombre_entrada):
    try:
        with open("new_salida2.txt", 'a') as archivo:
            archivo.write('\n'+ "### " + nombre_entrada + " ###" + '\n')
            for arreglo in arreglos:
                minimo = min(arreglo)
                archivo.write(str(arreglo) + " - " + str(minimo) +'\n')
            # archivo.write(str(arreglo) + '\n\n')
                
        print(f"El arreglo se ha escrito exitosamente en salida.txt.")
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")                

def main():
    # set random seed
    random.seed(3)

    # set starting time
    tiempo_inicial = time.time()

    # leer instancia TSP
    tsp = Tsp()
    tsp.leer("./datasets/uy734.tsp")
    tsp.escribir()

    # Variables
    cant_luciernagas = 5
    max_call_objetive_function = 150000
    coef_absorcion = 0.20322278084306258
    cant_nuevas_luciernagas = 10

    # Llamada DFA
    poblacion = DFA(tsp, cant_luciernagas, max_call_objetive_function, coef_absorcion, cant_nuevas_luciernagas)
    print("Mejor recorrido FINAL : " + str(poblacion[0].ruta) + " - " + str(poblacion[0].recorrido_total) + " - " + str(poblacion[0].intensidad_luz))
    
    # imprimir poblacion final
    # for luciernaga in poblacion:
    #     print("Ruta: " + str(luciernaga.ruta) + " - " + str(luciernaga.recorrido_total) + " - " + str(luciernaga.intensidad_luz))

    # Test mutacion random
    # luciernagas = generar_poblacion_inicial(tsp, 1)
    # print("Ruta original: " + str(luciernagas[0].ruta) + " - " + str(luciernagas[0].recorrido_total) + " - " + str(luciernagas[0].intensidad_luz))

    # nuevas_luciernagas = mutacion_inversa_random(tsp, luciernagas[0], 2)


    # set completion time
    end_time = time.time()
    # display computation time
    print('\nTotal time:\t%.3f sec' % (end_time - tiempo_inicial))
    return poblacion

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

    # num_executions = 21  # Número de ejecuciones
    # results = []  # Almacenar resultados
    # lengths = []
    # all_lengths = []
    # # datasets = ["./datasets/uy734.tsp", "./datasets/zi929.tsp", "./datasets/lu980.tsp"]
    # # datasets = ["./datasets/qa194.tsp"]
    # datasets = ["./datasets/uy734.tsp"]
    # # datasets = ["./datasets/wi29.tsp", "./datasets/dj38.tsp", "./datasets/uy734.tsp", "./datasets/zi929.tsp", "./datasets/lu980.tsp"]

    # for dataset in datasets:
    #     for i in range(num_executions):
    #         # Establecer una semilla aleatoria diferente en cada ejecución
    #         random.seed(i)
    #         # Realizar la ejecución
    #         print(f"\nEjecución {i + 1} con semilla {i}:")
    #         poblacion = main(dataset)
    #         for luciernaga in poblacion:
    #             lengths.append(luciernaga.recorrido_total)
    #         all_lengths.append(lengths)
    #         lengths = []
    #     # escribir
    #     escribir_en_archivo(all_lengths, dataset)
    #     all_lengths = []
    #     lengths = []