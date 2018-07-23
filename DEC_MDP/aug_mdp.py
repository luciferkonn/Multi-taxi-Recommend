"""
@author: Jikun Kang
"""


class AugMDP:
    def __init__(self, states, actions, prs, rewards, pi, ro):
        self.states = states
        self.actions = actions
        self.prs = prs
        self.rewards = rewards
        self.pi = pi
        self.ro = ro
