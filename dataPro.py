import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


dataDict = {}  # a dictionary with the results for each dinnerchance
average = []  # list of average win rates in order
values = []  # list of dinnerchances tested in order
hist = []  # list of all of winning dinnerchances

# reads the data and puts it in the form of a list
with open("out.csv") as out:
    preData = out.readlines()
    data = [
        [float(stat[:-1:].split(",")[0]),
         stat[:-1:].split(",")[1]] for stat in preData]

for stat in data:
    # if the dictionary does not include the dinnerchance in stat the key is created
    if stat[0] in dataDict:
        dataDict[stat[0]].append(stat[1])
    else:
        dataDict[stat[0]] = [stat[1]]

# generates the average win rates for the values for dinner chances
for key in dataDict:
    wins = 0  # amount of time the wolf wins per dinner chance
    total = 0  # the amount of trials per dinner chance
    for val in dataDict[key]:
        if val == " win":
            wins += 1
            hist.append(key)  # adds the dinner chance to the list of wins
        total += 1
    values.append(key)
    average.append(wins/total)  # adds the average to the average list

# this code generates a rolling average for the data
# this improves the readablity of the graph
# the average is taken from both behind and infront
# this code is loosely based on code from: https://www.geeksforgeeks.org/how-to-calculate-moving-averages-in-python/
windowSize = round(len(dataDict) / 200)  # finds the range of values to get the moving average based such that it spans 1% of the values 
i = 0  # current average index
movingAverages = []  # list of moving averages in order
while i < len(average):
        windowAverage = round(
            np.sum(average[max(0, i-windowSize):i+1+windowSize:]) /  # finds the sum of the values around the current average index
            ((windowSize*2)+1), 5)  # divides the number to get the average rather than the total
        movingAverages.append(windowAverage)
        i += 1

# generates a distribution to fit the data using the scipy module
# this code is based on code from: https://stackoverflow.com/questions/50140371/scipy-skewnormal-fitting
# estimate parameters from sample
a, loc, scale = stats.skewnorm.fit(hist)  # finds the skewness, location and scale of the data

plt.plot(values, average, values, movingAverages)  # plots the average and moving averages
xmin, xmax = max(0, plt.xlim()[0]), min(1, plt.xlim()[1])  # find the domain of the graph
x = np.linspace(xmin, xmax, 10000)  # generates the x values for the graph of the distribution
p = stats.skewnorm.pdf(x, a, loc, scale)  # generates the y values for the graph of the distribution
plt.plot(x, p*len(hist)/len(values)*(xmax - xmin)/total, linewidth=2)  # plots the distribution (it needed some scaling to change from a density plot)
plt.title("Chance fox wins based on dinner chance")
plt.xlabel("Dinner Chance")
plt.ylabel("Win Probability")
plt.show()
