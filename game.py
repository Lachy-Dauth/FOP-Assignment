'''
simulation of what is the time mr wolf
made by Lachlan Dauth
'''

import sys
import matplotlib.pyplot as plt
import numpy as np
from players import Wolf, Pig


def plot_player(player):
    '''
    Plots a list of either wolfs or pigs to the screen
    input: the list of objects
    '''
    xlist = []
    ylist = []
    slist = []
    clist = []
    nlist = []
    for p in range(len(player)):
        ylist.append(player[p].y)
        xlist.append(player[p].x)
        slist.append(40)
        clist.append(p)
        nlist.append(player[p].name)
        plt.annotate(nlist[p], (xlist[p], ylist[p]))
    plt.scatter(xlist, ylist, s=slist, c=clist)


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
    dinnerChance = 0.1  # the chance that the wolf calls dinner time
    defaultLand = 1  # default difficulty of land tiles
    # used for tiles with a value of p or w
    smooth = 10  # inter frame claculations that
    # improves the acruacy of the simulation and
    # improves the animation smoothness
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

    # shows how the iinital setup looks
    plt.imshow(bgImg)
    plot_player(pigsList)
    plot_player(wolfList)
    plt.pause(5)
    plt.clf()

    # sets the variables for exiting the main and if it is dinner time
    gameFinished = False
    time = False
    while gameFinished is False:
        if time is not True:
            # the first wolf picks new time
            time = wolfList[0].time()
            if time is True:
                print("It is dinner time!")
                plt.imshow(bgImg)
                plot_player(pigsList)
                plot_player(wolfList)
                plt.annotate("It is dinner time!", (edges[1]/2 - 3, 1))
                plt.pause(5)
                plt.clf()
            else:
                print("The time is", time)
                plt.imshow(bgImg)
                plot_player(pigsList)
                plot_player(wolfList)
                plt.annotate("The time is " + str(time), (edges[1]/2 - 3, 1))
                plt.pause(2)
                plt.clf()
                # calculates the amout of steps the pigs should take and
                # loops over each pig checking if they won
                for i in range(time * smooth):
                    for index, pig in enumerate(pigsList):
                        if gameFinished is False and pig.move_towards(edges, board, smooth) is True:
                                gameFinished = True
                                print(pig.name, "won the game!")
                    # creates the graph
                    plt.imshow(bgImg)
                    plot_player(pigsList)
                    plot_player(wolfList)
                    plt.pause(0.01)
                    plt.clf()
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
                    print("The pigs won the game!")

                for wolf in wolfList:
                    wolfOut = wolf.chase(edges, board, pigsList, smooth)
                    if wolfOut[0] is True:
                        gameFinished = True
                        print(
                            wolf.name,
                            "won the game! And",
                            wolfOut[1],
                            "was caught!")
                # creates the graph
                plt.imshow(bgImg)
                plot_player(pigsList)
                plot_player(wolfList)
                plt.pause(0.01)
                plt.clf()

if __name__ == "__main__":
    main()
