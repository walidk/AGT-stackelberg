from par_hq_network import *
import time
import pylab
import multiprocessing

N_RUNS = 500
N_MIN = 3
N_MAX = 1500
MIN_DEMAND = .7
ALPHA = .4
DEMAND = .7


def sim_time(i):
    n = pylab.randint(N_MIN, N_MAX)
    alpha = ALPHA
    net = random_network(n)
    r = ne_capacity(net)*DEMAND
    tic = time.clock()
    optimal_stackelberg(net,r,alpha)
    val =  (n,time.clock() - tic)
    print val
    return val

if __name__ == '__main__':
    p = multiprocessing.Pool()
    results = p.map(sim_time,[.4]*100)
    N,RT = zip(*results)
    pylab.scatter(N,RT)
    pylab.show()
