"""PySrim - A program to simulate the implantations of ions in matter through a monte-carlo simulation

Usage:
  pysrim.py [--numIons=<num>] [--elementIon=<elem>]
  pysrim.py (-h | --help)
  pysrim.py --version

Options:
  -h --help               Show this screen.
  --version               Show version.
  --numIons=<num>         Number of Ions in Simulation [default: 10]
  --elementIon=<element>  The element of the Ion being shot [default: Ge]
"""

from ion import Ion
from element import Element, ElementTable
from target import Target, Layer, Compound
from statistics import IonStatistics

import numpy as np
import math
import copy
from numpy import dot
from numpy.linalg import norm
from docopt import docopt
from mpi4py import MPI

tollerance = 1E-8

def shootIon(ion, target, ionStatistics):
    """
    A function to simulate one ion runing into a target
    """
    testIon = copy.deepcopy(ion)
    
    ionQueue = []
    ionQueue.append(testIon)
    
    while (len(ionQueue) != 0):
        currentIon = ionQueue.pop()

        ionStatistics.saveIonState(currentIon)
        
        SimulateElectronicStopping(currentIon, target)

        if (target.isPositionIn(currentIon.position) == True):
            SimulateNuclearStopping(currentIon, target, ionQueue)

    return "One Ion Cascade Complete"
        
def runSimulation(ion, target, numIons = 10, genStats = True):
    """
    Simulates shooting numIons into a target
    """
    ionStatistics = IonStatistics()
    
    for i in range(numIons):
        shootIon(ion, target, ionStatistics)
        
    ionStatistics.to_csv('temp.csv')

# Electronic Stopping Calculations    
def SimulateElectronicStopping(ion, target):
    """
    Simulates the movement of an ion within a target losing
    energy to the electron clouds of the target. Returns
    true if the ion is still traveling
    """
    energyLoss, pathLength = calcElectronicEnergyLoss(ion, target)
    
    ion.moveIonByDistance(pathLength)

    if (ion.energy() <= energyLoss):
        ion.velocity = np.array([0.0, 0.0, 0.0])
    else:
        unitDirection = ion.velocity / norm(ion.velocity, 2)
        ion.velocity  = math.sqrt((2 * (ion.energy() - energyLoss)) / ion.mass) * unitDirection

def calcElectronicEnergyLoss(ion, target):
    """
    Calculates the energy lost of an ion while traveling
    through the target to electrons
    """
    pathLength = calcFreePathLength(ion, target)

    energyLoss = 4.0 * pathLength
    
    return (energyLoss, pathLength)

def calcFreePathLength(ion, target):
    """
    Calculates the distance the given ion travels until it
    hits the nucleus of an atom
    """
    return max(math.sqrt(norm(ion.velocity, 2)), 5.0)

# Nuclear Stopping Calculations
def SimulateNuclearStopping(ion, target, ionQueue):
    """
    Simluates the collision of an ion with an element within
    the target. If a collision occurs 
    """

    atom = selectCollisionAtom(ion, target)

    ion1, ion2 = calcCollision(ion, atom)
    
    if (ion1.energy() > target.thresholdDisplacement(ion1)):
        ionQueue.append(ion1)

    if (ion2.energy() > target.thresholdDisplacement(ion2)):
        ionQueue.append(ion2)

def selectCollisionAtom(ion, target):
    """
    Based on the location of the ion within the target an atom
    is chosen with a probablility equal to the stochiometry of the
    layer. This is an amorphous assumption
    """
    from numpy.random import rand
    X = rand()

    
    layer = target.get_layerByPosition(ion.position)
    compound = layer.compound

    for i in range(len(compound.stochiometry)):
        if (X < compound.stochiometry[i] or i +1 == len(compound.stochiometry)):
            return compound.elements[i]
        else:
            X = X - compound.stochiometry[i]
        
def calcCollision(ion, atom):
    """
    Given an incoming ion and collision atom calculate the resulting
    trajectories of the ions after collision. Energy is conserved.
    The resulting trajectories is determined using the magic angle
    formula.
    """

    E0 = ion.energy()

    V0 = ion.velocity

    weight = np.random.rand()

    unitDirection = np.random.rand(3) - 0.5
    unitDirection = unitDirection / norm(unitDirection, 2)

    while (dot(unitDirection, ion.velocity) < 0):
        unitDirection = np.random.rand(3) - 0.5
        unitDirection = unitDirection / norm(unitDirection, 2)
            
    V1 = math.sqrt((2 * weight * E0) / ion.mass) * unitDirection

    unitDirection = np.random.rand(3) - 0.5
    unitDirection = unitDirection / norm(unitDirection, 2)

    while (dot(unitDirection, ion.velocity) < 0):
        unitDirection = np.random.rand(3) - 0.5
        unitDirection = unitDirection / norm(unitDirection, 2)
            
    V2 = math.sqrt((2 * (1 - weight) * E0) / atom.mass) * unitDirection

    newIon = Ion(ion.position, V2 , atom)
    ion.velocity = V1

    return (ion, newIon)
    
if __name__ == "__main__":
    arguments = docopt(__doc__, version='PySrim 0.1')

    numIons = int(arguments['--numIons'])

    element_table = ElementTable()
    ionElement = element_table.get_elementbysymbol(arguments['--elementIon'])

    # Define the Ion
    position = np.array([0.0, 0.0, 0.0])
    energy = 1E6 #eV
    velocity = math.sqrt(energy / ionElement.mass) * np.array([1.0, 0.0, 0.0])
    ion = Ion(position, velocity, ionElement)

    # Define the target material
    Na = element_table.get_elementbysymbol('Na')
    compoundNa = Compound([1.0], [Na], [15])
    layerNa = Layer(1000000, compoundNa)
    target = Target([layerNa])

    # Initialize MPI Enviroment
    comm = MPI.COMM_WORLD #Wow that was simple
    size = comm.Get_size()
    rank = comm.Get_rank()

    # We split the job among all the nodes running the job
    myNumIons = numIons / size
    if ((numIons % size) > rank):
        myNumIons += 1

    print "My rank %d of %d running %d ions" % (rank, size, myNumIons)
        
    runSimulation(ion, target, numIons = myNumIons)
