class GridWorld:
    def __init__(self):
        self.height = 5
        self.width = 5
        self.goal = (0, 4)
        self.initial_state = (4, 0)
        self.blocks = [(2, 1), (2, 3)]
        self.actions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
        self.action_names = ["↑", "↓", "←", "→"]
        self.action_map = dict(zip(self.action_names, self.actions)) # map "↑", "↓", "←", "→" into [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.step_cost = -1.0
        self.goal_reward = 10.0

    def get_states(self):
        return [ (r,c) for r in range(self.height) for c in range(self.width) ]

    # Deterministic Transition - 100% take action
    def transition (self, state, action):
        # Terminal State
        if state == self.goal:
            return [0.0, state]

        next_s = ( state[0] + action[0], state[1] + action[1] )
        
        # Boundary & Block Checking
        if ( 0 <= next_s[0] < self.height and 
             0 <= next_s[1] < self.width and 
             next_s not in self.blocks ):
            # Legal next state
            target = next_s
        else:
            # Boundary violation remain in same state
            target = state

        reward = self.goal_reward if target == self.goal else self.step_cost
        
        # Return transition reward and next state
        return reward, target