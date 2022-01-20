from envs.pendulum import *

p = PendulumDeterministic()

p.reset()
for i in range(200):
    p.step([0.0])
    p.render()
