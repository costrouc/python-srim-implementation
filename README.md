# PySrim

PySrim is a code written in python to simulate via Monte Carlo ion treveling through a target. The ions are stopped through the collisions of ions with the nucleus of an atom within the material and excitation of the electron clouds of each atom.

# Installation

## Dependencies
docopt  
matplotlib  
numpy  
pandas  
mpi4py  

## Pip installation
This installation obviously requires you to have the pip installer already present on your machine. To get pip refer to [here](http://www.pip-installer.org/en/latest/installing.html).  

Once you have pip you can install all the dependencies for PySrim  
`sudo pip install -r requirements.txt`

## Example Test Machine
`ssh finch.desktops.utk.edu`  

The logon information was given in the final report

## Run PySrim via web interface
[Python Web Interface](http://finch.desktops.utk.edu)

# Running
Use the makefile!  

> `make example`
Runs an example of mpi running with pysrim

> `make plot`
Runs an example of pysrim with mpi that creates a plot of the data

