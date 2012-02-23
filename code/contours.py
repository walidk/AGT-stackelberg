from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
from visual import *
import pylab

fig_width_pt = 350.0  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (pylab.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
params = {'backend': 'ps',
  'axes.labelsize': 10,
  'text.fontsize': 10,
  'legend.fontsize': 10,
  'xtick.labelsize': 10,
  'ytick.labelsize': 10,
  'text.usetex': True,
  'figure.figsize': fig_size}
pylab.rcParams.update(params)

b = 20000
link_101 = par_link(60, b*1.5, 600)
link_280 = par_link(70, b, 450)
link_101_280 = par_link(80, b*.5, 350)
link_580 = par_link(105, b, 800)
network = par_network([link_101, link_280, link_101_280, link_580])
N_DEMAND = 300
N_ALPHA = 300
demands = np.linspace(500,ne_capacity(network)*.99,N_DEMAND)
alphas = np.linspace(0,.8,N_ALPHA).tolist()
X, Y = np.meshgrid(demands, alphas)
profiles = network_profile(network,alphas+[1.],demands=demands)
latencies = profile_latencies(network,profiles)
latencies = [lat/latencies[-1] for lat in latencies[:-1]]
if True:
    pylab.clf()
    ax = pylab.contourf(X, Y, latencies,40,cmap=cm.hot)
    ax.ax.set_xlabel('Demand (cars/min)')
    ax.ax.set_ylabel('Fractional Compliance ($\\alpha$)')
    pylab.colorbar(ax)
    pylab.subplots_adjust(bottom=.13, right=.75)
    pylab.savefig('../figures/POSContour.pdf')
if False:
    pylab.clf()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, latencies, rstride=15, cstride=15, color='b', antialiased=True)
    ax.set_xlabel('Demand ($r$)')
    ax.set_ylabel('Fractional Compliance ($\\alpha$)')
    ax.set_zlabel('Price of Stability')
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    plt.savefig('../figures/POS3d.pdf')
