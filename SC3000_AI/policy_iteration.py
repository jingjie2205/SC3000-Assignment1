import numpy as np

class PolicyIteration:
    def __init__ (self, env):
        self.env = env
        self.gamma = 0.9
        self.V = np.zeros((env.height , env.width))
        # Converge threshold
        self.theta = 0.004
        # Initial policy - all direction to the right
        self.policy = np.full((self.env.height, self.env.width), '→', dtype=object)

    def policy_eval(self):
        while True:
            delta = 0
            # Loop through all states
            for s in self.env.get_states():
                # Skip if state is terminal or block
                if s == self.env.goal:
                    # For visualization purposes
                    self.policy[s] = '*'
                    continue    
                elif s in self.env.blocks:
                    # For visualization purposes
                    self.policy[s] = '■'
                    continue

                v_old = self.V[s[0], s[1]]

                # Get action from policy π
                a = self.env.action_map[self.policy[s[0]][s[1]]]
                # Get reward and next state after taking action a under policy π
                reward, next_s = self.env.transition(s, a)
                # Calculate value function for taking policy π
                self.V[s[0], s[1]] = reward + (self.gamma * self.V[next_s[0]][next_s[1]])

                delta = max(delta, abs(v_old - self.V[s[0], s[1]]))

            if delta < self.theta:
                break

    
    def policy_improv(self):
        policy_stable = True

        # Loop through all states
        for s in self.env.get_states():
            if s == self.env.goal or s in self.env.blocks:
                continue

            # Store Q value (up, down, left ,right) for state s
            q_value = []
            # Store old action
            old_action = self.policy[s]

            # Calculate Q value for all 4 actions
            for a in self.env.actions:
                # Get reward and next state after taking action a in state s
                reward, next_s = self.env.transition(s, a)

                # Deterministic action value
                action_value = reward + (self.gamma * self.V[next_s[0]][next_s[1]])
                # Store action value 
                q_value.append(action_value)

            # Convert highest action value to "↑", "↓", "←", "→"
            best_action_idx = np.argmax(q_value)
            
            # Update policy
            self.policy[s] = self.env.action_names[best_action_idx]

            # Check if action changed
            if old_action != self.policy[s]:
                policy_stable = False

        return policy_stable

    def solve(self):
        while True:
            self.policy_eval()
            policy_stable = self.policy_improv()
            if policy_stable:
                break
