'''
simulation of what is the time mr wolf
made by Lachlan Dauth
'''

import sys
import numpy as np
from players import Wolf, Pig


def main():
    '''
    main function for game.py
    '''

    # create an array of the csv values called initBoard
    initBoard = []
    with open("board.csv") as f:
        for line in f:
            line_s = line.strip()
            initBoard.append(line_s.split(','))
    pigsList = []  # list for all of the pig objects
    wolfList = []  # list for all of the wolf objects
    pigSpeed = 1  # speed for all of the pigs
    wolfSpeed = 1.5  # speed for all of the wolfs
    wolfTimeRange = [3, 6]  # the range of times the wolf can pick
    dinnerChance = 0.5  # the chance that the wolf calls dinner time
    defaultLand = 1  # default difficulty of land tiles
    smooth = 10  # inter frame claculations that
    # improves the acruacy of the simulation
    edges = (len(initBoard), len(initBoard[0]))  # the size of the board
    board = np.zeros(edges)
    bgImg = np.zeros((*edges, 3))  # creates bgImg array
    remPig = []  # the list of indexs for pigs that made it to the end

    # Process command line arguments
    if len(sys.argv) == 2:  # simplified command line arg
        dinnerChance = float(sys.argv[1])
    if len(sys.argv) == 7:  # full command line arg
        dinnerChance = float(sys.argv[1])
        pigSpeed = float(sys.argv[2])
        wolfSpeed = float(sys.argv[3])
        wolfTimeRange = [int(sys.argv[4]), int(sys.argv[5])]
        smooth = int(sys.argv[6])

    # spawn animals and create board
    for i in range(len(initBoard)):
        for j in range(len(initBoard[0])):
            # creates the pigs and wolves at the points with a value of p an w
            # and sets the land difficulty to the default
            if initBoard[i][j] == "p" or initBoard[i][j] == " p":
                pigsList.append(
                    Pig(j, i, pigSpeed, "Pig_" + str(len(pigsList))))
                board[i][j] = defaultLand
            elif initBoard[i][j] == "w" or initBoard[i][j] == " w":
                wolfList.append(Wolf(j, i, wolfSpeed,
                                     wolfTimeRange[0],
                                     wolfTimeRange[1],
                                     dinnerChance,
                                     "Wolf_" + str(len(wolfList))))
                board[i][j] = defaultLand
            else:
                board[i][j] = int(initBoard[i][j])
            # create bg img based on the csv values
            bgImg[i][j] = [1 - (board[i][j]/10),
                           1 - (board[i][j]/20) - ((board[i][j]**2)/300),
                           1 - (board[i][j]/10)]

    # sets the variables for exiting the main and if it is dinner time
    gameFinished = False
    time = False
    with open("out.csv", "a") as out:
        while gameFinished is False:
            if time is not True:
                # the first wolf picks new time
                time = wolfList[0].time()
                if time is not True:
                    # calculates the amout of steps the pigs should take and
                    # loops over each pig checking if they won
                    for i in range(time * smooth):
                        for index, pig in enumerate(pigsList):
                            if gameFinished is False and pig.move_towards(edges, board, smooth) is True:
                                gameFinished = True
                                out.write(str(dinnerChance) + ", loss\n")
            else:
                while gameFinished is False:
                    remPig = []  # empties the list
                    for index, pig in enumerate(pigsList):
                        if pig.run_away(edges, board, smooth) is True:
                            remPig.insert(0, index)
                    # removes the pigs in rempig
                    for i in remPig:
                        pigsList.pop(i)
                    if len(pigsList) == 0:
                        gameFinished = True
                        out.write(str(dinnerChance) + ", loss\n")

                    for wolf in wolfList:
                        wolfOut = wolf.chase(edges, board, pigsList, smooth)
                        if wolfOut[0] is True:
                            gameFinished = True
                            out.write(str(dinnerChance) + ", win\n")

if __name__ == "__main__":
    main()
