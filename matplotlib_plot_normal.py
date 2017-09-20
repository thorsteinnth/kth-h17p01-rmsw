import sys
import numpy as np
import scipy.stats as stats
import pylab as pl
import csv

if len(sys.argv) != 2:
    print("Usage: python matplotlib_plot_normal.py [filepath]")
    sys.exit(0)

filePath = str(sys.argv[1])

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

pl.hist(h,normed=True)      #use this to draw histogram of your data

pl.show()                   #use may also need add this
