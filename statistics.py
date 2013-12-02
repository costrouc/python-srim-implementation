import pandas as pd
import mpi4py as MPI

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

    def consolidate(self, comm):
        comm.Barrier()
        self.ids = comm.gather(self.ids, root=0)
        self.positions = comm.gather(self.positions, root=0)
        self.velocities = comm.gather(self.velocities, root=0)
        """
        temp_ids = [item for sublist in self.ids for item in sublist] 
        temp_pos = [item for sublist in self.positions for item in sublist] 
        temp_vel = [item for sublist in self.velocities for item in sublist] 

        self.ids = temp_ids
        self.positions = temp_pos
        self.velocities = temp_vel
        """
        
    def to_csv(self, filename = 'tmp.csv'):
        outputFile = open(filename, 'w')
        outputFile.write('id,x,y,z,u,v,w\n')
        for job in range(len(self.ids)):
            for i in range(len(self.ids[job])):
                outputFile.write('%d,%2.3f,%2.3f,%2.3f,%2.3f,%2.3f,%2.3f\n' %
                                 (self.ids[job][i], self.positions[job][i][0],
                                  self.positions[job][i][1], self.positions[job][i][2],
                                  self.velocities[job][i][0], self.velocities[job][i][1],
                                  self.velocities[job][i][2]))
        outputFile.close()
        
