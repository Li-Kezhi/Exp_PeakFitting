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
5. Report
    area1 = simps(comps['p1_'], x)
6. Plotting
    plot(x, comps[...])
"""

import numpy as np
from lmfit.models import PseudoVoigtModel, LinearModel
import sys
import matplotlib.pyplot as plt
from scipy.integrate import simps

fileLocation = 'E:\\temp\\'
fileName = 'O1s.txt'

start = 1      # Define the fitting range
end = 2

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
if startLine == endLine:
    starLine = 0
    endLine = np.size(x_original) - 1
if startLine == None:
    startLine = 0
if endLine == None:
    endLine = np.size(x_original) - 1

x = x_original[startLine:endLine]
y = y_original[startLine:endLine]


bg_mod = LinearModel(prefix='bg_')   # Background
pars = bg_mod.guess(y, x=x)

pars['bg_slope'].set(409)
pars['bg_intercept'].set(-210000)
pars['bg_slope'].set(vary = False)
pars['bg_intercept'].set(vary = False)

peak1  = PseudoVoigtModel(prefix='p1_')    # Peak information
pars.update(peak1.make_params())

pars['p1_center'].set(531.608488)
pars['p1_amplitude'].set(282890, min=0)
pars['p1_sigma'].set(0.55824521)
pars['p1_fraction'].set(0.3, min = 0.25, max = 0.35)

peak2  = PseudoVoigtModel(prefix='p2_')
pars.update(peak2.make_params())

pars['p2_center'].set(529.8)
pars['p2_amplitude'].set(80000, min=0)
pars['p2_sigma'].set(0.5, min = 0.05, max = 2)
pars['p2_fraction'].set(expr = 'p1_fraction')

mod = peak1 + peak2 + bg_mod      # Add-up
#mod = bg_mod


init = mod.eval(pars, x=x)
plt.plot(x, y, 'b.')
plt.plot(x, init, 'k--')
#plt.show()

out = mod.fit(y, pars, x=x)

print(out.fit_report(min_correl=0.5))    # Parameter result
result_txt = open(fileLocation + 'result_' + fileName, 'w')
result_txt.write(out.fit_report(min_correl=0.5))
result_txt.write('\n')
result_txt.write('===================\n')
comps = out.eval_components(x=x)
area1 = simps(comps['p1_'], x)           # Integration results
area2 = simps(comps['p2_'], x)
result_txt.write('Area1 = ' + str(area1) + ', Area2 = ' + str(area2))
result_txt.close()

plt.plot(x, out.best_fit, 'r-')    # Graph result
plt.plot(x, comps['bg_'], 'g-')            # Plot the background and the peaks
plt.plot(x, comps['p1_'] + comps['bg_'],  'k-')
plt.plot(x, comps['p2_'] + comps['bg_'],  'k-')
plt.show()

graphFit = np.transpose(np.vstack((x, out.best_fit, comps['bg_'], comps['p1_'], comps['p2_'])))   # Fitting result
np.savetxt(fileLocation + 'graph_' + fileName, graphFit, fmt = "%f, %f, %f, %f, %f", newline = '\n')


