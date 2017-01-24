#!/usr/bin/env python

"""
Semi-auto fitting program

Steps:
1. Set spectrum range and background range
2. Background fitting
    Select background model and fit the data
    Set bg_ parameters
3. Peaks information and initial guess
    Peak type, initial estimation
4. Fitting
    Modify fitting parameters
5. Plotting and reports
"""

__author__ = "LI Kezhi" 
__date__ = "$2017-01-24$"
__version__ = "1.3.1"

import numpy as np
from lmfit.models import VoigtModel, PolynomialModel
import matplotlib.pyplot as plt
from scipy.integrate import simps

FILE_LOCATION = './Examples/PeakFitting/'
FILE_NAME = 'Mn0-100.txt'

PLOT_HEAD = 52.0      # Define the fitting range
PLOT_END = 64.0

# Background setting
BG_FITTING_MODE = 'z'   # 't' for two-point method;
                        # 'z' for two-zone method
# Two-point method:
BG_HEAD_TPM = 53   # Head x point
BG_END_TPM = 63
# Two-zone method:
BG_HEAD_LEFT_TZM = 52.1   # x range: BG_HEAD_LEFT_TZM < x < BG_HEAD_RIGHT_TZM
BG_HEAD_RIGHT_TZM = 54
BG_END_LEFT_TZM = 61
BG_END_RIGHT_TZM = 63.9

# Fitting parameters:
BG_TYPE = 2  # 1: linear, 2: parabolic

PEAK_NAMES = (
    'p1_',
    'p2_'
)

PEAK_CENTER = (
    (56, None, 58),  # center, min, max
    (59, 57, 61)
)

PEAK_AMPLITUDE = (
    (2000, 0),  # amplitude, min
    (2000, 0)
)

PEAK_SIGMA = (
    (None, None, None),  # sigma, min, max
    (None, None, None)
)

# Program Control:
controlStatas = (
    'Initial glimpse',
    'Background fitting',
    'Initial guess',
    'Curve fitting',
    'Report'
)
STATUS = controlStatas[4]  # Choose the current program status

###########################

##### Pre-fuctions #####
def dataSelect(data, start, end):
    '''
    Return selected data in a given range
    data: two-row np.array
    start/end:
        floats: return x and y if start < x < end
        list of floats: return x and y if start[i] < x < end[i]
        Make sure that start < end, and start[i] < start[i+1], same for end
    return: tuple of (x, y)
    '''
    if data[0, 0] > data[-1, 0]:
        dataCopy = np.flipud(data)
    x, y = data[:, 0], data[:, 1]
    
    if type(start) == float or type(start) == int:
        assert start < end, 'start should be less than end'
        startLine, endLine = None, None
        for i in xrange(np.size(x)):
            if startLine == None and x[i] >= start:
                startLine = i
            if startLine != None and endLine == None and x[i] >= end:
                endLine = i
                break
        if startLine == None:
            startLine = 0
        if endLine == None:
            endLine = np.size(x_original) - 1
        xSelect = x[startLine:endLine]
        ySelect = y[startLine:endLine]
    else:
        assert start[0] < end[0], 'start should be less than end'
        assert start[0] < start[1], 'start should be in a increasing trend'
        assert end[0] < end[1], 'start should be in a increasing trend'
        assert end[0] < start[1], 'end[0] should be less than start[1]'
        assert len(x) == len(y), 'start should have same numbers of values as end'
        pairs = []
        for i, item in enumerate(start):
            pairs.append((start[i], end[i]))
        
        xSelect, ySelect = np.array([]), np.array([])
        for pair in pairs:
            startLine, endLine = None, None
            for i in xrange(np.size(x)):
                if startLine == None and x[i] >= pair[0]:
                    startLine = i
                if startLine != None and endLine == None and x[i] >= pair[1]:
                    endLine = i
                    break
            if startLine == None:
                startLine = 0
            if endLine == None:
                endLine = np.size(x_original) - 1
            xSelect = np.hstack((xSelect, x[startLine:endLine])) 
            ySelect = np.hstack((ySelect, y[startLine:endLine])) 
            x = x[endLine:]
            y = y[endLine:]

    return (xSelect, ySelect)

##### Read data #####
dat = np.loadtxt(FILE_LOCATION + FILE_NAME)
x_original = dat[:, 0]
y_original = dat[:, 1]

x, y = dataSelect(dat, PLOT_HEAD, PLOT_END)

##### Original Data #####
if STATUS == 'Initial glimpse':
    plt.plot(x, y, 'b.')
    plt.show() # First glimpse
    exit()

##### Background #####
if BG_FITTING_MODE == 't':
    x_bg, y_bg = dataSelect(dat, BG_HEAD_TPM, BG_END_TPM)
    x_bg = [x_bg[0], x_bg[-1]]  # Only leave two points
    y_bg = [y_bg[0], y_bg[-1]]
elif BG_FITTING_MODE == 'z':
    bg_head = (BG_HEAD_LEFT_TZM, BG_END_LEFT_TZM)
    bg_end = (BG_HEAD_RIGHT_TZM, BG_END_RIGHT_TZM)
    x_bg, y_bg = dataSelect(dat, bg_head, bg_end)

bg_mod = PolynomialModel(BG_TYPE, prefix='bg_')   # Background
pars = bg_mod.guess(y_bg, x=x_bg)

mod = bg_mod     

init = mod.eval(pars, x=x_bg)
plt.plot(x, y, 'b.')

out = mod.fit(y_bg, pars, x=x_bg)

if STATUS == 'Background fitting':
    print(out.fit_report(min_correl=0.5))    # Parameter result

    plt.plot(x_bg, out.best_fit, 'r-')    # Background plotting
    plt.xlim([x[0], x[-1]])
    plt.show()

    exit()

pars = out.params

##### Peak Fitting #####
peaks = []
peakParameters = {}
for i, peak in enumerate(PEAK_NAMES):
    peakParameters[peak] = {}
    peakParameters[peak]['center'] = PEAK_CENTER[i]
    peakParameters[peak]['amplitude'] = PEAK_AMPLITUDE[i]
    peakParameters[peak]['sigma'] = PEAK_SIGMA[i]
mod = bg_mod
for i, peak in enumerate(PEAK_NAMES):
    peaks.append(VoigtModel(prefix=peak))  # Peak information
    pars.update(peaks[i].make_params())

    pars[peak + 'center'].set(
        peakParameters[peak]['center'][0],
        min=peakParameters[peak]['center'][1], 
        max=peakParameters[peak]['center'][2]
        )
    pars[peak + 'amplitude'].set(
        peakParameters[peak]['amplitude'][0],
        min=peakParameters[peak]['amplitude'][1]
        )
    pars[peak + 'sigma'].set(
        peakParameters[peak]['sigma'][0],
        min=peakParameters[peak]['sigma'][1],
        max=peakParameters[peak]['sigma'][2]
        )

    mod += peaks[i]

init = mod.eval(pars, x=x)
plt.plot(x, y, 'b.')

if STATUS == 'Initial guess':
    plt.plot(x, init, 'k--')   # Initial guess plotting
    plt.show()   # Initial guess plotting
    exit()

out = mod.fit(y, pars, x=x)

plt.plot(x, out.best_fit, 'r-')    # Graph result
comps = out.eval_components(x=x)
plt.plot(x, comps['bg_'], 'g-')  # Plot the background and the peaks
for i, peak in enumerate(PEAK_NAMES):
    plt.plot(x, comps[peak] + comps['bg_'],  'k-')
plt.show()

if STATUS == 'Curve fitting':
    print(out.fit_report(min_correl=0.5))    # Parameter result
    exit()   


##### Text output #####

result_txt = open(FILE_LOCATION + 'result_' + FILE_NAME, 'w')
result_txt.write(out.fit_report(min_correl=0.5))
result_txt.write('\n')
result_txt.write('===================\n')
comps = out.eval_components(x=x)

for i, peak in enumerate(PEAK_NAMES):
    area = simps(comps[peak], x)  # Integration results
    result_txt.write('Area ' + str(i) + ': ' + str(area) + '\n')

result_txt.close()

resultFittingData = np.vstack((x, out.best_fit, comps['bg_']))
headerStr = 'x  Fit  Background'
for i, peak in enumerate(PEAK_NAMES):
    resultFittingData = np.vstack((resultFittingData, comps[peak]))
    headerStr += '  peak' + str(i)
graphFit = np.transpose(resultFittingData)   # Fitting result
np.savetxt(
    FILE_LOCATION + 'graph_' + FILE_NAME, graphFit, newline = '\n',
    header=headerStr
)

print('Successfully fitted and the report is generated!')