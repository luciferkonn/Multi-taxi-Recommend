"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Author : James Arambam
Date   : 30 Mar 2017
Description :
Input :
Output :
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

import mdptoolbox.example
import numpy as np

# ============================================================================ #


class tidcmdp:

    def __init__(self, agents, states, actions):

        self.agents = agents
        self.states = states
        self.actions = actions
        self.P1, _ = mdptoolbox.example.rand(states, actions)
        self.P2, _ = mdptoolbox.example.rand(states, actions)
        self.R = np.random.rand(self.states, self.states, self.actions, self.actions, self.states, self.states)



