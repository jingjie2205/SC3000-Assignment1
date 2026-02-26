import numpy as np
import pandas as pd
import json

from env import GridWorld
from value_iteration import ValueIteration
from policy_iteration import PolicyIteration
from utils import plot_rl_comparison

env = GridWorld()
vi_agent = ValueIteration(env)
pi_agent = PolicyIteration(env)

vi_agent.solve()
pi_agent.solve()

plot_rl_comparison(vi_agent.V, vi_agent.policy, pi_agent.V, pi_agent.policy)
# print(vi_agent.V)
# print(pi_agent.V)