import numpy as np
import random
from env import GridWorld

class monte_carlo:
    def __init__(self, env):
        self.env = env
        self.epsilon = 0.1
        self.episodes = 40000 # Num of Episodes to run
        self.gamma = 0.9

        self.V = np.zeros((env.height , env.width))

        # Dict ( state, action ) as keys - [] as value for rewards
        self.returns = {}
        self.Q = {}

        for s in env.get_states():
            for a in env.actions:
                self.Q[ ( s, a ) ] = 0
                self.returns[ ( s, a ) ] = []

        # Policy of gridworld in terms of "↑", "↓", "←", "→"
        self.policy = np.full((self.env.height, self.env.width), ' ', dtype=object)

    def epsilon_greedy (self, state):
        # Explore randomly
        if np.random.random() < self.epsilon:
            return random.choice(self.env.actions)
        # Return highest Q value at current state
        else:
            q_values = [self.Q[ (state, action) ] for action in self.env.actions]
            return self.env.actions[np.argmax(q_values)]

    def generate_episode(self):
        # Random policy
        episode = []
        # Initial state of agent ( Bottom Right )
        state = (4, 0)
        
        while state != self.env.goal:
            # Choose a random action
            action = self.epsilon_greedy(state)
            # Store transition values
            reward, next_s = self.env.transition(state, action)

            # Appeend into policy
            episode.append((state, action, reward))
            # Move to next state
            state = next_s

        return episode

    def first_visit(self):
        for _ in range(self.episodes):
            G = 0
            # Set to track visited states
            visited = set()

            # Generate an episode (state, action, reward)
            random_policy = self.generate_episode()

            # Loop backwards
            for i in reversed(range(len(random_policy))):
                state, action, reward = random_policy[i]
                G = self.gamma * G + reward

                if ( state, action ) not in visited:
                    visited.add(( state, action ))

                    self.returns[( state, action )].append(G)
                    self.Q[( state, action )] = np.mean(self.returns[( state, action )])

    def extract_policy(self):
        for state in self.env.get_states():

            if state == self.env.goal: 
                    self.policy[state] = '*'
                    continue    
            elif state in self.env.blocks:
                self.policy[state] = '■'
                continue

            q_values = [self.Q[(state, a)] for a in self.env.actions]
            best_action = np.argmax(q_values)
            self.policy[state] = self.env.action_names[best_action]

    # def solve(self):

            
env = GridWorld()
mc = monte_carlo(env)

mc.first_visit()
mc.extract_policy()
print(mc.policy)