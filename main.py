# This holds memoized state values.
values = {
  (0, 0): 0
}


# Return the successor states to the specified state, along with their
# associated transition probabilities.
# The return value is an array of tuples of the form ((g', r'), p), where (g', r')
# is a successor state of (g, r), and p is the probability of transitioning to it from (g, r).
def successors(g, r):
  states      = []
  num_marbles = float(g + r)         # Need to convert to float for divisions below.

  if g > 0:
    p_green = g / num_marbles        # Probability of withdrawing a green marble from the urn.
    states.append(((g-1, r), p_green))

  if r > 0:
    p_red = r / num_marbles          # Probability of withdrawing a red marble from the urn.
    states.append(((g, r-1), p_red))

  return states


# Calculate the value of the specified state, using memoization to retrieve previously calculated values.
def value(g, r):
  if (g, r) not in values:
    continuation_value = sum([value(*s)*p for s, p in successors(g, r)])
    stop_value         = g - r
    values[(g, r)]     = max(stop_value, continuation_value)

  return values[(g, r)]

# Solve this particular board state.
print value(2, 2)
