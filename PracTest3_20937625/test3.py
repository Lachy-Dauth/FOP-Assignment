'''

beaconSim.py - beacon simulation, knights move to the beacon when lit
               and run away when it goes out

'''

import matplotlib.pyplot as plt
import numpy as np
import random
from grailCast import *

MAXROWS = 40
MAXCOLS = 60

def flipCoords(row, col, limits):
    '''
    flipCoords - converts rows and columns to x,y coords for scatter plot

    row: row in grid
    col: column in grid
    limits: max number of rows and columns
    '''
    xpos = col
    ypos = limits[0] - row - 1
    return (xpos, ypos)
    
def plot_feature_scatter(itemlist, colour, limits):
    xlist = []
    ylist = []
    slist = []
    for r,c in itemlist:
        ylist.append(limits[0] - r - 1)  
        xlist.append(c)
        slist.append(100)
    plt.scatter(xlist,ylist,color=colour, marker='s', s=slist)
    
def plot_knight_scatter(knights, limits):
    xlist = []
    ylist = []
    slist = []
    clist = []
    nlist = []
    for k in range(len(knights)):
        ylist.append(limits[0] - knights[k].getRow() - 1)  
        xlist.append(knights[k].getCol()) #flip rows/columns to y/x
        slist.append(40)
        clist.append(k)
        nlist.append(knights[k].getName())
        plt.annotate(nlist[k], (xlist[k], ylist[k]))
    plt.scatter(xlist,ylist,s=slist,c=clist)
  

def main():

    knightNames = ["Sir Galahad", "Sir Robin", "knight 1", "knight 2", "knight 3", "knight 4"]
    beacons = [(20,30)] 
    beaconLit = False
    limits = [MAXROWS, MAXCOLS]
    # Starting population
    numKnights = len(knightNames)
    knightList = []
    switchChance = 0.75

    for i in range(numKnights):  # add knight objects to grid
        knightList.append(Knight(limits, knightNames[i])) 

    # Simulation
    
    for t in range(20):
        if random.random() >= switchChance:
            beaconLit = not beaconLit
        print("### Timestep ", t, "###")
        if beaconLit == True:
            for i in range(numKnights):
                knightList[i].lure(beacons, limits)
        else:
            for i in range(numKnights):
                knightList[i].runaway(beacons, limits)
        plot_knight_scatter(knightList, limits)
        ax = plt.axes()
        plot_feature_scatter(beacons, "yellow", limits)
        if beaconLit == True:
            print("The beacon is lit.")
            plt.title("Beware! At timestep " + str(t) + " the beacons are lit.")
        else:
            print("The beacon is not lit.")
            plt.title("Run Away! The beacons are out at timestep " + str(t) + ".")
        plt.xlabel("Column")
        ax.set_facecolor("tan")
        plt.ylabel("Rows")
        plt.xlim(-1,MAXCOLS)
        plt.ylim(-1,MAXROWS)
        plt.pause(1)
        plt.clf()
    
if __name__ == "__main__":
    main()
