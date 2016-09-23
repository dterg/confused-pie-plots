'''
Confused pie plots

This script is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This script utilizes matplotlib and numpy libraries - BSD licensed software.

This script is distributed in the hope of being useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this script. If not, see
http://www.gnu.org/licenses

Author: Dieter Galea, 2016
'''

import matplotlib
matplotlib.use('Tkagg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import matplotlib.colors as colors
import random
import pandas as pd

# import confusion matrix
fullConfMat = pd.read_csv('confMat.csv', delimiter=',', header=None)
confMat = np.array(fullConfMat.ix[2:,2:])

# get class names
childNames = fullConfMat[1][2:].tolist()
parentNames = fullConfMat[0][2:].tolist()

# calculate number of classes/parents
nChildren = len(childNames)
uniqueParents = np.unique(parentNames)
nCols = np.shape(uniqueParents)[0]
nRows = 1
idx = []

# put labels into a dictionary
parentDict = dict((el,0) for el in parentNames)
for iParent, parent in enumerate(uniqueParents):
    for i, j in enumerate(parentNames):
        if j == parent:
            idx.append(i)
    parentDict[parent] = idx
    iUpperLvlClasses = [childNames[i] for i in idx]
    iLevelnClasses = np.shape(np.unique(iUpperLvlClasses))[0]
    idx = []

    # store the maximum number of classes for a parent
    if iLevelnClasses > nRows:
        nRows = iLevelnClasses

# calculate number legend rows needed
legendRowsNeeded = int(np.ceil(float(nChildren) / float(nCols)))
totalRows = nRows + legendRowsNeeded

# create a grid space
heightRatios = []
[heightRatios.append(3) for x in range(0,nRows)]
[heightRatios.append(1) for x in range(0,legendRowsNeeded)]
the_grid = GridSpec(totalRows, nCols, height_ratios=heightRatios)
nColors = nChildren
cmap = plt.cm.gist_ncar
colors = cmap(np.linspace(0.,1.,nColors))

fig = plt.figure(facecolor='white')
ax = fig.gca()

iCounter = 0
speciesCounter = 0
iRow = totalRows - legendRowsNeeded

# plot each class for each parent
for iParent, parent in enumerate(uniqueParents):
    childrenIdx = parentDict[parent]
    for jChild, child in enumerate(childrenIdx):
        speciesCounter += 1
        spName = childNames[child]
        plt.subplot(the_grid[jChild,iParent], aspect=1)
        if jChild == 0:
            plt.text(-1, 1.2, parent[0:9]+'.', fontsize=10)
        sliceSize = confMat[child,]
        if confMat[child, child] == 100:
            predictedSlices = plt.pie([100],
                            colors = colors[[child,]],
                            shadow=False,
                            startangle=90,
                            radius=1)
        else:
            predictedSlices = plt.pie(sliceSize,  # data
                colors=colors,  # array of colours
                shadow=False,   # disable shadow
                startangle=90,  # starting angle
                radius=1)
        for wedge in predictedSlices[0]:
            wedge.set_linewidth(0.1)

        actualSlices = plt.pie([100],
                colors=colors[[child,]],
                shadow=False,
                startangle=90,
                radius=0.4)

        # abbreviate name - this applies for bacterial species where naming is 'Parent child'
        # and this abbreviates to 'P. child'
        Abv = parent[0]
        AbvName = Abv + '. ' + spName

        # check if color is dark
        totalColor = 0.299 * colors[child, 0] + 0.587 * colors[child, 1] + 0.114 * colors[child, 2]
        if totalColor > 0.3:
            plt.text(-0.2, -0.1, AbvName[0]+AbvName[3], color='black', fontsize=10)
        else:
            plt.text(-0.2, -0.1, AbvName[0] + AbvName[3], color='white', fontsize=10)

        # draw legend
        if iCounter > nCols-1:
            iCounter = 0
            iRow += 1
        plt.subplot(the_grid[iRow, iCounter], aspect = 1)

        legendDots = plt.pie([100],
                               colors=colors[[child, ]],
                               shadow=False,
                               startangle=90,
                               radius=0.8)

        plt.text(1.2,-0.1,AbvName, fontsize=10) ### 4.5 adjust depending on resolution

        iCounter += 1

mng = plt.get_current_fig_manager()
#mng.resize(*mng.window.maxsize())
plt.show()
plt.savefig('Figure.tiff', format='tiff', dpi=320)
