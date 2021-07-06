from gym.envs.registration import register

register(
    id='lorenz-oscillator-discrete-v0',
    entry_point='lorenz.envs:LorenzOscillatorDiscrete',
)

register(
    id='lorenz-stabilizer-discrete-v0',
    entry_point='lorenz.envs:LorenzStabilizerDiscrete',
)

# register(
#     id='lorenz-stabilizer-easy-v0',
#     entry_point='gym_lorenz.envs:LorenzStabilizerEasy',
# )
