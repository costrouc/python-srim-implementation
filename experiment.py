from Collections import namedtuple

class Element:
    """
    Representation of an element
    """
    def __init__(self, name, atomicNumber, mass)
        self.name = name
        self.atomicNumber = atomicNumber
        self.mass = mass
    
class Compound:
    """
    Representation of an compound in a material
    """
    def __init__(self, stochiometry, elements):
        self.stochiometry = stochiometry
        self.elements = elements

class Layer:
    """
    Representation of a layer in a material
    """
    def __init__(self, compound):
        self.thickness = 0.5 # [L] cm
        self.compound = compound

class Material:
    """
    Representation of a material being shot at
    """
    def __init__(self, layers):
        self.layers = layers
        
class Ion:
    """
    Representation of an ion
    """
    def __init___(self, element):
        self.position = [0.0, 0.0, 0.0]
        self.velocity = [1.0, 0.0, 0.0]
        self.element = element

    def __str__(self):
        print "Position:"
        print self.position
        print "Velocity:"
        print self.velocity
        print "Element"
        print self.element

def shootIon(ion, material):
    """
    A function to simulate one ion runing into a material
    """
    # 
    ionQ.append(ion)

    while (len(ionQ) != 0):
        currentIon = ionQ.pop()
        
        SimulateElectronicStopping(currentIon, material)
        SimulateNuclearStopping(currentIon, material)

        
def runSimulation(ion, material, numIons = 10, genStats = True):
    """
    Simulates shooting numIons into a material
    """
    simulationStatistics = []
    
    for i in range(numIons):
        stat = shootIon(ion, material)
        simulationStatistics.append(stat)
        
    return pass
        
def calcFreePathLength():
    """
    Calculates the distance the given ion travels until it
    hits the nucleus of an atom
    """
    return 0.1

def SimulateElectronicStopping(ion, material):
    """
    Simulates the movement of an ion within a material losing
    energy to the electron clouds of the material. Returns
    true if the ion is still traveling
    """
    pathLength = calcFreePathLength(ion, material)
    energyLoss = calcElectronicEnergyLoss(pathLength, ion, material)
    
    return pass

def SimluateNuclearStopping(ion, material):
    """
    Simluates the collision of an ion with an element within
    the material. If a collision occurs 
    """
    
    
    
    
