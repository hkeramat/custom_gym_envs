from gym.envs.registration import register

register(
    id='cartpole-continuous-v0',
    entry_point='cartpole.envs:CartPoleContinuous',
)
