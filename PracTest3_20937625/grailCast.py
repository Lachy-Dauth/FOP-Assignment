'''
grailCast.py - characters based on The Holy Grail, by Monty Python

Cast:
    Knight - the knights of the round table, lured by a beacon

'''
import random

class Knight():
    '''
    Knight - has a row,col position and a name

    __init__ arguments:
        row : within MAXROWS
        col : within MAXCOLS
        name : a string
    '''
    def __init__(self, limits, name):
        self.row = random.randint(0, limits[0]-1)
        self.col = random.randint(0, limits[1]-1)
        self.name = name
        self.captured = False
        self.felloff = False
    
    # Accessor methods

    def getRow(self):      # you *could* access these directly
        return self.row    # but showing how we can protect the data

    def getCol(self):
        return self.col

    def getName(self):
        return self.name

    # Mutator methods

    def lure(self, beacons, limits):
        '''
        lure - moves the individual knight towards the beacon(s)

        beacons - a list of beacon tuples (round bracket lists)
        limits - the boundaries of the "world"
        '''
        print("lure ", self.name)
        chosenBeacon = beacons[0] # could have multiple beacons...
        count = 0
        if chosenBeacon[0] < self.row:
            self.row -= 1
        elif chosenBeacon[0] > self.row:
            self.row += 1
        else:
            count += 1
        if chosenBeacon[1] < self.col:
            self.col -= 1
        elif chosenBeacon[1] > self.col:
            self.col += 1
        else:
            count += 1
        if count == 2:
            self.captured = True
            print(self.name, " has been captured")

    def runaway(self, beacons, limits):
        '''
        runaway - moves the individual knight away from the beacon(s)

        beacons - a list of beacon tuples (round bracket lists)
        limits - the boundaries of the "world"
        '''
        print("runaway ", self.name)
        chosenBeacon = beacons[0]
        
        if self.row <= 0 or self.row >= limits[0]:
            self.felloff = True
            print(self.name, " has fallen off the world")
        if self.col <= 0 or self.col >= limits[1]:
            self.felloff = True
            print(self.name, " has fallen off the world")

        if chosenBeacon[0] < self.row:
            self.row += 1
        elif chosenBeacon[0] > self.row:
            self.row -= 1
        if chosenBeacon[1] < self.col:
            self.col += 1
        elif chosenBeacon[1] > self.col:
            self.col -= 1

