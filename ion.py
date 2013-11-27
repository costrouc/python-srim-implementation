"""
A module to represent an Ion Class
"""

import math
import numpy as np

from element import Element

class Ion:
    """
    Representation of an ion
    """
    def __init__(self, element):
        self.position = np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([1.0, 0.0, 0.0])
        self.element = element

    def set_trajectory(self, trajectory):
        """
        Replaces the current position and velocity of the ion
        """
        self.position = trajectory[0]
        self.velocity = trajectory[1]

    def moveIonByDistance(self, pathLength):
        """
        Given the current velocity direction
        displace the atom a given distance 
        """
        v = math.sqrt(self.velocity[0]**2 + self.velocity[0]**2 + self.velocity[0]**2)
        
        unitVelocity = self.velocity / v

        self.position = self.position + pathLength * unitVelocity

    def get_energy(self):
        """
        Kinetic Energy of an ion (1/2)mv^2
        """
        v = math.sqrt(self.velocity[0]**2 + self.velocity[0]**2 + self.velocity[0]**2)
        return 0.5 * self.element.mass * v**2

    def reduceEnergyBy(self, energyLoss):
        """
        Reduces the energy of the ion by a set number
        if the energy is greater than the total energy of the
        ion it will simply set it to zero
        """
        totalEnergy = self.get_energy() - energyLoss

        if (totalEnergy <= 0.0):
            totalEnergy = 0.0
        else:
            self.velocity = 0.25 * self.velocity
            
    def __str__(self):
        print "Position:"
        print self.position
        print "Velocity:"
        print self.velocity
        print "Element"
        print self.element
