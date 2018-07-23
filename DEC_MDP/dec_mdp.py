# """
# @author: Jikun Kang
# """
# import numpy as np
# import mdp
# from aug_mdp import AugMDP
# from mdp import MDP
# from database_operate import Pfind
#
# def intersect(planes, boundaries):
#     pass
#
#
# def coverage_set(MDP, ro):
#     planes = {} # planes are equivalent to policies
#     poins = {}
#     # initialize boundaries of parameter space
#     for n in range(1, len(ro)+1):
#         boundaries = {}
#
#     # loop until no new optimal policies found
#     while len(newplanes) > 0:
#         newplanes = {}
#         points = intersect(planes, boundaries)
#         # get optimal plane at each point
#         for point in points:
#             plane = solve(augment(MDP, point, ro))
#             if plane not in planes:
#                 newplanes = newplanes + plane
#         planes = planes + newplanes
#     return planes
#
#
# def indicator(e, E):
#     if e in E:
#         return 1
#     else:
#         return 0
#
#
# def augment(MDP, policy, ro):
#     rewards = MDP.rewards + np.multiply(np.multiply(indicator(e, E[k]), ro[:, 3]), MDP.prs)
#     aMDP = AugMDP(MDP.states, MDP.actions, MDP.prs, rewards, policy, ro)
#     return aMDP
#
#
# def value(grid, policy):
#     v_star = (1 - Pfind[grid.x][grid.y])* value(grid, policy) + Pfind[grid.x][grid.j] * 10
#     return v_star
#
#
# def P(e, policy):
#     # pr(si|PIi) * pr(ai|si,PIi) * pr(si'|si, ai)
#
#
# def Po(events, policy):
#     val = 0
#     for e in events:
#         val = val + P(e, policy)
#     return val
#
#
# def jv(ro, policy1, policy2):
#     joint_value = 0
#     for i in E:
#         joint_value = joint_value + Po(ro.e1[i], policy1) * Po(ro.e2[i], policy2) * ro.c[i]
#
#
# def gv(policy1, policy2, MDP1, MDP2, ro):
#     global_value = value(MDP1.state.grid, policy1) + value(MDP2.states.grid, policy2) + jv(ro, policy1, policy2)
#     return global_value
#
#
# def solve(param):
#     pass
#
#
# def csa(MDP1, MDP2, ro):
#     optset = coverage_set(MDP1, ro)
#     value = float("-inf")
#     joint_policy = {}
#     for policy1 in optset:
#         policy2 = solve(augment(MDP2,policy1, ro))
#         v = gv(policy1, policy2, MDP1, MDP2, ro)
#         if v > value:
#             value = v
#             joint_policy = {policy1, policy2}
#     return joint_policy
#
