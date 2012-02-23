import pylab
fig_width_pt = 300.0  # Get this from LaTeX using \showthe\columnwidth
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
from par_hq_network import *

def plot_link(link,name='anon', style = None):
  flows = list(linspace(0,link_c(link),50)) + list(pylab.linspace(link_c(link),link_c(link)/3.,50))
  modes = [MODE_FF]*50 + [MODE_C]*50
  if style is None:
    pylab.plot(flows,
         [link_latency(link,link_state(flow,mode)) 
         for flow, mode 
         in zip(flows,modes)],label=name)
  else:
    pylab.plot(flows,
         [link_latency(link,link_state(flow,mode)
          )       for flow, mode 
                  in zip(flows,modes)],
                  style,
                  label=name)


def plot_network(network, names = None, styles = None):
  if names is None:
    names = map(str(range(1,len(network)+1)))
  if styles is not None:
    [plot_link(link,name, style=style) for link, name,style in zip(network,names, styles)]
  else:
    [plot_link(link,str(i)) for link, name in zip(network,names)]
  pylab.legend(loc='upper right')

def plot_network_profile(network,alphas,N_POINTS=1000):
    profiles = network_profile(network,alphas + [1.],N_POINTS)
    latencies = profile_latencies(network,profiles)
    so = latencies[-1]
    [plot(latency/so) for latency in latencies[:-1]]

if __name__ == "__main__":
  pass
