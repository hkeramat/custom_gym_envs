# Generic improts
import os
import sys
import collections

# Custom imports
from lorenz.envs.lorenz_stabilizer_discrete import *

#######################################
# Run Lorentz attractor without control
#######################################

# Initialize attractor
lorenz      = LorenzStabilizerDiscrete()
lorenz.name = 'lorenz_free_stabilizer'
lorenz.set_cpu(0,1)
lorenz.reset()

# Evolve attractor
done    = False
sum_rwd = 0.0

while (not done):
    _, rwd, done, _ = lorenz.step()
    sum_rwd += rwd

sum_rwd = f"{sum_rwd:.3f}"
print('# Default rwd = '+str(sum_rwd))

# Plot
os.system('gnuplot -c plot.gnu '+str(lorenz.path)+'/ '+str(lorenz.name)+'_0.dat ')
