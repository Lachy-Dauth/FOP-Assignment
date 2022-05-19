import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

dataDict = {}
average = []
values = []
hist = []
with open("out.csv") as out:
    preData = out.readlines()
    data = [
        [float(stat[:-1:].split(",")[0]),
         stat[:-1:].split(",")[1]] for stat in preData]
for stat in data:
    if stat[0] in dataDict:
        dataDict[stat[0]].append(stat[1])
    else:
        dataDict[stat[0]] = [stat[1]]
for key in dataDict:
    wins = 0
    total = 1
    for val in dataDict[key]:
        if val == " win":
            wins += 1
            hist.append(key)
        total += 1
    values.append(key)
    average.append(wins/total)

windowSize = round(len(dataDict) / 100)
i = 0
movingAverages = []
while i < len(average):
        windowAverage = round(
            np.sum(
                average[max(0, i-windowSize):i+1+windowSize:]
            ) / ((windowSize*2)+1), 5)
        movingAverages.append(windowAverage)
        i += 1

bin = len(values)
# estimate parameters from sample
ae, loce, scalee = stats.skewnorm.fit(hist)

plt.plot(values, average, values, movingAverages)
xmin, xmax = max(0, plt.xlim()[0]), min(1, plt.xlim()[1])
x = np.linspace(xmin, xmax, 10000)
p = stats.skewnorm.pdf(x, ae, loce, scalee)
plt.plot(x, p*len(hist)/bin*(xmax - xmin)/total, linewidth=2)
plt.title("Chance fox wins based on dinner chance")
plt.xlabel("Dinner Chance")
plt.ylabel("Win Probability")
plt.show()
