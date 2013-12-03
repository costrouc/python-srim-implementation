import sys

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

def plotDistribution(inputfilename, outputfilename):
    """
    A function to plot the distribution data from the ion locations
    """
    
    db_particle =  pd.read_csv(inputfilename)
        
    # Create some random numbers
    x = db_particle['x']
    y = db_particle['y']
    z = db_particle['z']
    
    # Estimate the 2D histogram
    nbins = 100
    Hxy, xedges, yedges = np.histogram2d(x,y,bins=nbins, normed=True)
    Hxz, xedges, zedges = np.histogram2d(x,z,bins=nbins, normed=True)
    Hyz, yedges, zedges = np.histogram2d(y,z,bins=nbins, normed=True)
    
    # H needs to be rotated and flipped
    Hxy = np.rot90(Hxy)
    Hxy = np.flipud(Hxy)
    
    Hxz = np.rot90(Hxz)
    Hxz = np.flipud(Hxz)
    
    Hyz = np.rot90(Hyz)
    Hyz = np.flipud(Hyz)
    
    # Mask zeros
    Hmaskedxy = np.ma.masked_where(Hxy==0,Hxy) # Mask pixels with a value of zero
    Hmaskedxz = np.ma.masked_where(Hxz==0,Hxz) # Mask pixels with a value of zero
    Hmaskedyz = np.ma.masked_where(Hyz==0,Hyz) # Mask pixels with a value of zero
    
    # Plot 2D histogram using pcolor
    # fig2 = plt.figure()
    fig, ax = plt.subplots(1, 3)
    fig.set_size_inches((14,4.5))
    ax[0].pcolormesh(xedges,yedges,Hmaskedxy)
    ax[0].set_xlabel('x')
    ax[0].set_ylabel('y')
    
    ax[1].pcolormesh(xedges,zedges,Hmaskedxz)
    ax[1].set_xlabel('x')
    ax[1].set_ylabel('z')
    
    ax[2].pcolormesh(yedges,zedges,Hmaskedyz)
    ax[2].set_xlabel('y')
    ax[2].set_ylabel('z')

    plt.tight_layout()
    plt.savefig(outputfilename, transparent = True)

if __name__ == '__main__':
    plotDistribution(sys.argv[1], sys.argv[2])
