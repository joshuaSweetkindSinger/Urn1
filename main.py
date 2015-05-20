# States are represented as tuples of green/red marbles extracted respectively.
values = {
  #(0, 0): 0
}

# Returns not only successor states, but also probabilities (in 3ples).
def successors(g, r, capacity):
  states = []
  if g + r != capacity:
    num_extracted = g + r
    num_compositions = capacity + 1 - g - r
    num_remaining = capacity - num_extracted
    p_green = float(sum(range(num_remaining))) / (num_compositions * num_remaining)
    states.append((g+1, r, p_green))
    p_red = 1 - p_green
    states.append((g, r+1, p_red))
  return states

def value(g, r, capacity):
  stop_value = g - r
  continuation_value = stop_value
  if g + r != capacity:
    successor_states = successors(g, r, capacity)
    continuation_value = sum([value(s[0], s[1], capacity)*s[2] for s in successor_states])
  if (g, r) not in values:
    values[(g, r)] = max(stop_value, continuation_value)
  return values[(g, r)]

print value(0, 0, 20)
