values = {
  (0, 0): 0
}

# Successors returns not only successor states, but also probabilities (a 3ple).
def successors(g, r):
  states = []
  num_marbles = float(g + r)
  if g > 0:
    p_green = g / num_marbles
    states.append((g-1, r, p_green))
  if r > 0:
    p_red = r / num_marbles
    states.append((g, r-1, p_red))
  return states

def value(g, r):
  if (g, r) not in values:
    continuation_value = sum([value(s[0], s[1])*s[2] for s in successors(g, r)])
    stop_value = g - r
    values[(g, r)] = max(stop_value, continuation_value)
  return values[(g, r)]

print value(2, 2)
