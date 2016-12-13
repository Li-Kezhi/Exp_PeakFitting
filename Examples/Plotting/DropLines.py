#!/usr/bin/env python

"""
Plotting script

"""

__author__ = "LI Kezhi" 
__date__ = "$2016-12-13$"
__version__ = "1.0.0"


import numpy as np
import matplotlib.pyplot as plt

import mpltex


##### Preparation #####
# File names
name = []
name.append('./DropLines/PDF#41-1379_MnOOH.txt')
name.append('./DropLines/PDF#24-0734_Mn3O4.txt')
name.append('./DropLines/PDF#44-1472_MnCO3.txt')
# Label names
labels = []
labels.append(r'MnOOH #24-0734')
labels.append(r'Mn$_3$O$_4$ #24-0734')
labels.append(r'MnCO$_3$ #44-1472')
# Colors
colors = []
colors.append((228/255.0, 26/255.0, 28/255.0))
colors.append((55/255.0, 126/255.0, 184/255.0))
colors.append((77/255.0, 175/255.0, 74/255.0))
# colors.append((152/255.0, 78/255.0, 163/255.0))
# colors.append((255/255.0, 127/255.0, 0/255.0))
# colors.append((255/255.0, 255/255.0, 51/255.0))
# colors.append((166/255.0, 86/255.0, 40/255.0))
# colors.append((247/255.0, 129/255.0, 191/255.0))
# colors.append((153/255.0, 153/255.0, 153/255.0))
# Read data
data = []
for i in xrange(len(name)):
    data.append(np.loadtxt(name[i]))
# # Y-axis shift
# yShift = np.zeros_like(data[0])
# x, y = np.shape(data[0])
# for i in xrange(x):
#     yShift[i, 1] = 20000
# for i in xrange(len(name)):
#     data[i] += yShift * i

##### Plotting #####
@mpltex.presentation_decorator
def plot(data, name):
    fig, ax = plt.subplots()
    for i in xrange(len(name)):
        ax.bar(data[i][:,6], data[i][:,1],
               width=0.1, 
               edgecolor=colors[i], facecolor=colors[i],
               label=labels[i])

    ax.set_xlim(5, 80)
    ax.set_ylim(0, 100)

    ax.set_yticks([]) # Hide yticks
    ax.tick_params(axis='x', top='off', bottom='off')

    ax.legend(loc='best')
    ax.set_ylabel('Intensity (A.U.)')
    ax.set_xlabel(r'2$\theta$($^{\circ}$)')

    plt.show()


plot(data, name)
