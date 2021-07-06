# `cartpole-continuous-v0`

Continuous cartpole environment solved with an in-house PPO method. The policy exploits a normal law as pdf. The rest of the environment is similar to the original one.

<p align="center">
  <img width="900" alt="" src="save/ppo.png">
</p>

```
Observation:
        Type: Box(4)
        Num     Observation               Min                     Max
        0       Cart Position             -4.8                    4.8
        1       Cart Velocity             -Inf                    Inf
        2       Pole Angle                -0.418 rad (-24 deg)    0.418 rad (24 deg)
        3       Pole Angular Velocity     -Inf                    Inf
Actions:
        Type: Box(1)
        Num   Action                      Min                     Max
        0     Push cart                   -1.0                    1.0
Reward:
        Reward is 1 for every step taken, including the termination step
Starting State:
        All observations are assigned a uniform random value in [-0.05..0.05]
Episode Termination:
        Pole Angle is more than 12 degrees.
        Cart Position is more than 2.4 (center of the cart reaches the edge of
        the display).
        Episode length is greater than 200.
Solved Requirements:
        Considered solved when the average return is greater than or equal to
        195.0 over 100 consecutive trials.
```
