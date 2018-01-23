import numpy as np


def coverage_set(MDP, ro):
    pass


def solve_augment(MDP, policy, ro):
    pass


def csa (MDP1, MDP2, ro):
    optset = coverage_set(MDP1, ro)
    value = float("-inf")
    joint_policy = {}
    for policy1 in optset:
        policy2 = solve_augment(MDP2,policy1, ro)