'''

makes players for whats the time mr wolf game.

'''
import random


# finds the distance between 2 points
def dist2points(p1, p2):
    '''
    returns the distance between 2 points
    input is ((x1, y1), (x2, y2))
    '''
    return (((p1[0] - p2[0])**2) + ((p1[1] - p2[1]) ** 2)) ** 0.5


# finds the pig closest to a point
def closest(point, pigs):
    '''
    returns the point, distance and name of the pig
    input is ((x, y), listOfPigObjects)
    '''
    arr = (((pig.x, pig.y), pig.name) for pig in pigs)
    largest = [0, 0]
    dist = 100000000
    name = ""
    for p in arr:
        if dist2points(point, p[0]) < dist:
            dist = dist2points(point, p[0])
            largest = p[0]
            name = p[1]
    return largest, dist, name


class Wolf:
    '''
    wolf player

    init values:
    x
    y
    speed
    min time
    max time
    dinner time chance
    name
    '''

    def __init__(self, x, y, speed, min, max, dinnerChance, name):
        self.x = x
        self.y = y
        self.speed = speed
        self.min = min
        self.max = max
        self.dinnerChance = dinnerChance
        self.name = name

    def time(self):
        '''
        finds a new time
        '''

        # checks if dinner time
        if random.random() < self.dinnerChance:
            return True
        else:
            # sets new time based on min and max
            return random.randint(self.min, self.max)

    def chase(self, edges, board, pigs, smooth):
        '''
        moves to the right of the screen
        if it hits the end of the wall it wins
        it will move in on "hour" its speed over the terrain difficulty spaces

        inputs:
        edges
        board
        '''

        closestPig, dist, name = closest((self.x, self.y), pigs)

        # how far the pig can travel in the horizontal direction
        # such that it is only traveling one diagonal unit
        distHor = (closestPig[0] - self.x)/dist
        # how far the pig can travel in the vertical direction
        # such that it is only traveling one diagonal unit
        distVer = (closestPig[1] - self.y)/dist

        # checking if the pig is caught if not moving the wolf
        if abs(dist) > abs(self.speed / smooth / (board[round(self.y)][round(self.x)])):
            self.x += self.speed * distHor / smooth / (board[round(self.y)][round(self.x)])
            self.y += self.speed * distVer / smooth / (board[round(self.y)][round(self.x)])
        else:
            return True, name

        return False, False

class Pig:
    '''
    pig player

    init values:
    x
    y
    speed
    name 
    '''

    def __init__(self, x, y, speed, name):
        self.x = x
        self.y = y
        self.speed = speed
        self.name = name

    def move_towards(self, edges, board, smooth):
        ''' 
        moves to the right of the screen
        if it hits the end of the wall it wins
        it will move in on "hour" its speed over the terrain difficulty spaces

        inputs:
        edges
        board
        '''

        self.x += self.speed / smooth / (board[round(self.y)][round(self.x)])
        if self.x >= edges[1] - 1:
            return True


    def run_away(self, edges, board, smooth):
        ''' 
        moves to the left of the screen
        if it hits the end of the wall it wins
        it will move in on "hour" its speed over the terrain difficulty spaces

        inputs:
        edges
        board
        '''

        self.x -= self.speed / smooth / (board[round(self.y)][round(self.x)])
        if self.x <= 0:
            return True
