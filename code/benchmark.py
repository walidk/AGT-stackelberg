from par_hq_network import *
import time
import numpy

N_LINKS = [3,10,50]

N_DEMAND = 50

N_ALPHAS = [1,10,100]

N_REPEATS = 10

benchmarks = []

disp_info = lambda nl, na, nr: '%i %i %i' % (nl , na, nr)

for nl in N_LINKS:
	for na in N_ALPHAS:
		avg = 0
		for nr in range(N_REPEATS):
			network = random_network(nl)
			print disp_info(nl, na, nr)
			tic = time.clock()
			network_profile(network, linspace(0,1,na),N_DEMAND)
			toc = time.clock()
			print toc - tic
			avg+=toc - tic
		avg/=nr
		benchmarks.append((nl,na,avg))
