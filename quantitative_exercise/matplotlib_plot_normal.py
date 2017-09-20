import sys
import numpy as np
import scipy.stats as stats
import pylab as pl
import csv

if len(sys.argv) != 5:
    print("Usage: python matplotlib_plot_normal.py [filepath] [title] [x axis label] [y axis label]")
    sys.exit(0)

filePath = str(sys.argv[1])
title = str(sys.argv[2])
xLabel = str(sys.argv[3])
yLabel = str(sys.argv[4])

dataPoints = []

with open(filePath, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        # each row is a list of strings
        for dataPoint in row:
            dataPoints.append(float(dataPoint))

h = sorted(dataPoints)  #sorted

fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed

pl.plot(h,fit,'-o')
pl.title(title)
pl.xlabel(xLabel)
pl.ylabel(yLabel)

pl.hist(h,normed=True)      #use this to draw histogram of your data

pl.show()                   #use may also need add this
