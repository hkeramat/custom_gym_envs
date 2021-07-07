# `pendulum-modified-v0`

Continuous pendulum environment with reduced initial state variability. In the original environment, the initial states are:

```
high = np.array([np.pi, 1])
self.state = self.np_random.uniform(low=-high, high=high)
```

Here, they are reduced to:

```
high = 0.1*np.array([np.pi, 1])
self.state = np.array([-np.pi/2.0, 0.0]) + self.np_random.uniform(low=-high, high=high)
```

Below is an example of training with an in-house PPO method.

<p align="center">
  <img width="900" alt="" src="save/ppo.png">
</p>
