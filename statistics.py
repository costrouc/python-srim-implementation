import pandas as pd

class IonStatistics:
    """
    A datastore for ion data
    """
    def __init__(self):
        self.ids = []
        self.positions = []
        self.velocities = []

    def saveIonState(self, ion):
        self.ids.append(ion.id)
        self.positions.append(ion.position)
        self.velocities.append(ion.velocity)
        
    def to_csv(self, filename = 'tmp.csv'):
        outputFile = open(filename, 'w')
        outputFile.write('id,x,y,z,u,v,w\n') 
        for i in range(len(self.ids)):
            outputFile.write('%d,%2.3f,%2.3f,%2.3f,%2.3f,%2.3f,%2.3f\n' %
                             (self.ids[i], self.positions[i][0],
                              self.positions[i][1], self.positions[i][2],
                              self.velocities[i][0], self.velocities[i][1],
                              self.velocities[i][2]))
        outputFile.close()
        
