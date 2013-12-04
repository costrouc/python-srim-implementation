import time
import subprocess
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from numpy import polyfit, poly1d
import numpy as np

# Running Timing for different number of processors
maxNumProcessors = 4

numCores = []
runTimes = []

numIons = 100
ionEnergy = 100000.0
elementIon = 'Fe'

multipleSamples = 10

for i in range(maxNumProcessors):
    for j in range(multipleSamples):
        start_time = time.time()
    
        args = ['mpirun', '-n', str(i+1),
                'python', 'pysrim.py',
                '--numIons', str(numIons),
                '--ionEnergy', str(ionEnergy),
                '--elementIon', str(elementIon),
                '-o', 'temp.csv']
    
        proc = subprocess.call(args)

        runTime = time.time() - start_time

        numCores.append(i+1)
        runTimes.append(runTime)

fig, ax = plt.subplots()

ax.set_xlabel('Number of Cores')
ax.set_ylabel('Run Time [seconds]')
ax.plot(numCores, runTimes, 'bo')

fig.suptitle('Number of Cores vs. Runtime')
x = [1,2,3,4]
y = [sum(runTimes[0:9]) / 10, sum(runTimes[10:19]) / 10, sum(runTimes[20:29]) / 10, sum(runTimes[30:39])/ 10]

ax.plot(x, y, 'r--')

fig.savefig('numcores.svg')

# Running Timing for different number of ions
maxNumIons = 400

numIons = []
runTimes = []
averageRunTimes = []

numCores = 4
ionEnergy = 100000.0
elementIon = 'Fe'

numSamples = 10

for i in range(10, maxNumIons, 50):
    averageRunTime = 0.0
    for j in range(numSamples):
        start_time = time.time()
    
        args = ['mpirun', '-n', str(numCores),
                'python', 'pysrim.py',
                '--numIons', str(i),
                '--ionEnergy', str(ionEnergy),
                '--elementIon', str(elementIon),
                '-o', 'temp.csv']
    
        proc = subprocess.call(args)

        runTime = time.time() - start_time
        
        averageRunTime += runTime
        
        numIons.append(i+1)
        runTimes.append(runTime)
        
    averageRunTimes.append(averageRunTime / numSamples)

fig, ax = plt.subplots()

ax.set_xlabel('Number of Ions')
ax.set_ylabel('Run Time [seconds]')
fig.suptitle('Number of Ions vs. Runtime')

ax.plot(numIons, runTimes, 'bo')
ax.plot(range(0, maxNumIons, 50), averageRunTimes, 'r--')

fig.savefig('numions.svg')


# Running Timing for different ion energies
maxIonEnergy = 1000000

ionEnergies = []
runTimes = []
averageRunTimes = []

numCores = 4
numIons = 100
elementIon = 'Fe'

numSamples = 5

for i in range(10, maxIonEnergy, 100000):
    averageRunTime = 0.0
    for j in range(numSamples):
        start_time = time.time()
    
        args = ['mpirun', '-n', str(numCores),
                'python', 'pysrim.py',
                '--numIons', str(numIons),
                '--ionEnergy', str(i),
                '--elementIon', str(elementIon),
                '-o', 'temp.csv']
    
        proc = subprocess.call(args)

        runTime = time.time() - start_time
        
        averageRunTime += runTime
        
        ionEnergies.append(i)
        runTimes.append(runTime)
        
    averageRunTimes.append(averageRunTime / numSamples)

fig, ax = plt.subplots()

ax.set_xlabel('Ion Energy')
ax.set_ylabel('Run Time [seconds]')
fig.suptitle('Ions Energy vs. Runtime')

ax.plot(ionEnergies, runTimes, 'bo')
ax.plot(range(10, maxIonEnergy, 100000), averageRunTimes, 'r--')

fig.savefig('ionenergies.svg')
