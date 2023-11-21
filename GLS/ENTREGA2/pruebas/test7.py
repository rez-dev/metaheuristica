import random
import sys
import time
import math
import matplotlib.pyplot as plt
import optuna

INTVL_TIME = 1.0  # interval time for display logs
NUM_EPSILON = 0.001  # tolerance for numerical error
NB_LIST_SIZE = 5  # size of neighbor-list

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
    def gen_neighbor(self):
        self.neighbor = [[] for _ in range(self.num_node)]
        for i in range(self.num_node):
            temp = [(self.dist(i,j),j) for j in range(self.num_node) if j != i]
            temp.sort(key=lambda x: x[0])
            (self.neighbor)[i] = [temp[h][1] for h in range(min(NB_LIST_SIZE,self.num_node))]
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

def guided_local_search(tsp, work, time_limit, max_call_count,penalty_ratio):
    # initialize first random tour
    random_tour(tsp, work)
    # print("work: " + str(work.tour) + " " + str(work.length(tsp)))
    # update penalty
    datos = []
    contador = 0
    # guided local search
    print('\n[guided local search algorithm]')
    # initialize current working data
    cur_work = Work(tsp,penalty_ratio)
    cur_work.copy(work)
    # Se agrega el random tour a la lista de datos
    # datos.append(cur_work.obj)
    # guided local search
    start_time = cur_time = disp_time = time.time()
    cnt = 0
    while cur_time - start_time < time_limit and contador < max_call_count:
        best_obj = work.obj
        temp = contador
        # Busqueda local
        contador = two_opt_search(tsp, work, cur_work,max_call_count, temp)
        # Actualizacion penalizaciones
        update_penalty(tsp,cur_work)

        cnt += 1
        cur_time = time.time()
        datos.append(cur_work.obj)
        if work.obj < best_obj:
            print('{}\t{}*\t{}\t{:.2f}'.format(cnt,cur_work.obj,work.obj,cur_time-start_time))
            # datos.append(cur_work.obj)
        elif cur_time - disp_time > INTVL_TIME:
            print('{}\t{}\t{}\t{:.2f}'.format(cnt,cur_work.obj,work.obj,cur_time-start_time))
            # datos.append(cur_work.obj)
            disp_time = time.time()

    # print tour length
    print('length= {}'.format(work.obj))
    return datos

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

    # Realiza la optimización utilizando el penalty_ratio
    tsp = Tsp()
    tsp.read("./datasets/qa194.tsp")
    tsp.gen_neighbor()

    work = Work(tsp, penalty_ratio)
    random_tour(tsp, work)
    datos = guided_local_search(tsp, work, 250, 5000, penalty_ratio)

    # Define la función objetivo, por ejemplo, minimizar la longitud del tour
    return work.obj

# --------------------------------------------------------------------
#   main
# --------------------------------------------------------------------
def main(argv=sys.argv):
    # # set starting time
    start_time = time.time()

    # read instance
    tsp = Tsp()
    tsp.read("./datasets/qa194.tsp")
    tsp.write()

    # construct neighbor-list
    tsp.gen_neighbor()

    # set parameters
    # penalty_ratio = 8.108455507870257
    penalty_ratio = 7.594320955969139
    max_call_count = 5000
    tiempo_maximo = 250

    # solve TSP
    work = Work(tsp,penalty_ratio)  # create work
    datos = guided_local_search(tsp, work, tiempo_maximo, max_call_count,penalty_ratio)  # guided local search
    work.write(tsp)

    # set completion time
    end_time = time.time()
    # display computation time
    print('\nTotal time:\t%.3f sec' % (end_time - start_time))

    # Print convergence graph
    print(datos)
    plt.plot(datos)
    plt.xlabel("Iteraciones")
    plt.ylabel("Distancia total")
    plt.title("Convergencia")
    plt.show()

    # EJECUCION DE OPTUNA 
    # Crea un estudio Optuna
    # study = optuna.create_study(direction='minimize')
    # # Ejecuta la optimización
    # study.optimize(objective, n_trials=50)
    # # Obtiene el mejor valor de penalty_ratio
    # best_penalty_ratio = study.best_params['penalty_ratio']
    # # Imprime el mejor valor encontrado
    # print(f"Mejor valor de penalty_ratio encontrado: {best_penalty_ratio}")

    # DATASES OPTIMUM VALUES
    # qa194 = 9352

    # wi29 = 27603
    # dj38 = 6656
    # uy734 = 79114
    # zi929 = 95345
    # lu980 = 11340



# main ---------------------------------------------------------------
if __name__ == "__main__":
    main()