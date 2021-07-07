from gym.envs.registration import register

register(
    id='pendulum-modified-v0',
    entry_point='pendulum.envs:PendulumModified',
)
