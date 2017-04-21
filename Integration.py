#!/usr/bin/env python

"""
Semi-auto integration program

Steps:
1. File name and position
    fileLocation, fileName
2. Set spectrum range and background range
    Cancel exit() before Background-part
2. Background fitting
    Select background model and fit the data
    Cancel exit() at the end of Background-part
    Set bg_ parameters
3. Integrating and reports
"""

__author__ = "LI Kezhi"
__date__ = "$2017-02-26$"
__version__ = "1.0.1"

import numpy as np
from scipy import integrate
from lmfit.models import VoigtModel, LinearModel, PolynomialModel
import matplotlib.pyplot as plt
from scipy.integrate import simps
from __future__ import print_function

fileLocation = './Examples/Integration/'
fileName = 'A-MN10.csv'

start = 50      # Define the fitting range
end = 300

# Background setting
BG_FITTING_MODE = 'z'   # 't' for two-point method;
                        # 'z' for two-zone method
# Two-point method:
head0 = 53   # Head x point; integration range
end0 = 63
# Two-zone method:
head1 = 50   # Head x range: head1 < x < head2
             # Integration range: head2 < x < end1
head2 = 55
end1 = 250
end2 = 300

# Integration setting
INT_METHOD = 't'   # 't' for trapozoid integration
                   # 's' for Simpson's integration


###########################

##### Read data #####
dat = np.loadtxt(fileLocation + fileName, delimiter=',')
x_original = dat[:, 0]
y_original = dat[:, 1]

startLine, endLine = None, None
for i in xrange(np.size(x_original)):
    if x_original[i] >= start and startLine is None:
        startLine = i
    if startLine != None and endLine is None and x_original[i] >= end:
        endLine = i
        break
if startLine == endLine:
    starLine = 0
    endLine = np.size(x_original) - 1
if startLine is None:
    startLine = 0
if endLine is None:
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
        if x_original[i] >= head0 and startLine is None:
            startLine = i
        if startLine != None and x_original[i] >= end:
            endLine = i
    x_bg = [x_original[startLine], x_original[endLine]]
    y_bg = [y_original[startLine], y_original[endLine]]
elif BG_FITTING_MODE == 'z':
    startLine1, startLine2 = None, None
    endLine1, endLine2 = None, None
    for i in xrange(np.size(x_original)):
        if x_original[i] >= head1 and startLine1 is None:
            startLine1 = i
        if startLine1 != None and startLine2 is None and x_original[i] >= head2:
            startLine2 = i
        if x_original[i] >= end1 and endLine1 is None:
            endLine1 = i
        if endLine1 != None and endLine2 is None and x_original[i] >= end2:
            endLine2 = i
    x_bg = np.hstack((x_original[startLine1:startLine2],
                      x_original[endLine1:endLine2]))
    y_bg = np.hstack((y_original[startLine1:startLine2],
                      y_original[endLine1:endLine2]))

bg_mod = PolynomialModel(1, prefix='bg_')   # Background
pars = bg_mod.guess(y_bg, x=x_bg)

mod = bg_mod

init = mod.eval(pars, x=x_bg)
plt.plot(x, y, 'b.')

out = mod.fit(y_bg, pars, x=x_bg)

print(out.fit_report(min_correl=0.5))    # Parameter result

plt.plot(x_bg, out.eval(), 'r-')    # Background plotting
plt.xlim([x[0], x[-1]])
plt.show()

# exit()   # Stop here?


##### Integration #####
if BG_FITTING_MODE == 't':
    startInt = head0   # Integration range
    endInt = end0
elif BG_FITTING_MODE == 'z':
    startInt = head2
    endInt = end1

# Background subtraction
comp = out.eval_components(x=x)
out_param = out.params
y_bg_fit = bg_mod.eval(params=out_param, x=x)
y_bg_remove = y - y_bg_fit

startLine, endLine = None, None
for i in xrange(np.size(x)):
    if x[i] >= startInt and startLine is None:
        startLine = i
    if startLine != None and endLine is None and x[i] >= endInt:
        endLine = i
x_int = x_original[startLine:endLine]
y_int = y_bg_remove[startLine:endLine]
y_bg_fit_ = y_bg_fit[startLine:endLine]
y_orig = y_original[startLine:endLine]


if INT_METHOD == 't':
    integration = np.trapz(y_int, x_int)
elif INT_METHOD == 's':
    integration = integrate.simps(y_int, x_int)
print('Integration: ' + repr(integration))

# Plotting
plt.plot(x, y, 'b.')
plt.plot(x_bg, out.best_fit, 'r-')    # Background plotting
plt.xlim([x[0], x[-1]])
plt.fill_between(x_int, y_orig, y_bg_fit_, facecolor='green')
plt.show()


##### Text output #####

result_txt = open(fileLocation + 'integration_' + fileName + '.txt', 'w')
result_txt.write(out.fit_report(min_correl=0.5))
result_txt.write('\n')
result_txt.write('===================\n')
result_txt.write('Integration area = ' + repr(integration))
result_txt.write('Start from: ' + repr(startInt))
result_txt.write('End by: ' + repr(endInt))
result_txt.close()
