#!/usr/local/bin/python3.7

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.linalg import circulant as ci
import sys

plt.rcParams['figure.figsize'] = 6, 6
plt.rcParams['axes.grid'] = True
plt.rcParams.update({'font.size':8})

def Trace(x):
    sns.heatmap(x, cmap="coolwarm", fmt='.2f', annot=False, cbar=False, xticklabels=False, yticklabels=False)
    return plt.show()

def SubCrypt(shuffleKey, subM, subSize):
    subMflat = subM.flatten()
    subCflat = shuffleKey.dot(subMflat)
    subC = subCflat.reshape(subSize, subSize)
    return subC

def GlobCrypt(shuffleKey, Mat, subSize, size):
    MatC = Mat * 0.
    for i in range(size//subSize):
        for j in range(size//subSize):
            subM = Mat[i*subSize : (i+1)*subSize, j*subSize : (j+1)*subSize]
            MatC[i*subSize : (i+1)*subSize, j*subSize : (j+1)*subSize] = SubCrypt(shuffleKey, subM, subSize)
    return MatC

sizeMat = 36
sub     = 3
if sizeMat%sub != 0:
    print('problème de divisibilité')
    sys.exit()


shuf = np.zeros((sub**2,sub**2))
shuf = np.eye(sub**2)
np.random.shuffle(shuf)
print(shuf)

mat = -np.eye(sizeMat) 
for i in range(sizeMat):
    mat += np.diagflat(np.ones(sizeMat-i)/(i+1), i)
    mat += np.diagflat(np.ones(sizeMat-i)/(i+1), -i)

matC = GlobCrypt(shuf, mat, sub, sizeMat)

Trace(mat)
Trace(matC)


x, y = np.ogrid[-1:1:sizeMat*1j, -1:1:sizeMat*1j]
Boule = -(x**2 + y**2) ** 0.5 
Boule /= np.amin(Boule)
Boule *= -1
Boule += 1

boulC = GlobCrypt(shuf, Boule, sub, sizeMat)

Trace(Boule)
Trace(boulC)

X, Y = np.ogrid[-1:1:sizeMat*1j, -1:1:sizeMat*1j]
Truc = 1 + X + Y + X*Y

Traf = GlobCrypt(shuf, Truc, sub, sizeMat)

Trace(Truc)
Trace(Traf)
