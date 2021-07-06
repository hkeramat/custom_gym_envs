# Generic imports
from gym                    import spaces

# Custom imports
from lorenz.envs.lorenz_env import Lorenz

###############################################
### Discrete lorenz oscillator class
class LorenzOscillatorDiscrete(Lorenz):

    # Initialize instance
    def __init__(self):

        super().__init__()
        self.set_action_space()
        self.set_name()

    # Set name
    def set_name(self):

        self.name = 'lorenz_oscillator_discrete'

    # Set action space
    def set_action_space(self):

        self.act          = [-1.0, 0.0, 1.0]
        self.action_space = spaces.Discrete(len(self.act))

    # Stepping with possible action
    def step(self, a=1):

        u = self.act[a]
        return self.step_physical(u)

    # Compute reward
    def get_rwd(self, x_prv, x):

        rwd = 0.0 + (x_prv*x < 0.0)*1.0

        return rwd
