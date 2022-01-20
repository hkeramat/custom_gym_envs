from gym.envs.registration import register

register(
    id='pendulum-deterministic-v0',
    entry_point='pendulum.envs:PendulumDeterministic',
)
