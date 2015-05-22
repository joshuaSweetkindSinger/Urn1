#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import mul

N = 20 # Capacity

# A game state is denoted (g, r), where
# g and r are the number of green and red marbles respectively that have already been extracted.
# The hash below holds memoized values for game states. Its keys are game states and its values are floats.
values = {}

# This hash holds memoized values for the probability of drawing a green marble from the urn,
# given that the current game state is (g, r). Its keys are game states and its values are floats
# between 0 and 1.
green_transition_probabilities = {}


# This hash holds memoized values for the probability of visiting a particular game state (g, r).
# Its keys are game states and its values are probabilities. If the game state (g, r) has probability p,
# this means that the probability of visiting that game state sometime during the game is p.
state_probabilities = {
  (0, 0): 1
}


# Return n-choose-k.
def choose(n, k):
  if k > n-k:
    k = n-k
  return float(reduce(mul, range((n-k+1), n+1), 1) / reduce(mul, range(1, k+1), 1))


# Pr[S = (g, r) | G = num_green] = (num_ways_to_choose_g_green) * (num_ways_to_choose_r_red) / (num_ways_to_choose_g+r)
def pr_state_given_composition(g, r, num_green):
  return choose(num_green, g) * choose(N - num_green, r) / choose(N, g + r)


# Pr[S = (g, r)] =  Σ Pr[G = num_green] * Pr[S = (g, r) | G = num_green]
# = (1/(N+1))Σ Pr[S = (g, r) | G = num_green]
def pr_state(g, r):
  if (g, r) not in state_probabilities:
    state_probabilities[(g, r)] = sum([pr_state_given_composition(g, r, num_green) for num_green in range(N+1)]) / (N + 1)

  return state_probabilities[(g, r)]


# Pr[G = num_green | S = (g, r)] = Pr[G = num_green, S = (g, r)] / Pr[S = (g, r)]
# = Pr[G = num_green]*Pr[S = (g, r) | G = num_green] / Pr[S = (g, r)]
# = Pr[S = (g, r) | G = num_green] / ((N+1) * Pr[S = (g, r)] )
def pr_composition_given_state(g, r, num_green):
  return pr_state_given_composition(g, r, num_green) / (pr_state(g, r) * (N + 1))


# Pr[X = green | S = (g, r), G = num_green] where G = original number of green marbles in urn
def green_prob_given_composition_and_state(g, r, num_green):
  return (num_green - g) / (N - r - g)


# Pr[X = green | S = (g, r)] = Σ_(num_green=0,N) Pr[G = num_green | S = (g, r)] * Pr[X = green | S = (g, r), G = num_green]
def green_prob(g, r):
  if (g, r) not in green_transition_probabilities:
    green_transition_probabilities[(g, r)] = sum([pr_composition_given_state(g, r, num_green) * green_prob_given_composition_and_state(g, r, num_green) for num_green in range(N+1)])

  return green_transition_probabilities[(g, r)]


# Return an array consisting of the two successor states of the state (g, r), along with
# their associated transition probabilities. There are always exactly two successor states:
# one corresponding to removing a red marble, and the other corresponding to removing a green marble.
# Example: successors(g,r) => [((g-1, r), p1), ((g, r-1), p2)]
# Note: It is possible that one of the two successor states will have 0 probability, if there is only
# one color of marble left.
def successors(g, r):
  states = []

  # There are marbles left in urn, so this state has successors.
  if g + r < N:
    p_green = green_prob(g, r)
    p_red   = 1 - p_green

    states.append(((g+1, r), p_green))
    states.append(((g, r+1), p_red))

  return states


# Returns the value of the game state (g, r).
def value(g, r):
  stop_value         = g - r
  continuation_value = sum([value(*s) * p for s, p in successors(g, r)]) if g + r < N else stop_value

  if (g, r) not in values:
      values[(g, r)]  = max(stop_value, continuation_value)

  return values[(g, r)]

print value(0, 0)
