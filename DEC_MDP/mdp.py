"""
@author: Jikun Kang
"""
import numpy as np
grid_size = 100
find_pr = np.zeros((grid_size, grid_size)) # read from text file
reward_each_step = 10


class MDP(object):

    def __init__(self, state_sapce, action_space, prs, reward):
        self.state_space = state_sapce
        self.action_space = action_space
        self.prs = prs
        self.reward = reward
        self.action_prob = 1/9

    def get_next_state(self, state, action):
        nextStateGrid = []
        for i in range(0, grid_size):
            nextStateGrid.append([])
            for j in range(0, grid_size):
                next = dict()
                if i == 0:
                    next['N'] = next['NE'] = next['NW'] = [i, j]
                else:
                    next['N'] = [i - 1, j]
                    next['NE'] = [i - 1, j + 1]
                    next['NW'] = [i - 1, j - 1]
                if i == grid_size - 1:
                    next['S'] = next['SW'] = next['SE'] = [i, j]
                else:
                    next['S'] = [i + 1, j]
                    next['SE'] = [i + 1, j + 1]
                    next['SW'] = [i + 1, j - 1]
                if j == 0:
                    next['W'] = next['NW'] = next['SW'] = [i, j]
                else:
                    next['W'] = [i, j - 1]
                    next['NW'] = [i - 1, j - 1]
                    next['SW'] = [i + 1, j - 1]
                if j == grid_size - 1:
                    next['E'] = next['NE'] = next['SE'] = [i, j]
                else:
                    next['E'] = [i, j + 1]
                    next['NE'] = [i - 1, j + 1]
                    next['SE'] = [i + 1, j + 1]
                next['T'] = [i, j]  # stay in the same grid
                nextStateGrid[i].append(next)
        return self.action_prob, nextStateGrid[state.gridX][state.gridY][action], 1

    # @staticmethod
    # def get_reward(grid):
    #     # reward = (1 - find_pr[state.gridX][state.gridY])
    #     reward = find_pr[grid]*reward_each_step
    #     return reward

