import pandas as pd

class IonStatistics:
    """
    A datastore for ion data
    """
    def __init__(self):
        self.ids = []
        self.positions = []
        self.directions = []
        self.energies = []

    def saveIonState(self, ion):
        self.ids.append(ion.id)
        self.positions.append(ion.position)
        self.directions.append(ion.direction)
        self.energies.append(ion.energy)

    def to_csv(self, filename = 'tmp.csv'):
        outputFile = open(filename, 'w')
        outputFile.write('id, x, y, z, u, v, w, energy\n') 
        for i in range(len(self.ids)):
            outputFile.write('%d, %2.3f, %2.3f, %2.3f, %2.3f, %2.3f, %2.3f, %2.3f\n' %
                             (self.ids[i], self.positions[i][0],
                              self.positions[i][1], self.positions[i][2],
                              self.directions[i][0], self.directions[i][1],
                              self.directions[i][2], self.energies[i]))
        outputFile.close()
        
