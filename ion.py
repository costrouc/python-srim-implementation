"""
A module to represent an Ion Class
"""

import math
import numpy as np
from numpy import dot
from numpy.linalg import norm

from element import Element

class Ion(Element):
    """
    Representation of an ion
    input:
    position [x, y, z]
    velocity [u, v, w]
    energy e (electron volts eV)
    element Element(args)
    """
    id_counter = 0
    
    def __init__(self, position, velocity, element):
        Element.__init__(self, element.symbol, element.atomicNumber, element.mass)
        self.position = position
        self.velocity = velocity
        self.element = element
        self.id = Ion.id_counter
        Ion.id_counter += 1

    def moveIonByDistance(self, distance):
        """
        Given the current velocity direction
        displace the atom a given distance 
        """
        unitDirection = self.velocity / norm(self.velocity, 2)
        
        self.position = self.position + distance * unitDirection

    def energy(self):
        return 0.5 * self.mass * (self.velocity[0] * self.velocity[0] + \
                                  self.velocity[1] * self.velocity[1] + \
                                  self.velocity[2] * self.velocity[2] )
            
    def __str__(self):
        return "Position:" + str(self.position) + \
               "Velocity:" + str(self.velocity) + \
               "Energy: " + str(self.energy) + \
               "Element:\nSymbol: " + self.symbol + \
               "Atomic Number: " + str(self.atomicNumber) + \
               "Mass: " + str(self.mass)
                                       
