import random
import sys
import time
import math
import matplotlib.pyplot as plt
import numpy as np
import optuna

INTVL_TIME = 1.0  # interval time for display logs
NUM_EPSILON = 0.001  # tolerance for numerical error
# NB_LIST_SIZE = 5  # size of neighbor-list

class Tsp:
    # constructor ----------------------------------------------------
    def __init__(self):
        self.name = ''
        self.num_node = 0  # number of nodes
        self.coord = []  # coordinate list of nodes
        self.neighbor = []  # neighbor-list
    # read TSP data --------------------------------------------------
    def read(self, filename):
        # open file
        input_file = open(filename, 'r')
        data = input_file.readlines()
        input_file.close()

        # read data
        for i in range(len(data)):
            data[i] = (data[i].rstrip()).split()
            data[i] = list(filter(lambda str:str != ':', data[i]))  # remove colon
            if len(data[i]) > 0:
                data[i][0] = data[i][0].rstrip(':')
                if data[i][0] == 'NAME':
                    self.name = data[i][1]
                elif data[i][0] == 'TYPE':
                    if data[i][1] != 'TSP':
                        print('Problem type is not TSP!')
                        sys.exit(1)
                elif data[i][0] == 'DIMENSION':
                    self.num_node = int(data[i][1])
                elif data[i][0] == 'EDGE_WEIGHT_TYPE':  # NOTE: accept only EUC_2D
                    if data[i][1] != 'EUC_2D':
                        print('Edge weight type is not EUC_2D')
                        sys.exit(1)
                elif data[i][0] == 'NODE_COORD_SECTION':
                    sec_coord = i

        # coord section
        self.coord = [(0.0, 0.0)] * self.num_node
        line_cnt = sec_coord+1
        for i in range(self.num_node):
            (self.coord)[int(data[line_cnt][0])-1] = (float(data[line_cnt][1]),float(data[line_cnt][2]))
            line_cnt += 1

    # print TSP data -------------------------------------------------
    def write(self):
        print('\n[TSP data]')
        print('name:\t{}'.format(self.name))
        print('#node:\t{}'.format(self.num_node))
        print('coord:\t{}'.format(self.coord))

    # calculate distance (rounded euclidian distance in 2D) ----------
    def dist(self,v1,v2):
        xd = float((self.coord)[v1][0] - (self.coord)[v2][0])
        yd = float((self.coord)[v1][1] - (self.coord)[v2][1])
        return float(int(math.sqrt(xd * xd + yd * yd)+0.5))

    # construct neighbor-list ----------------------------------------
    # Funcion que genera un vecindario de tamaño NB_LIST_SIZE para cada nodo, ordenado de menor a mayor distancia
    def gen_neighbor(self, nb_list_size):
        self.neighbor = [[] for _ in range(self.num_node)]
        for i in range(self.num_node):
            temp = [(self.dist(i,j),j) for j in range(self.num_node) if j != i]
            temp.sort(key=lambda x: x[0])
            (self.neighbor)[i] = [temp[h][1] for h in range(min(nb_list_size,self.num_node))]
        # print("Vecinos: " + str(self.neighbor))

class Work:
    # constructor ----------------------------------------------------
    def __init__(self,tsp,penalty_ratio):
        self.tour = [i for i in range(tsp.num_node)]  # tour of salesman
        self.pos = [i for i in range(tsp.num_node)]  # position of nodes in tour
        self.call_count = 0
        self.obj = self.length(tsp)  # objective value
        self.penalty = {}  # penalty for edges
        self.penalty_ratio = penalty_ratio  # penalty ratio for edges
    
    def copy(self,org):
        self.tour = org.tour[:]
        self.pos = org.pos[:]
        self.obj = org.obj
        self.penalty = (org.penalty).copy()
        self.call_count = org.call_count

    def length(self,tsp):
        length = 0.0
        self.call_count += 1
        for i in range(len(self.tour)):
            length += tsp.dist((self.tour)[i],(self.tour)[(i+1) % len(self.tour)])
        return length

    # calculate penalized distance -----------------------------------
    def pdist(self,tsp,v1,v2):
        if (v1,v2) in self.penalty:
            return tsp.dist(v1,v2) + self.penalty_ratio * (self.penalty)[v1,v2]
        else:
            return tsp.dist(v1,v2)

    # set position ---------------------------------------------------
    def set_pos(self):
        for i in range(len(self.tour)):
            (self.pos)[(self.tour)[i]] = i

    # next node in tour ----------------------------------------------
    def next(self,v):
        return (self.tour)[((self.pos)[v]+1) % len(self.tour)]

    # previous node in tour ------------------------------------------
    def prev(self,v):
        return (self.tour)[((self.pos)[v]-1) % len(self.tour)]

    # write WORK data ------------------------------------------------
    def write(self,tsp):
        print('\n[Tour data]')
        print('length= {}'.format(self.length(tsp)))

def random_tour(tsp, work):
    print('\n[Random tour]')
    tour = list(range(tsp.num_node))  # Crea una lista de nodos en orden secuencial
    random.shuffle(tour)  # Mezcla aleatoriamente la lista de nodos

    # Establece la ruta aleatoria como la nueva ruta de trabajo
    work.tour = tour
    work.set_pos()
    work.obj = work.length(tsp)

    # Imprime la longitud de la ruta aleatoria
    print('length= {}'.format(work.obj))

# Funcion que actualiza las penalizaciones de las aristas del tour
def update_penalty(tsp,work):
    max_val = 0.0
    arg_max_val = None
    for i in range(len(work.tour)): # Se recorre el tour
        v = (work.tour)[i]
        next_v = (work.tour)[(i+1) % len(work.tour)]
        if (v,next_v) in work.penalty: # Se evalua si la arista ya tiene penalizacion
            val = float(tsp.dist(v,next_v)) / float(1.0 + (work.penalty)[v,next_v]) # Se calcula (Ci / 1 + Pi) => util
        else:
            val = float(tsp.dist(v,next_v)) # Si la arista no tiene penalizacion se calcula la distancia normal
        if val > max_val:
            max_val = val
            arg_max_val = (v,next_v)
    v, next_v = arg_max_val
    if (v,next_v) in work.penalty: # Si la arista ya tiene penalizacion se aumenta en 1
        (work.penalty)[v,next_v] += 1.0
    else:
        (work.penalty)[v,next_v] = 1.0 # Si la arista no tiene penalizacion se crea con valor 1
    if (next_v,v) in work.penalty:
        (work.penalty)[next_v,v] += 1.0 # Se hace lo mismo para la arista inversa
    else:
        (work.penalty)[next_v,v] = 1.0 # Se hace lo mismo para la arista inversa

def guided_local_search(tsp, work, max_call_count,penalty_ratio):
    print('\n[guided local search algorithm]')
    datos_convergencia = []
    contador = 0
    
    # initialize first random tour
    random_tour(tsp, work)
    
    # initialize current working data
    cur_work = Work(tsp,penalty_ratio)
    cur_work.copy(work)

    start_time = cur_time = disp_time = time.time() # set starting time
    cnt = 0 # counter for display logs
    while contador < max_call_count:
        best_obj = work.obj
        temp = contador
        # local search
        contador = two_opt_search(tsp, work, cur_work,max_call_count, temp)

        # update penalty
        update_penalty(tsp,cur_work)

        cnt += 1
        cur_time = time.time()

        # save current values
        datos_convergencia.append(cur_work.obj)

        # display improvement
        if work.obj < best_obj:
            print('{}\t{}*\t{}\t{:.2f}'.format(cnt,cur_work.obj,work.obj,cur_time-start_time))
        elif cur_time - disp_time > INTVL_TIME:
            print('{}\t{}\t{}\t{:.2f}'.format(cnt,cur_work.obj,work.obj,cur_time-start_time))
            disp_time = time.time()

    # print tour length
    print('final length= {}'.format(work.obj))
    return datos_convergencia

# evaluate difference for 2-opt operation
def eval_diff(tsp, work, u, v, flag):
    if flag == 'pdist':
        cur = work.pdist(tsp,u,work.next(u)) + work.pdist(tsp,v,work.next(v))
        new = work.pdist(tsp,u,v) + work.pdist(tsp,work.next(u),work.next(v))
        return new - cur
    else:
        cur = tsp.dist(u,work.next(u)) + tsp.dist(v,work.next(v))
        new = tsp.dist(u,v) + tsp.dist(work.next(u),work.next(v))
        return new - cur

# change tour by 2-opt operation
def change_tour(tsp, work, u, v):
    if (work.pos)[u] < (work.pos)[v]:
        i, j = (work.pos)[u], (work.pos)[v]
    else:
        i, j = (work.pos)[v], (work.pos)[u]
    # reverse sub-path [i+1,...,j]
    (work.tour)[i+1:j+1] = list(reversed((work.tour)[i+1:j+1]))
    # update positions
    work.set_pos()
    # update objective value
    work.obj = work.length(tsp)
    # print("call_count: " + str(work.call_count))

def two_opt_search(tsp, work, cur_work, max_call_count,contador):
    nuevo_contador = contador
    # 2-opt neighborhood search
    improved = False
    restart = True
    while restart:
        if nuevo_contador >= max_call_count:
            print("MAXIMO ALCANZADO1 " + str(nuevo_contador))
            restart = False
            break
        restart = False
        # Generador bajo demanda de vecinos (tuplas de nodos)
        nbhd = ((u,v)
                for u in work.tour
                for v in (tsp.neighbor)[u])
        for u,v in nbhd:
            # evaluate difference in original distance
            delta = eval_diff(tsp, cur_work, u, v, 'dist') # Se evalua la mejora del tour con el posible swap de los nodos
            if cur_work.obj + delta < work.obj - NUM_EPSILON: # Si se presenta mejoras en el tour se actualiza el tour (work = cur_work)
                # update incumbent tour
                work.copy(cur_work) 
                change_tour(tsp, work, u, v) #Se cambia el work original
                nuevo_contador += 1
            if nuevo_contador >= max_call_count:
                print("MAXIMO ALCANZADO2 " + str(nuevo_contador))
                restart = False
                break
            # evaluate difference in penalized cost
            delta = eval_diff(tsp, cur_work, u, v, 'pdist') # Se evalua la mejora del tour con el posible swap de los nodos penalizados
            if delta < -NUM_EPSILON:  # Si se presenta mejoras significativas en el tour se actualiza el current tour
                # change current tour
                change_tour(tsp, cur_work, u, v) #Se cambia el work temporal
                nuevo_contador += 1
                improved = True
                restart = True
                if nuevo_contador >= max_call_count:
                    print("MAXIMO ALCANZADO3 " + str(nuevo_contador))
                    restart = False
                break
    return nuevo_contador

def objective(trial):
    # Define el rango de búsqueda para el penalty_ratio
    penalty_ratio = trial.suggest_float('penalty_ratio', 0.1, 10.0)

    # Define el rango de búsqueda para nb_list_size
    nb_list_size = trial.suggest_int('nb_list_size', 4, 10)

    # Realiza la optimización utilizando el penalty_ratio
    tsp = Tsp()
    tsp.read("./datasets/qa194.tsp")
    tsp.gen_neighbor(nb_list_size)

    work = Work(tsp, penalty_ratio)
    random_tour(tsp, work)
    datos_convergencia = guided_local_search(tsp, work, 5000, penalty_ratio)

    # Define la función objetivo, por ejemplo, minimizar la longitud del tour
    return work.obj

# --------------------------------------------------------------------
#   main
# --------------------------------------------------------------------
def main(argv=sys.argv):
    # # set parameters
    # # penalty_ratio = 8.108455507870257
    # penalty_ratio = 7.594320955969139
    # max_call_count = 5000
    # nb_list_size = 5
    # # tiempo_maximo = 250
    # # set random seed
    # random.seed(6)  

    # # # set starting time
    # start_time = time.time()

    # # read instance
    # tsp = Tsp()
    # tsp.read("./datasets/qa194.tsp")
    # tsp.write()

    # # construct neighbor-list
    # tsp.gen_neighbor(nb_list_size)

    # # solve TSP
    # work = Work(tsp,penalty_ratio)  # create work
    # datos_convergencia = guided_local_search(tsp, work, max_call_count,penalty_ratio)  # guided local search
    # work.write(tsp)

    # # set completion time
    # end_time = time.time()
    # # display computation time
    # print('\nTotal time:\t%.3f sec' % (end_time - start_time))
    

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
    # gap = (work.obj - qa194) / qa194
    # print("Gap: " + str(gap))

    # largos = [9532.0, 9539.0, 9412.0, 9415.0, 9572.0, 9444.0, 9360.0, 9465.0, 9426.0, 9523.0, 9451.0, 9413.0, 9690.0, 9362.0, 9433.0, 9427.0, 9488.0, 9519.0, 9564.0, 9547.0, 9388.0]
    # # xd = [1,2,3,4,5,6]
    # mediana = np.median(np.sort(largos))
    # print("Mediana: " + str(mediana))

    # return datos_convergencia, work.obj
    # EJECUCION DE OPTUNA 
    # Crea un estudio Optuna
    study = optuna.create_study(direction='minimize')
    # Ejecuta la optimización
    study.optimize(objective, n_trials=31)
    # Obtiene el mejor valor de penalty_ratio
    best_penalty_ratio = study.best_params['penalty_ratio']
    best_nb_list_size = study.best_params['nb_list_size']
    # Imprime el mejor valor encontrado
    print(f"Mejor valor de penalty_ratio encontrado: {best_penalty_ratio}")
    print(f"Mejor valor de nb_list_size encontrado: {best_nb_list_size}")



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
    #     main_result,length = main()
    #     results.append(main_result)
    #     lengths.append(length)
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