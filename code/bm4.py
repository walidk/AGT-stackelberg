from par_hq_network import *
import time
import pylab
import multiprocessing
import simplejson
N_RUNS = 500
N_MIN = 3
N_MAX = 1000
MIN_DEMAND = .7
ALPHA = .4
DEMAND = .7


def sim_time(dem_frac):
    n = pylab.randint(N_MIN, N_MAX)
    alpha = ALPHA
    net = random_network(n)
    r = ne_capacity(net)*dem_frac
    tic = time.clock()
    optimal_stackelberg(net,r,alpha)
    val =  (n,time.clock() - tic)
    print val
    return val

if __name__ == '__main__':
    p = multiprocessing.Pool()
    r1 = p.map(sim_time,[.4]*500)
    r2 = p.map(sim_time,[.2]*500)
    r3 = p.map(sim_time,[.1]*500)
    N,RT = zip(*r1)
    N2,RT2 = zip(*r2)
    N3,RT3 = zip(*r3)
    with open('demand_data.json','w') as fn:
        simplejson.dump(((N,RT),(N2,RT2),(N3,RT3)),fn)
