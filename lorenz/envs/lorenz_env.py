# Generic imports
import os
import time
import gym
import numpy           as     np
from   gym             import spaces
from   scipy.integrate import odeint

###############################################
### Generic class
class Lorenz(gym.Env):
    metadata = {'render.modes': ['human']}

    # Initialize instance
    def __init__(self):

        # Main parameters
        self.sigma      = 10.0
        self.rho        = 28.0
        self.beta       = 8.0/3.0
        self.dt_act     = 0.5
        self.dt         = 0.025
        self.int_steps  = round(self.dt_act/self.dt)
        self.norm       = 100.0
        self.obs_norm   = 10.0
        self.t_max      = 25.0
        self.max_steps  = round(self.t_max/self.dt_act)
        self.init_time  = 5.0
        self.init_steps = round(self.init_time/self.dt_act)
        self.t0         =-self.init_time

        # Other attributes
        self.crt_step   = 0
        self.idx        =-1
        self.cpu        = 0
        self.n_cpu      = 1

        # Set observation space
        self.observation_space = spaces.Box(low=-self.norm,
                                            high=self.norm,
                                            shape=(6,))

    # Set name
    # Mandatory re-implementation in daughter class
    def set_name(self):
        pass
        #raise NotImplementedError:

    # Set action space
    # Mandatory re-implementation in daughter class
    def set_action_space(self):
        raise NotImplementedError

    # Set cpus and paths
    def set_cpu(self, cpu, n_cpu):

        # Set nb of cpus and index
        self.cpu   = cpu
        self.n_cpu = n_cpu
        self.idx   =-cpu-1

        # Handle paths
        res_path = self.name
        if (self.cpu == 0):
            os.makedirs(res_path, exist_ok=True)
        t         = time.localtime()
        path_time = time.strftime("%H-%M-%S", t)
        self.path = res_path+'/'+str(path_time)
        if (self.cpu == 0):
            os.makedirs(self.path, exist_ok=True)

    # Reset variables
    def reset(self):

        # Update index for output
        self.idx  += self.n_cpu

        # Initial point
        self.x0    = 10.0
        self.y0    = 10.0
        self.z0    = 10.0

        # Init values and lists
        self.t     = self.t0
        self.x     = self.x0
        self.y     = self.y0
        self.z     = self.z0
        self.u     = 0.0
        self.vx    = 0.0
        self.vy    = 0.0
        self.vz    = 0.0

        self.lst_t  = []
        self.lst_x  = []
        self.lst_y  = []
        self.lst_z  = []
        self.lst_vx = []
        self.lst_vy = []
        self.lst_vz = []
        self.lst_u  = []

        self.lst_store()

        # Run several steps before starting control
        for _ in range(self.init_steps):
            self.step()

        # Reset current step
        self.crt_step = 0

        return self.get_obs()

    # Lorenz attractor
    def lorenz(self, xv, t, a, sigma, rho, beta):

        x, y, z = xv
        dxdt    = sigma*(y - x)
        dydt    = x*(rho - z) - y + a
        dzdt    = x*y - beta*z

        return dxdt, dydt, dzdt

    # Stepping
    # Mandatory re-implementation in daughter class
    def step(self):
        raise NotImplementedError

    # Physical stepping
    def step_physical(self, u):

        # Integrate, store and compute reward
        rwd = 0.0
        t   = np.linspace(self.t, self.t+self.dt_act, self.int_steps+1)
        f   = odeint(self.lorenz,
                     (self.x, self.y, self.z), t,
                     args=(u, self.sigma, self.rho, self.beta))

        for i in range(1,self.int_steps+1):
            self.x  = float(f.T[0,i])
            self.y  = float(f.T[1,i])
            self.z  = float(f.T[2,i])
            self.t += self.dt
            self.u  = u

            self.vx = (self.x - self.lst_x[-1])/self.dt
            self.vy = (self.y - self.lst_y[-1])/self.dt
            self.vz = (self.z - self.lst_z[-1])/self.dt

            self.lst_store()

            rwd += self.get_rwd(self.lst_x[-2], self.lst_x[-1])

        # Get observation
        obs = self.get_obs()

        # Handle termination
        done           = False
        self.crt_step += 1

        if self.is_term():
            done = True
            self.dump(self.idx)
            self.lst_store()

        return obs, rwd, done, None

    # Store states
    def lst_store(self):

        self.lst_t.append (self.t )
        self.lst_x.append (self.x )
        self.lst_y.append (self.y )
        self.lst_z.append (self.z )
        self.lst_vx.append(self.vx)
        self.lst_vy.append(self.vy)
        self.lst_vz.append(self.vz)
        self.lst_u.append (self.u )

    # Check if termination is required
    def is_term(self):

        return (self.crt_step >= self.max_steps)

    # Compute reward
    # Mandatory re-implementation in daughter class
    def get_rwd(self, x_prv, x):
        raise NotImplementedError

    # Get observations
    def get_obs(self):

        x  = self.x/self.obs_norm
        y  = self.y/self.obs_norm
        z  = self.z/self.obs_norm
        vx = self.vx/self.obs_norm
        vy = self.vy/self.obs_norm
        vz = self.vz/self.obs_norm

        obs = [x, y, z, vx, vy, vz]

        return obs

    # Dump
    def dump(self, idx=None):

        addstr = ''
        if (idx is not None):
            addstr = '_'+str(idx)

        filename = self.path+'/'+self.name+addstr+'.dat'
        np.savetxt(filename,
                   np.hstack([np.reshape(self.lst_t, (-1,1)),
                              np.reshape(self.lst_x, (-1,1)),
                              np.reshape(self.lst_y, (-1,1)),
                              np.reshape(self.lst_z, (-1,1)),
                              np.reshape(self.lst_vx,(-1,1)),
                              np.reshape(self.lst_vy,(-1,1)),
                              np.reshape(self.lst_vz,(-1,1)),
                              np.reshape(self.lst_u, (-1,1))]),
                   fmt='%.5e')

    # Rendering
    def render(self, mode='human'):
        pass

    # Closing
    def close(self):
        pass
