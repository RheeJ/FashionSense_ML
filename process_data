###pre-process stanford image dataset

import os
import numpy as np
import math
import csv

featureDict = {}
csvArray = []

for i in range(0, 26):
    imagePath = str(i) + ".npy"
    array = np.load(imagePath)
    temp = []
    for j in range(len(array)):
        if not math.isnan(array[j][0]):
            temp.append(int(array[j][0]))
        else:
            temp.append(0)
    featureDict[i] = temp
    csvArray.append(temp)


a = np.asarray(csvArray)
np.savetxt("data.csv", a, delimiter=",")

