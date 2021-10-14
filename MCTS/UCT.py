import math

def UCT(w, n, N, c=math.sqrt(2)):
  """ 
  Calculate Upper Confidence Bound 
  w: number of wins
  n: number of simulations of the node
  N: number of simulations of the node's parent
  c: temperature
  """
  return w/n + c * math.sqrt(math.log(N) / n)