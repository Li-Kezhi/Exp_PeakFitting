import numpy as np
import matplotlib.pyplot as plt

import mpltex


##### Preparation #####
# File names
name = []
name.append('./RawData/MnO2-4-100.USR')
name.append('./RawData/MnO2-6-100.USR')
name.append('./RawData/MnO2-8-100.USR')
# Label names
labels = []
labels.append(r'$\lambda$-MnO$_2$-4h')
labels.append(r'$\lambda$-MnO$_2$-6h')
labels.append(r'$\lambda$-MnO$_2$-8h')
# Read data
data = []
for i in xrange(len(name)):
    data.append(np.loadtxt(name[i], skiprows=8))
# Y-axis shift
yShift = np.zeros_like(data[0])
x, y = np.shape(data[0])
for i in xrange(x):
    yShift[i, 1] = 20000
for i in xrange(len(name)):
    data[i] += yShift * i

##### Plotting #####
@mpltex.presentation_decorator
def plot(data, name):
    fig, ax = plt.subplots()
    for i in xrange(len(name)):
        ax.plot(data[i][:,0], data[i][:,1], label=labels[i])

    ax.set_xlim(5, 80)

    ax.set_yticks([]) # Hide yticks

    ax.legend(loc='best')
    ax.set_ylabel('Intensity (A.U.)')
    ax.set_xlabel(r'2$\theta$($^{\circ}$)')

    plt.show()


plot(data, name)