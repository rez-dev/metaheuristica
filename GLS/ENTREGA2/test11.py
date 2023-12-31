# GLS 
# Rodrigo Escobar Zamorano
# Referencia: Shunji Umetani, "Guided Local Search Algorithm for Traveling Salesman Problem", 2019
# https://github.com/shunji-umetani/tsp-solver

# Importar librerías
import random
import sys
import time
import math
import matplotlib.pyplot as plt
import numpy as np
import optuna

# Variables globales
INTVL_TIME = 1.0  # intervalo de tiempo con el que se muestra el progreso
NUM_EPSILON = 0.001  # tolerancia de error para comparación de números flotantes

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

class Solucion:
    # constructor ----------------------------------------------------
    def __init__(self,tsp,grado_penalizacion):
        self.ruta = [i for i in range(tsp.num_nodos)]  # ruta of salesman
        self.pos = [i for i in range(tsp.num_nodos)]  # position of nodes in ruta
        self.call_count = 0
        self.recorrido_total = self.largo(tsp)  # objective value
        self.penalizaciones = {}  # penalizaciones for edges
        self.grado_penalizacion = grado_penalizacion  # penalizaciones ratio for edges
    
    def copiar(self,org):
        self.ruta = org.ruta[:]
        self.pos = org.pos[:]
        self.recorrido_total = org.recorrido_total
        self.penalizaciones = (org.penalizaciones).copy()
        self.call_count = org.call_count

    def largo(self,tsp):
        largo = 0.0
        self.call_count += 1
        for i in range(len(self.ruta)):
            largo += tsp.distancia_euc((self.ruta)[i],(self.ruta)[(i+1) % len(self.ruta)])
        return largo

    # calcular distancia_euc penalizada  -----------------------------------
    def distancia_penalizada(self,tsp,v1,v2):
        if (v1,v2) in self.penalizaciones:
            return tsp.distancia_euc(v1,v2) + self.grado_penalizacion * (self.penalizaciones)[v1,v2]
        else:
            return tsp.distancia_euc(v1,v2)

    # definir posiciones de ciudades en ruta ---------------------------------------------------
    def definir_pos(self):
        for i in range(len(self.ruta)):
            (self.pos)[(self.ruta)[i]] = i

    # siguiente node in ruta ----------------------------------------------
    def siguiente(self,v):
        return (self.ruta)[((self.pos)[v]+1) % len(self.ruta)]

    # previous node in ruta ------------------------------------------
    def anterior(self,v):
        return (self.ruta)[((self.pos)[v]-1) % len(self.ruta)]

    # escribir WORK data ------------------------------------------------
    def escribir(self,tsp):
        print('\n[ruta data]')
        print('largo= {}'.format(self.largo(tsp)))

def ruta_random(tsp, solucion):
    print('\n[ruta random]')
    ruta = list(range(tsp.num_nodos))  # Crea una lista de nodos en orden secuencial
    random.shuffle(ruta)  # Mezcla aleatoriamente la lista de nodos

    # Establece la ruta aleatoria como la nueva ruta de trabajo
    solucion.ruta = ruta
    solucion.definir_pos()
    solucion.recorrido_total = solucion.largo(tsp)

    # Imprime la longitud de la ruta aleatoria
    print('largo= {}'.format(solucion.recorrido_total))

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

def guided_local_search(tsp, max_call_count,grado_penalizacion):
    print('\n[algoritmo guided local search]')
    datos_convergencia = []
    contador = 0

    # inicializar clase de solucion
    solucion = Solucion(tsp,grado_penalizacion)
    
    # inicializar ruta inicial random
    ruta_random(tsp, solucion)
    
    # inicializa la solucion actual
    solucion_actual = Solucion(tsp,grado_penalizacion)
    solucion_actual.copiar(solucion)

    # se inicializa el tiempo
    tiempo_inicial = tiempo_actual = disp_time = time.time() 
    iteracion = 0 # counter for display logs

    # se inicializa el bucle de llamadas
    while contador < max_call_count:
        mejor_recorrido = solucion.recorrido_total
        temp = contador

        # busqueda local
        contador = dos_opt(tsp, solucion, solucion_actual,max_call_count, temp)

        # penalizar solucion actual por aparicion de aristas
        actualizar_penalizacion(tsp,solucion_actual)

        iteracion += 1
        tiempo_actual = time.time()

        # guardar recorrido de ruta
        datos_convergencia.append(solucion_actual.recorrido_total)

        # mostrar progreso en mejoras
        if solucion.recorrido_total < mejor_recorrido:
            print('{}\t{}*\t{}\t{:.2f}'.format(iteracion,solucion_actual.recorrido_total,solucion.recorrido_total,tiempo_actual-tiempo_inicial))
        elif tiempo_actual - disp_time > INTVL_TIME:
            print('{}\t{}\t{}\t{:.2f}'.format(iteracion,solucion_actual.recorrido_total,solucion.recorrido_total,tiempo_actual-tiempo_inicial))
            disp_time = time.time()

    # mostrar ruta largo
    print('largo final= {}'.format(solucion.recorrido_total))
    return datos_convergencia, solucion

# evaluar mejora con cambio de ruta
def evaluar_mejora(tsp, solucion, u, v, flag):
    # Se evalua la mejora del ruta con el posible swap de los nodos
    if flag == 'distancia_penalizada':
        actual = solucion.distancia_penalizada(tsp,u,solucion.siguiente(u)) + solucion.distancia_penalizada(tsp,v,solucion.siguiente(v))
        nueva = solucion.distancia_penalizada(tsp,u,v) + solucion.distancia_penalizada(tsp,solucion.siguiente(u),solucion.siguiente(v))
        return nueva - actual
    # Se evalua la mejora del ruta con el posible swap de los nodos penalizados
    else:
        actual = tsp.distancia_euc(u,solucion.siguiente(u)) + tsp.distancia_euc(v,solucion.siguiente(v))
        nueva = tsp.distancia_euc(u,v) + tsp.distancia_euc(solucion.siguiente(u),solucion.siguiente(v))
        return nueva - actual

# cambiar ruta por la operación 2-opt
def cambiar_ruta(tsp, solucion, u, v):
    if (solucion.pos)[u] < (solucion.pos)[v]:
        i, j = (solucion.pos)[u], (solucion.pos)[v]
    else:
        i, j = (solucion.pos)[v], (solucion.pos)[u]
    # reverse sub-path [i+1,...,j]
    (solucion.ruta)[i+1:j+1] = list(reversed((solucion.ruta)[i+1:j+1]))
    # actualizar posiciones
    solucion.definir_pos()
    # llamar a la FUNCION OBJETIVO para calcular la longitud del ruta
    solucion.recorrido_total = solucion.largo(tsp)
    # print("call_count: " + str(solucion.call_count))

def dos_opt(tsp, solucion, solucion_actual, max_call_count,contador):
    nuevo_contador = contador
    mejora = False
    reiniciar = True
    while reiniciar:
        if nuevo_contador >= max_call_count:
            # print("MAXIMO ALCANZADO1 " + str(nuevo_contador))
            reiniciar = False
            break
        reiniciar = False
        # Generador bajo demanda de vecinos (tuplas de nodos)
        vecindario = ((u,v)
                for u in solucion.ruta
                for v in (tsp.vecinos)[u])
        for u,v in vecindario:
            # evaluar mejora con costo normal
            delta = evaluar_mejora(tsp, solucion_actual, u, v, 'distancia_euc') # Se evalua la mejora del ruta con el posible swap de los nodos
            if solucion_actual.recorrido_total + delta < solucion.recorrido_total - NUM_EPSILON: # Si se presenta mejoras en el ruta se actualiza el ruta (solucion = solucion_actual)
                # actualizar ruta con el cambio de ruta
                solucion.copiar(solucion_actual) 
                # antes = solucion.recorrido_total
                cambiar_ruta(tsp, solucion, u, v) #Se cambia el solucion original
                # despues = solucion.recorrido_total
                # if antes < despues:
                #     print("AUMENTÓ EL LARGO1 " + str(antes) + " " + str(despues))
                nuevo_contador += 1
            if nuevo_contador >= max_call_count:
                # print("MAXIMO ALCANZADO2 " + str(nuevo_contador))
                reiniciar = False
                break
            # evaluar mejora con costo penalizado
            delta = evaluar_mejora(tsp, solucion_actual, u, v, 'distancia_penalizada') # Se evalua la mejora del ruta con el posible swap de los nodos penalizados
            if delta < -NUM_EPSILON:  # Si se presenta mejoras significativas en el ruta se actualiza el current ruta
                # change current ruta
                # print("solucion actual antes: " + str(solucion_actual.recorrido_total))
                # antes = solucion_actual.recorrido_total
                cambiar_ruta(tsp, solucion_actual, u, v) #Se cambia el solucion temporal
                # despues = solucion_actual.recorrido_total
                # if antes < despues:
                #     print("AUMENTÓ EL LARGO2 " + str(antes) + " " + str(despues))
                # print("solucion actual despues: " + str(solucion_actual.recorrido_total))
                nuevo_contador += 1
                mejora = True
                reiniciar = True
                if nuevo_contador >= max_call_count:
                    # print("MAXIMO ALCANZADO3 " + str(nuevo_contador))
                    reiniciar = False
                break
    return nuevo_contador

def objective(trial):
    # Define el rango de búsqueda para el grado_penalizacion
    grado_penalizacion = trial.suggest_float('grado_penalizacion', 0.1, 10.0)

    # Define el rango de búsqueda para cantidad_vecinos
    cantidad_vecinos = trial.suggest_int('cantidad_vecinos', 4, 10)

    # Realiza la optimización utilizando el grado_penalizacion y cantidad_vecinos
    tsp = Tsp()
    tsp.leer("./datasets/qa194.tsp")
    tsp.gen_vecindario(cantidad_vecinos)

    datos_convergencia, solucion = guided_local_search(tsp, 5000, grado_penalizacion)

    # Define la función objetivo, por ejemplo, minimizar la longitud del ruta
    return solucion.recorrido_total

# --------------------------------------------------------------------
#   main
# --------------------------------------------------------------------
def main(argv=sys.argv):
    # # parametros
    # # grado_penalizacion = 8.108455507870257
    # grado_penalizacion = 7.594320955969139
    # max_call_count = 5000
    # cantidad_vecinos = 5

    # # set random seed
    # random.seed(6)  

    # # set starting time
    # tiempo_inicial = time.time()

    # # leer instancia TSP
    # tsp = Tsp()
    # tsp.leer("./datasets/qa194.tsp")
    # tsp.escribir()

    # # generar lista de vecindarios
    # tsp.gen_vecindario(cantidad_vecinos)

    # # resolver TSP
    # # solucion = Solucion(tsp,grado_penalizacion)
    # datos_convergencia, solucion = guided_local_search(tsp, max_call_count,grado_penalizacion)
    # # solucion.escribir(tsp)

    # # set completion time
    # end_time = time.time()
    # # display computation time
    # print('\nTotal time:\t%.3f sec' % (end_time - tiempo_inicial))
    

    # # Print convergence graph
    # # print(datos_convergencia)
    # plt.plot(datos_convergencia)
    # plt.xlabel("Iteraciones")
    # plt.ylabel("Distancia total")
    # plt.title("Convergencia")
    # plt.show()

    # # DATASETS OPTIMUM VALUES
    # qa194 = 9352
    # wi29 = 27603
    # dj38 = 6656
    # uy734 = 79114
    # zi929 = 95345
    # lu980 = 11340

    # # Calculate gap with optimum value
    # gap = (solucion.recorrido_total - qa194) / qa194
    # print("Gap: " + str(gap))

    # largos = [9532.0, 9539.0, 9412.0, 9415.0, 9572.0, 9444.0, 9360.0, 9465.0, 9426.0, 9523.0, 9451.0, 9413.0, 9690.0, 9362.0, 9433.0, 9427.0, 9488.0, 9519.0, 9564.0, 9547.0, 9388.0]
    # # xd = [1,2,3,4,5,6]
    # mediana = np.median(np.sort(largos))
    # print("Mediana: " + str(mediana))
    # return datos_convergencia, solucion.recorrido_total

    # EJECUCION DE OPTUNA 
    # Crea un estudio Optuna
    study = optuna.create_study(direction='minimize')
    # Ejecuta la optimización
    study.optimize(objective, n_trials=31)
    # Obtiene el mejor valor de grado_penalizacion
    best_grado_penalizacion = study.best_params['grado_penalizacion']
    best_cantidad_vecinos = study.best_params['cantidad_vecinos']
    # Imprime el mejor valor encontrado
    print(f"Mejor valor de grado_penalizacion encontrado: {best_grado_penalizacion}")
    print(f"Mejor valor de cantidad_vecinos encontrado: {best_cantidad_vecinos}")



# main ---------------------------------------------------------------
if __name__ == "__main__":
    main()

    # # Ciclo de ejecuciones
    # num_executions = 21  # Número de ejecuciones
    # results = []  # Almacenar resultados
    # lengths = []

    # for i in range(num_executions):
    #     # Establecer una semilla aleatoria diferente en cada ejecución
    #     random.seed(i)

    #     # Realizar la ejecución
    #     print(f"\nEjecución {i + 1} con semilla {i}:")
    #     main_result,largo = main()
    #     results.append(main_result)
    #     lengths.append(largo)
    #     # plt.plot(results[i], label=f"Ejecución {i + 1}")

    # maximo_valor, posicion = max((numero, indice) for indice, numero in enumerate(lengths))
    # print(f"El máximo valor es {maximo_valor} y se encuentra en la posición {posicion}")
    # minimo_valor, posicion = min((numero, indice) for indice, numero in enumerate(lengths))
    # print(f"El mínimo valor es {minimo_valor} y se encuentra en la posición {posicion}")
    # print(lengths)
    # # Imprimir los resultados de todas las ejecuciones
    # # for i, result in enumerate(results):
    #     # print(f"Resultado de la ejecución {i + 1}: {result}")
    # # plt.xlabel("Iteraciones")
    # # plt.ylabel("Distancia total")
    # # plt.title("Convergencia de todas las ejecuciones")
    # # plt.legend()
    # # plt.show()
    # plt.boxplot(lengths)

    # # Agregar título y etiquetas a los ejes
    # plt.title('Diagrama de Cajas')
    # plt.ylabel('Valores')

    # # Mostrar el diagrama de cajas
    # plt.show()