"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Author : James Arambam
Date   : 30 Mar 2017
Description :
Input : 
Output : 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

# ================================ priImports ================================ #

import sys
import os
import platform
from pprint import pprint
import time
from tidcmdp import tidcmdp


print "# ============================ START ============================ #"

# ============================================================================ #

# --------------------- Variables ------------------------------ #

ppath = os.getcwd() + "/"  # Project Path Location

# -------------------------------------------------------------- #


def main():

    agents = 2
    states = 3
    actions = 2
    mdp = tidcmdp(agents, states, actions)
    print mdp.P1.shape, mdp.P2.shape, mdp.R.shape

# =============================================================================== #

if __name__ == '__main__':
    main()
    print "# ============================  END  ============================ #"