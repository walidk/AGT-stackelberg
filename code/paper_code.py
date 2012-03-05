from visual import *
from par_hq_network import *
import pylab

fig_path = lambda fn:  '../figures/%s.pdf' % fn

b = 20000
link_101 = par_link(60, b*1.5, 600)
link_280 = par_link(70, b, 450)
link_101_280 = par_link(80, b*.5, 350)
link_580 = par_link(105, b, 800)
network = par_network([link_101, link_280, link_101_280, link_580])
N_POINTS = 1000
demands = linspace(0,ne_capacity(network),N_POINTS)
alphas = [0., .05,  .15, .5]
profiles = network_profile(network,alphas + [1.],N_POINTS)
latencies = profile_latencies(network,profiles)
styles = ['-','g--','r-.', 'm:']
names = ['I-101','I-280','I-880','I-580']
plot_network(network,names, styles)
pylab.ylim([55,140])
pylab.xlim([0,900])
pylab.legend(loc='lower right')
# pylab.show()
pylab.savefig(fig_path('LatenciesSim'))
pylab.clf()
so = latencies[-1]
[pylab.plot(latency/so,style,label='$\\alpha=$%s' % str(alpha)) 
 for latency, style, alpha in zip(latencies[:-1],
                                  styles,
                                  alphas)]
pylab.legend(loc='upper left')
# pylab.show()
pylab.savefig(fig_path('POSSim'))

pylab.clf()
ne = latencies[0]
[pylab.plot(ne/latency,style,label='$\\alpha=$%s' % str(alpha)) 
 for latency, style, alpha in zip(latencies[1:-1],
                                  styles[1:],
                                  alphas[1:])]
pylab.legend(loc='lower left')
pylab.savefig(fig_path('VOASim'))
#pylab.show()
