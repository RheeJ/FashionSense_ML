import scipy.io as sio
import numpy as np
import math
def deserialize(filename):
    train_list = []
    test_list = []
    mat = sio.loadmat(filename)
    count = 0
    for val in mat['GT']:
        listicle = [0,0,0,0,0,0,0,0]
        if math.isnan(val):
            listicle[7] = 1
        else:
            listicle[int(val)] = 1
        if count < 1700:
            train_list.append(listicle)
        else:
            test_list.append(listicle)
    a = np.array(train_list)
    b = np.array(test_list)
    np.save('train_labels.npy', a)
    np.save('test_labels.npy', b)
print deserialize('category_GT.mat')
