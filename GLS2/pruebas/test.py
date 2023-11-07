import sys
import time
import math
import argparse
import networkx as netx
import matplotlib.pyplot as plt

# TIME_LIMIT = 60  # default time limit for iterated local search
INTVL_TIME = 1.0  # interval time for display logs
NUM_EPSILON = 0.001  # tolerance for numerical error
# OR_OPT_SIZE = 3  # size of sub-path (or_opt_search)
NB_LIST_SIZE = 5  # size of neighbor-list
PENALTY_RATIO = 1  # penalty ratio for edges

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
    def gen_neighbor(self):
        self.neighbor = [[] for _ in range(self.num_node)]
        for i in range(self.num_node):
            temp = [(self.dist(i,j),j) for j in range(self.num_node) if j != i]
            temp.sort(key=lambda x: x[0])
            (self.neighbor)[i] = [temp[h][1] for h in range(min(NB_LIST_SIZE,self.num_node))]

class Work:
    # constructor ----------------------------------------------------
    def __init__(self,tsp):
        self.tour = [i for i in range(tsp.num_node)]  # tour of salesman
        self.pos = [i for i in range(tsp.num_node)]  # position of nodes in tour
        self.obj = self.length(tsp)  # objective value
        self.penalty = {}  # penalty for edges
        # self.alpha = 0.0  # coefficient of penalized distance
    
    def copy(self,org):
        self.tour = org.tour[:]
        self.pos = org.pos[:]
        self.obj = org.obj
        self.penalty = (org.penalty).copy()
        # self.alpha = org.alpha

    def length(self,tsp):
        length = 0.0
        for i in range(len(self.tour)):
            length += tsp.dist((self.tour)[i],(self.tour)[(i+1) % len(self.tour)])
        return length

    # calculate penalized distance -----------------------------------
    def pdist(self,tsp,v1,v2):
        if (v1,v2) in self.penalty:
            return tsp.dist(v1,v2) + PENALTY_RATIO * (self.penalty)[v1,v2]
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


def nearest_neighbor(tsp, work):
    print('\n[nearest neighbor algorithm]')
    # nearest neighbor
    for i in range(1,tsp.num_node):
        # find nearest unvisited node
        min_dist = float('inf')
        arg_min_dist = None
        for j in range(i,tsp.num_node):
            dist = tsp.dist((work.tour)[i-1],(work.tour)[j])
            if dist < min_dist:
                min_dist = dist
                arg_min_dist = j
        # set nearest unvisited node
        (work.tour)[i], (work.tour)[arg_min_dist] = (work.tour)[arg_min_dist], (work.tour)[i]

    # initialize position of nodes in tour
    work.set_pos()
    # calculate tour length
    work.obj = work.length(tsp)

    # print tour length
    print('length= {}'.format(work.obj))

def guided_local_search(tsp, work, time_limit):
    # update penalty
    def update_penalty(tsp,work):
        max_val = 0.0
        arg_max_val = None
        for i in range(len(work.tour)):
            v = (work.tour)[i]
            next_v = (work.tour)[(i+1) % len(work.tour)]
            if (v,next_v) in work.penalty:
                val = float(tsp.dist(v,next_v)) / float(1.0 + (work.penalty)[v,next_v])
            else:
                val = float(tsp.dist(v,next_v))
            if val > max_val:
                max_val = val
                arg_max_val = (v,next_v)
        v, next_v = arg_max_val
        if (v,next_v) in work.penalty:
            (work.penalty)[v,next_v] += 1.0
        else:
            (work.penalty)[v,next_v] = 1.0
        if (next_v,v) in work.penalty:
            (work.penalty)[next_v,v] += 1.0
        else:
            (work.penalty)[next_v,v] = 1.0

    # guided local search
    print('\n[guided local search algorithm]')

    # initialize current working data
    cur_work = Work(tsp)
    cur_work.copy(work)

    # guided local search
    start_time = cur_time = disp_time = time.time()
    cnt = 0
    while cur_time - start_time < time_limit:
        best_obj = work.obj
        # set coefficient of penalized distance
        # cur_work.alpha = PENALTY_RATIO * float(cur_work.length(tsp)) / float(len(cur_work.tour))
        # print("alpha: ",cur_work.alpha)
        # print("length: ",cur_work.length(tsp))
        # print("len tour: ",len(cur_work.tour))
        # local search algorithm
        two_opt_search(tsp, work, cur_work)
        # update penalty
        update_penalty(tsp,cur_work)
        cnt += 1
        cur_time = time.time()
        if work.obj < best_obj:
            print('{}\t{}*\t{}\t{:.2f}'.format(cnt,cur_work.obj,work.obj,cur_time-start_time))
        elif cur_time - disp_time > INTVL_TIME:
            print('{}\t{}\t{}\t{:.2f}'.format(cnt,cur_work.obj,work.obj,cur_time-start_time))
            # print("HOLA")
            disp_time = time.time()

    # print tour length
    print('length= {}'.format(work.obj))

def two_opt_search(tsp, work, cur_work):
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

    # 2-opt neighborhood search
    improved = False
    restart = True
    while restart:
        restart = False
        nbhd = ((u,v)
                for u in work.tour
                for v in (tsp.neighbor)[u])
        for u,v in nbhd:
            # evaluate difference in original distance
            delta = eval_diff(tsp, cur_work, u, v, 'dist')
            if cur_work.obj + delta < work.obj - NUM_EPSILON:
                # update incumbent tour
                work.copy(cur_work)
                change_tour(tsp, work, u, v)
            # evaluate difference in penalized cost
            delta = eval_diff(tsp, cur_work, u, v, 'pdist')
            if delta < -NUM_EPSILON:
                # change current tour
                change_tour(tsp, cur_work, u, v)
                improved = True
                restart = True
                break
    return improved

# --------------------------------------------------------------------
#   main
# --------------------------------------------------------------------
def main(argv=sys.argv):
    # set starting time
    start_time = time.time()

    # read instance
    tsp = Tsp()
    tsp.read("qa194.tsp")
    tsp.write()

    # construct neighbor-list
    tsp.gen_neighbor()

    # solve TSP
    work = Work(tsp)
    nearest_neighbor(tsp, work)  # nearest neighbor algorithm
    guided_local_search(tsp, work, 30)  # guided local search
    work.write(tsp)

    # set completion time
    end_time = time.time()

    # display computation time
    print('\nTotal time:\t%.3f sec' % (end_time - start_time))


# main ---------------------------------------------------------------
if __name__ == "__main__":
    main()