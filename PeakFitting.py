#!/usr/bin/env python

"""
Parameters needed to modify:
1. File name and position
    fileLocation, fileName
2. Background model
    "import" part, bg_mod part
3. Peaks information
    Peak type, initial estimation
4. Add-up model
    mod = peak1 + peak2 + bg_mod
"""

import numpy as np
from lmfit.models import VoigtModel, LinearModel
import sys
import matplotlib.pyplot as plt

fileLocation = 'E:\\SkyDrive\\Sharing data\\XRD\\20160424_MnCeBi\\For python\\'
fileName = 'Mn0-100.txt'

start = 52.0      # Define the fitting range
end = 64.0

dat = np.loadtxt(fileLocation + fileName)
x_original = dat[:, 0]
y_original = dat[:, 1]

startLine, endLine = None, None
for i in xrange(np.size(x_original)):
    if x_original[i] >= start and startLine == None:
        startLine = i
    if startLine != None and x_original[i] >= end:
        endLine = i
        break

x = x_original[startLine:endLine]
y = y_original[startLine:endLine]


bg_mod = LinearModel(prefix='bg_')   # Background
pars = bg_mod.guess(y, x=x)

peak1  = VoigtModel(prefix='p1_')    # Peak information
pars.update(peak1.make_params())

pars['p1_center'].set(56, min=54, max=58)
pars['p1_amplitude'].set(2000, min=0)

peak2  = VoigtModel(prefix='p2_')
pars.update(peak2.make_params())

pars['p2_center'].set(59, min=57, max=61)
pars['p2_amplitude'].set(2000, min=0)

mod = peak1 + peak2 + bg_mod      # Add-up


init = mod.eval(pars, x=x)
plt.plot(x, y, 'b.')
#plt.plot(x, init, 'k--')

out = mod.fit(y, pars, x=x)

print(out.fit_report(min_correl=0.5))    # Parameter result
result_txt = open(fileLocation + 'result_' + fileName, 'w')
result_txt.write(out.fit_report(min_correl=0.5))
result_txt.close()

plt.plot(x, out.best_fit, 'r-')    # Graph result
plt.show()

graphFit = np.transpose(np.vstack((x, out.best_fit)))   # Fitting result
np.savetxt(fileLocation + 'graph_' + fileName, graphFit, fmt = "%f, %f", newline = '\n')
