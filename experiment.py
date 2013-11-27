tollerance = 1E-8

class Element:
    """
    Representation of an element
    """
    def __init__(self, name, atomicNumber, mass):
        self.name = name
        self.atomicNumber = atomicNumber
        self.mass = mass
    
class Compound:
    """
    Representation of an compound in a target. It is assumed
    that the stochiometry of the compound is normalized to one.
    """
    def __init__(self, stochiometry, elements, thresholdDisplacement):
        self.stochiometry = stochiometry
        self.elements = elements
        self.thresholdDisplacement = thresholdDisplacement
        
class Layer:
    """
    Representation of a layer in a target
    """
    def __init__(self, compound):
        self.thickness = 0.5 # [L] cm
        self.compound = compound

class Target:
    """
    Representation of a target being shot at
    """
    def __init__(self, layers):
        self.layers = layers

        self.totalThickness = 0.0
        for layer in layers:
            self.totalThickness = self.totalThickness + layer.thickness

    def isPositionIn(self, position):
        pointIsIn = True
        if (position[0] < tollerance or position[0] > self.totalThickness - tollerance):
            pointIsIn = False
        return pointIsIn

    def get_thresholdDisplacement(self, ion, target):
        layer = target.getLayerAtPosition(ion.position)
        return layer.compound.get_thresholdDisplacment(ion.element)
        
class Ion:
    """
    Representation of an ion
    """
    def __init___(self, element):
        self.position = [0.0, 0.0, 0.0]
        self.velocity = [1.0, 0.0, 0.0]
        self.element = element

    def set_trajectory(trajectory):
        self.position = trajectory[0]
        self.velocity = trajectory[1]
        
    def __str__(self):
        print "Position:"
        print self.position
        print "Velocity:"
        print self.velocity
        print "Element"
        print self.element

def shootIon(ion, target):
    """
    A function to simulate one ion runing into a target
    """
    ionQueue = []
    ionQueue.append(ion)

    while (len(ionQueue) != 0):
        currentIon = ionQueue.pop()
        
        SimulateElectronicStopping(currentIon, target)

        if (target.isPointIn(currentIon.point) == True):
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
        
def calcFreePathLength():
    """
    Calculates the distance the given ion travels until it
    hits the nucleus of an atom
    """
    return 0.1

def calcElectronicEnergyLoss(ion, target):
    """
    Calculates the energy lost of an ion while traveling
    through the target to electrons
    """
    pathLength = calcFreePathLength(ion, target)

    energyLoss = 1.0
    
    return (energyLoss, pathLength)
    
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

def SimluateNuclearStopping(ion, target, ionQueue):
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
    
    if (ion.get_energy() < target.get_thresholdDisplacement(ion)):
        ionQueue.append(ion)

    if (newIon.get_energy() < target.get_thresholdDisplacement(newIon)):
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
    
