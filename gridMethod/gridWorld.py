from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt

WORLD_SIZE = 100
REWARD = -1.0
ACTION_PROB = 0.1111

# left, up, right, down
actions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'ST']

THETA = 1e-9

states = np.zeros((WORLD_SIZE, WORLD_SIZE))


def one_step_lookahead(state, V):
    A = np.zeros(len(actions))
    for a in range(len(actions)):
        A[a] = prob * (reward + discount_factor * V[next_state])
    return A

while True:
    delta = 0
    for s in range(10000):
        A = one_step_lookahead(s, V)
