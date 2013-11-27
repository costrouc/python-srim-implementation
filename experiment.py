"""
Module that runs the SRIM simulation
"""

from ion import Ion
from element import Element
from target import Target, Layer, Compound

import numpy as np
from numpy.linalg import norm

tollerance = 1E-8

def shootIon(ion, target):
    """
    A function to simulate one ion runing into a target
    """
    ionQueue = []
    ionQueue.append(ion)

    while (len(ionQueue) != 0):
        currentIon = ionQueue.pop()
        
        SimulateElectronicStopping(currentIon, target)

        if (target.isPositionIn(currentIon.position) == True):
            SimulateNuclearStopping(currentIon, target, ionQueue)

    return "One Ion Cascade Complete"
        
def runSimulation(ion, target, numIons = 10, genStats = True):
    """
    Simulates shooting numIons into a target
    """
    simulationStatistics = []
    
    for i in range(numIons):
        stat = shootIon(ion, target)
        simulationStatistics.append(stat)
        
    return

# Electronic Stopping Calculations    
def SimulateElectronicStopping(ion, target):
    """
    Simulates the movement of an ion within a target losing
    energy to the electron clouds of the target. Returns
    true if the ion is still traveling
    """
    energyLoss, pathLength = calcElectronicEnergyLoss(ion, target)
    
    ion.moveIonByDistance(pathLength)

    if (ion.energy <= energyLoss):
        ion.energy = 0.0
    else:
        ion.energy = ion.energy - energyLoss
    
    return 

def calcElectronicEnergyLoss(ion, target):
    """
    Calculates the energy lost of an ion while traveling
    through the target to electrons
    """
    pathLength = calcFreePathLength(ion, target)

    energyLoss = 1.0
    
    return (energyLoss, pathLength)

def calcFreePathLength(ion, target):
    """
    Calculates the distance the given ion travels until it
    hits the nucleus of an atom
    """
    return 0.1

# Nuclear Stopping Calculations
def SimulateNuclearStopping(ion, target, ionQueue):
    """
    Simluates the collision of an ion with an element within
    the target. If a collision occurs 
    """

    atom = selectCollisionAtom(ion, target)

    ion1, ion2 = calcCollision(ion, atom)
    
    if (ion1.energy < target.get_thresholdDisplacement(ion1, target)):
        ionQueue.append(ion1)

    if (ion2.energy < target.get_thresholdDisplacement(ion2, target)):
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
    print "1 collision"
    
    # Trajectory: [[position], [velocity]]
    totalEnergy = ion.energy
    
    randUnitDirection = np.random.rand(3)
    randUnitDirection = randUnitDirection / norm(randUnitDirection, 2)
    newIon = Ion(ion.position, randUnitDirection, 0.5 * totalEnergy, atom)
    
    randUnitDirection = np.random.rand(3)
    randUnitDirection = randUnitDirection / norm(randUnitDirection, 2)
    ion.direction = randUnitDirection
    ion.energy = 0.5 * totalEnergy
    
    return (ion, newIon)
    
if __name__ == "__main__":
    Na = Element("Na", 11, 22.978)
    Ge = Element("Ge", 32, 72.64)

    position = np.array([0.0, 0.0, 0.0])
    direction = np.array([1.0, 0.0, 0.0])
    energy = 1E5 #eV
        
    ionGe = Ion(position, direction, energy, Ge)

    compoundNa = Compound([1.0], [Na], [100])
    layerNa = Layer(compoundNa)
    target = Target([layerNa])

    shootIon(ionGe, target)
