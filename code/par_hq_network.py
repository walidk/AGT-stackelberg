import random
from pylab import copy, linspace, array

MODE_FF = 0
MODE_C = 1

def link_state(flow,mode):
  return (flow,mode)

def state_flow(state):
  return state[0]

def state_mode(state):
  return state[1]

def is_state_ff(state):
  return state_mode(state) == MODE_FF

def par_link(a,b,c):
  return (a,b,c)

def link_a(link):
  return link[0]

def link_b(link):
  return link[1]

def link_c(link):
  return link[2]

def par_network(links):
  return ordered_links(links)

def network_link(network,lid):
  return network[lid]

def link_latency(link,state):
  return link_a(link) if is_state_ff(state) else link_b(link)*(1./state_flow(state) -1./link_c(link)) + link_a(link)

def network_latency(network,states):
  if states is None:
    return 0
  return sum([link_latency(link,state)*state_flow(state) for link, state in zip(network,states)])

def network_capacity(network):
  return sum([link_c(link) for link in network])

def social_optimum(network,r):
  n = n_links(network)
  flows = [0]*n
  modes = [MODE_FF]*n
  flow_remaining = r
  for i, link in enumerate(network):
    c = link_c(link)
    if c > flow_remaining:
      flows[i] = flow_remaining
      return [link_state(*pair) for pair in zip(flows,modes)]
    flows[i] = c
    flow_remaining-=c
  raise Exception('too much flow')
  
def social_optimum_range(network,r_range):
    new_flow = [0.]*n_links(network)
    j = 0
    last_flow_amount = 0
    last_cap = link_c(network_link(network,j))
    states = []
    steps = [x - y for x,y in zip(r_range,[0] + list(r_range[:-1]))]
    for step in steps:
        new_flow = copy(new_flow)
        while True:
            if last_cap - last_flow_amount > step:
                last_flow_amount+=step
                new_flow[j]=last_flow_amount
                break
            new_flow[j]=last_cap
            step-=(last_cap - last_flow_amount)
            j+=1
            if j == n_links(network):
                raise Exception('not enough cap')
            last_flow_amount = 0
            last_cap = link_c(network_link(network,j))
        states.append([link_state(flow,MODE_FF) for flow in new_flow])
    return states
        
        

def ne_capacity(network):
  top_link = network[-1]
  sums = link_c(top_link)
  for link in network[:-1]:
    sums+=flow_hat(link,top_link)
  return sums

def ordered_links(links):
  return sorted(links,key=link_a)

def n_links(network):
  return len(network)

def flow_hat(l1,l2):
  return link_b(l1)*link_c(l1)/(link_c(l1)*(link_a(l2) - link_a(l1)) + link_b(l1))

def ne_link_j_free_flow(network,r,j):
  if j == n_links(network):
    return ne_congested(network,r)
  flow_remaining = r
  flows = []
  modes = []
  ff_link = network_link(network,j)
  for i in range(n_links(network)):
    if i < j:
      link = network_link(network,i)
      flow = flow_hat(link,ff_link)
    elif i == j:
      flow = flow_remaining
    else:
      flow = 0
    flows.append(flow)
    modes.append(MODE_C if i < j else MODE_FF)
    flow_remaining-=flow
  
  return [link_state(flow,mode) for flow,mode in zip(flows,modes)]

def price_of_anarchy(network,r):
  return network_latency(network,best_ne(network, r))/network_latency(network,social_optimum(network, r))

def ne_congested(network,r):
  raise Exception('not implemented')

def all_ne(network,r):
  return filter(lambda ne: ne_valid(network,ne),[ne_link_j_free_flow(network,r,j) for j in range(n_links(network))])

def state_valid(link,state):
  result = 0 <= state_flow(state) <= link_c(link)
  return result

def ne_valid(network,ne):
  return all(state_valid(link,state) for link,state in zip(network,ne))

def best_ne(network,r):
  for j in range(n_links(network)):
    ne = ne_link_j_free_flow(network,r,j)
    if ne_valid(network,ne):
      return ne
  raise Exception('NOT A VALID DEMAND')
  
def best_ne_range(network,r_range):
    j = 0
    nes = []
    for r in r_range:
        while True:
            ne = ne_link_j_free_flow(network,r,j)
            if ne_valid(network,ne):
                nes.append(ne)
                break
            j+=1
            if j == len(network):
                raise Exception('not a valid flow')
    return nes
                
def stackelberg_range(network, r_range,alpha):
    nc_states = best_ne_range(network,[(1.-alpha)*r for r in r_range])
    return [optimal_stackelberg(network,r,alpha,nc_state) for r,nc_state in zip(r_range,nc_states)]
    
def stackelberg_ranges(network,r_range,alpha_range):
    return [stackelberg_range(network,r_range,alpha) for alpha in alpha_range]

def random_link(mean_a,mean_b,mean_c):
  return par_link((1+random.random())*mean_a,(1+random.random())*mean_b,(1+random.random())*mean_c)
  
def random_network(n_links):
  MEAN_FFS, MEAN_BWS, MEAN_CAP = 1.,4., 5.
  return par_network([random_link(MEAN_FFS,MEAN_BWS,MEAN_CAP) for i in range(n_links)])
  
def network_demands(network,N_POINTS=1000):
    return linspace(0.01,ne_capacity(network)*(1-.01),N_POINTS)
    
def network_profile(network,alphas,N_POINTS=1000):
    demands = network_demands(network,N_POINTS)
    return stackelberg_ranges(network,demands,alphas)
    
def profile_latencies(network,profiles):
    return [array([network_latency(network,ne) for ne in profile]) for profile in profiles]

def optimal_stackelberg(network, r, alpha,nc_states = None):
  comp_flow = alpha*r
  nc_flow = r - comp_flow
  if nc_states is None:
      nc_states = best_ne(network, nc_flow)
  for i, state in enumerate(nc_states):
    if is_state_ff(state):
      ff_link_ind = i
      break
  modes = map(state_mode,nc_states)
  nc_flows = map(state_flow,nc_states)
  comp_flows = [0.]*n_links(network)
  remaining_flow = comp_flow
  for i in range(ff_link_ind,n_links(network)):
    potential_flow = link_c(network_link(network,i)) - nc_flows[i]
    if potential_flow > remaining_flow:
      comp_flows[i] = remaining_flow
      return [link_state(c_flow + nc_flow, mode) for (c_flow,nc_flow),mode in zip(zip(comp_flows,nc_flows),modes)]
    comp_flows[i] = potential_flow
    remaining_flow-=potential_flow
  raise Exception('TOO MUCH FLOW')
