from par_hq_network import *
import time
import pylab
import multiprocessing

N_RUNS = 1000
N_MIN = 200
N_MAX = 1000
MIN_DEMAND = .7



def sim_time(i):
    n = pylab.randint(N_MIN, N_MAX)
    alpha = pylab.rand()
    net = random_network(n)
    r = ne_capacity(net)*((1-MIN_DEMAND)*pylab.rand() + MIN_DEMAND)
    tic = time.clock()
    optimal_stackelberg(net,r,alpha)
    val =  (n,time.clock() - tic)
    print val
    return val

if __name__ == '__main__':
    p = multiprocessing.Pool()
    results = p.map(sim_time,[0]*N_RUNS)
    N,RT = zip(*results)
    pylab.scatter(N,RT)
    pylab.show()
