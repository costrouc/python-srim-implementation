"""
A Module that represent the target being shot at
"""

tollerance = 1E-8

class Compound:
    """
    Representation of an compound in a target. It is assumed
    that the stochiometry of the compound is normalized to one.
    """
    def __init__(self, stochiometry, elements, thresholdDisplacement):
        self.stochiometry = stochiometry
        self.elements = elements
        self.thresholdDisplacement = thresholdDisplacement

    def get_thresholdDisplacement(self, element):
        thresholdDisplacement = 0.0
        
        for i in range(len(self.elements)):
            if (self.elements[i] == element):
                thresholdDisplacement = self.thresholdDisplacement[i]

        return thresholdDisplacement
        
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
        positionIsIn = True
        if (position[0] < tollerance or position[0] > self.totalThickness - tollerance):
            positionIsIn = False
        return positionIsIn

    def get_thresholdDisplacement(self, ion, target):
        layer = target.get_layerByPosition(ion.position)
        return layer.compound.get_thresholdDisplacement(ion.element)

    def get_layerByPosition(self, position):
        x = position[0]

        for layer in self.layers:
            if (x <= layer.thickness):
                return layer
            else:
                x = x - layer.thickness
        return None
