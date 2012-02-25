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


with open('sim_time.json','r') as fn:
    N,RT = load(fn)
N = map(lambda x: x/1000.,N)
z =  pylab.polyfit(N,RT, 2)
pylab.scatter(N,RT)
pylab.hold(True)
tt = pylab.linspace(.2,1.,100)
pylab.plot(tt,map(pylab.poly1d(z), tt),'k',linewidth=2.)
pylab.annotate('$y = ({0:.3n}) x^2$'.format(z[0]),
            xy=(tt[50],pylab.poly1d(z)(tt[50])),
            xytext=(0.6, 0.7),
            textcoords='axes fraction',
            arrowprops=dict(facecolor='black', 
                            shrink=0.05),
            horizontalalignment='right', 
            verticalalignment='top',
            )
pylab.xlabel('# Links *1000')
pylab.ylabel('Run Time (s)')
pylab.show()

