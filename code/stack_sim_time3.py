from simplejson import load
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


#with open('sim_time.json','r') as fn:
with open('demand_data.json','r') as fn:
    (N,RT),(N2,RT2),(N3,RT3) = load(fn)
pylab.scatter(N,RT)
pylab.hold(True)
pylab.scatter(N2,RT2,c='r')
pylab.scatter(N3,RT3,c='g')
pylab.xlabel('Number of Links')
pylab.ylabel('Run Time (s)')
pylab.legend(map(lambda x: 'demand = %.1f*max demand' % x,[.4,.2,.1]),loc='upper left')
pylab.show()

