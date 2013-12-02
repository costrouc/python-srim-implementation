"""
Module that runs the SRIM simulation
"""

from ion import Ion
from element import Element
from target import Target, Layer, Compound
from statistics import IonStatistics

import numpy as np
import math
from numpy.linalg import norm

tollerance = 1E-8

def shootIon(ion, target, ionStatistics):
    """
    A function to simulate one ion runing into a target
    """
    ionQueue = []
    ionQueue.append(ion)
    
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
        print "Shooting Ion %d" % (i)
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
    return 6.0

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

    print atom.mass
    print ion.mass

    E0 = ion.energy()

    V0 = ion.velocity

    weight = np.random.rand()

    unitDirection = np.random.rand(3)
    unitDirection = unitDirection / norm(unitDirection, 2)
    V1 = math.sqrt((2 * weight * E0) / ion.mass) * unitDirection
    V2 = (ion.mass / atom.mass) * (V0 - V1)

    newIon = Ion(ion.position, V2 , atom)
    ion.velocity = V1

    print E0 - ion.energy() - newIon.energy()
    
    return (ion, newIon)
    
if __name__ == "__main__":
    Na = Element("Na", 11, 22.978)
    Ge = Element("Ge", 32, 72.64)

    position = np.array([0.0, 0.0, 0.0])

    energy = 1E8 #eV
    velocity = math.sqrt(energy / Ge.mass) * np.array([1.0, 0.0, 0.0])
    ionGe = Ion(position, velocity, Ge)

    compoundNa = Compound([1.0], [Na], [15])
    layerNa = Layer(1000000, compoundNa)
    target = Target([layerNa])

    runSimulation(ionGe, target, numIons = 10)
