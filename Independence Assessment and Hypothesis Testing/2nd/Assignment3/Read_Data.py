import os
import numpy as np

fileName='../1405036.txt'
#fileName='../1405048.txt'

def getData():
    data = []
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    with open(os.path.join(fileDir,fileName)) as f:
        for line in f:
            data.append(line)
    data = np.array(data, dtype=np.float)
    #print(data)
    #print(data.dtype)
    return data