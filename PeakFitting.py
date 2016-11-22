#!/usr/bin/env python

"""
Semi-auto fitting program

Steps:
1. File name and position
    fileLocation, fileName
2. Set spectrum range and background range
    Cancel exit() before Background-part
2. Background fitting
    Select background model and fit the data
    Cancel exit() at the end of Background-part
    Set bg_ parameters
3. Peaks information and initial guess
    Peak type, initial estimation
    Cancel exit() and plotting codes after estimation-part
4. Fitting
    Modify fitting parameters
    Cancel last exit()
    Do remember to change report/plotting format parameters
5. Plotting and reports
"""

__author__ = "LI Kezhi" 
__date__ = "$2016-11-22$"
__version__ = "1.2"

import numpy as np
from lmfit.models import VoigtModel, LinearModel, PolynomialModel
import sys
import matplotlib.pyplot as plt
from scipy.integrate import simps

fileLocation = './Examples/'
fileName = 'Mn0-100.txt'

start = 52.0      # Define the fitting range
end = 64.0

# Background setting
BG_FITTING_MODE = 'z'   # 't' for two-point method;
                        # 'z' for two-zone method
# Two-point method:
head0 = 53   # Head x point
end0 = 63
# Two-zone method:
head1 = 52.1   # Head x range: head1 < x < head2
head2 = 54
end1 = 61
end2 = 63.9

###########################

##### Read data #####
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


##### Original Data #####
plt.plot(x, y, 'b.')
plt.show() # First glimpse

# exit()   # Stop here?

##### Background #####
if BG_FITTING_MODE == 't':
    startLine, endLine = None, None
    for i in xrange(np.size(x_original)):
        if x_original[i] >= head0 and startLine == None:
            startLine = i
        if startLine != None and x_original[i] >= end:
            endLine = i
    x_bg = [x_original[startLine], x_original[endLine]]
    y_bg = [y_original[startLine], y_original[endLine]]
elif BG_FITTING_MODE == 'z':
    startLine1, startLine2 = None, None
    endLine1, endLine2 = None, None
    for i in xrange(np.size(x_original)):
        if x_original[i] >= head1 and startLine1 == None:
            startLine1 = i
        if startLine1 != None and startLine2 == None and x_original[i] >= head2:
            startLine2 = i
        if x_original[i] >= end1 and endLine1 == None:
            endLine1 = i
        if endLine1 != None and endLine2 == None and x_original[i] >= end2:
            endLine2 = i
    x_bg = np.hstack((x_original[startLine1:startLine2], 
                                x_original[endLine1:endLine2]))
    y_bg = np.hstack((y_original[startLine1:startLine2],
                                y_original[endLine1:endLine2]))

bg_mod = PolynomialModel(2, prefix='bg_')   # Background
pars = bg_mod.guess(y_bg, x=x_bg)

mod = bg_mod     

init = mod.eval(pars, x=x_bg)
plt.plot(x, y, 'b.')

out = mod.fit(y_bg, pars, x=x_bg)

print(out.fit_report(min_correl=0.5))    # Parameter result

plt.plot(x_bg, out.best_fit, 'r-')    # Background plotting
plt.xlim([x[0], x[-1]])
plt.show()

# exit()   # Stop here?
pars['bg_c0'].set(-941.6)   # Set parameters after fitting bg
pars['bg_c1'].set(34.81)
pars['bg_c2'].set(-0.3106)

##### Peak Fitting #####
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
# plt.plot(x, init, 'k--')   # Initial guess plotting
# plt.show()   # Initial guess plotting
# exit()   # Stop here?

out = mod.fit(y, pars, x=x)

print(out.fit_report(min_correl=0.5))    # Parameter result

plt.plot(x, out.best_fit, 'r-')    # Graph result
comps = out.eval_components(x=x)
plt.plot(x, comps['bg_'], 'g-')            # Plot the background and the peaks
plt.plot(x, comps['p1_'] + comps['bg_'],  'k-')
plt.plot(x, comps['p2_'] + comps['bg_'],  'k-')
plt.show()

# exit()   # Stop here?


##### Text output #####

result_txt = open(fileLocation + 'result_' + fileName, 'w')
result_txt.write(out.fit_report(min_correl=0.5))
result_txt.write('\n')
result_txt.write('===================\n')
comps = out.eval_components(x=x)
area1 = simps(comps['p1_'], x)           # Integration results
area2 = simps(comps['p2_'], x)
result_txt.write('Area1 = ' + str(area1) + ', Area2 = ' + str(area2))
result_txt.close()

graphFit = np.transpose(np.vstack((x, out.best_fit, comps['bg_'], comps['p1_'], comps['p2_'])))   # Fitting result
np.savetxt(fileLocation + 'graph_' + fileName, graphFit, fmt = "%f, %f, %f, %f, %f", newline = '\n')


