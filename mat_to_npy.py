import scipy.io as sio
import numpy as np
import math
def deserialize(filename, i, listy):
    listicle = []
    print filename
    mat = sio.loadmat(filename)
    label = mat['GT'][i-1]
    if filename == "clothing-data/labels/black_GT.mat":
        listicle = [0,0,0]
        if math.isnan(label):
            listicle[2] = 1
        else:
            listicle[int(label)-1] = 1
        listy.append(listicle)
        return listy
    else:
        return "not implemented yet"
