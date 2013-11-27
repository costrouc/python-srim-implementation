"""
Module that runs the SRIM simulation
"""

from ion import Ion
from element import Element
from target import Target, Layer, Compound

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
    ion.reduceEnergyBy(energyLoss)
    
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
    # traj = [[position], [velocity]]
    traj1, traj2 = calcCollisionTrajectory(ion, atom)

    newIon = Ion(atom)
    newIon.set_trajectory(traj1)
    
    ion.set_trajectory(traj2)
    
    if (ion.get_energy() < target.get_thresholdDisplacement(ion, target)):
        ionQueue.append(ion)

    if (newIon.get_energy() < target.get_thresholdDisplacement(newIon, target)):
        ionQueue.append(ion)

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
        
def calcCollisionTrajectory(ion, atom):
    """
    Given an incoming ion and collision atom calculate the resulting
    trajectories of the ions after collision. Energy is conserved.
    The resulting trajectories is determined using the magic angle
    formula.
    """
    # Trajectory: [[position], [velocity]]
    position = ion.position
    velocity = ion.velocity

    return [[position, 0.5 * velocity], [position, 0.5 * velocity]]
    
if __name__ == "__main__":
    Na = Element("Na", 11, 22.978)
    Ge = Element("Ge", 32, 72.64)
    
    ionGe = Ion(Ge)

    compoundNa = Compound([1.0], [Na], [100])
    layerNa = Layer(compoundNa)
    target = Target([layerNa])

    shootIon(ionGe, target)
