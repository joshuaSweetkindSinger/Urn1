#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import mul

N = 20 # Capacity

# States are represented as tuples of green/red marbles extracted respectively.
values = {}

g_transition_probabilities = {}
state_probabilities = {
  (0, 0): 1
}

def C(n, r):
  if r > n-r:
    r = n-r
  return float(reduce(mul, range((n-r+1), n+1), 1) / reduce(mul, range(1, r+1), 1))

# Pr[S = (g, r)]
def pr_state(g, r):
  if (g, r) not in state_probabilities:
    # Σ Pr[G = k] * Pr[S = (g, r) | G = k]
    state_probabilities[(g, r)] = sum([pr_state_given_composition(g, r, k) for k in range(N+1)]) / (N + 1)
  return state_probabilities[(g, r)]

# Pr[S = (g, r) | G = k]
def pr_state_given_composition(g, r, G):
  return C(G, r) * C(N - r, g) / C(N, g + r)

# Pr[G = k | S = (g, r)]
def pr_composition_given_state(g, r, G):
  return pr_state_given_composition(g, r, G) / (pr_state(g, r) * (N + 1))

# Pr[X = green | S = (g, r), G = k] where G = green marbles in urn
def pr_g_transition_given_composition(g, r, G):
  return (G - r) / (N - r - g)

# Pr[X = green | S = (g, r)]
def pr_g_transition(g, r):
  if (g, r) not in g_transition_probabilities:
    # Σ Pr[G = k | S = (g, r)] * Pr[X = green | S = (g, r), R = k]
    g_transition_probabilities[(g, r)] = sum([pr_composition_given_state(g, r, k) * pr_g_transition_given_composition(g, r, k) for k in range(N+1)])
  return g_transition_probabilities[(g, r)]

# Returns not only successor states, but also probabilities (in 3ples).
def successors(g, r):
  states = []
  if g + r != N:
    p_green = pr_g_transition(g, r)
    states.append(((g+1, r), p_green))
    p_red = 1 - p_green
    states.append(((g, r+1), p_red))
  return states

def value(g, r):
  stop_value = g - r
  continuation_value = stop_value
  if g + r != N:
    successor_states = successors(g, r)
    continuation_value = sum([value(*s[0])*s[1] for s in successor_states])
  if (g, r) not in values:
    values[(g, r)] = max(stop_value, continuation_value)
  return values[(g, r)]

print value(0, 0)
