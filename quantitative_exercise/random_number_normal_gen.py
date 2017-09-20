from __future__ import print_function
import sys
import random
import numpy

if len(sys.argv) == 2 and sys.argv[1] == "help":
    print("Usage: python random_number_normal_gen.py [number of random numbers desired] [Mean] [Standard deviation]")
    sys.exit(0)

numberCount = int(sys.argv[1])
mean = int(sys.argv[2])
sd = int(sys.argv[3])

for x in range(numberCount):
    randomNumber = numpy.random.normal(mean, sd)
    if (x != numberCount-1):
        print(str(randomNumber) + ",", end='')
    else:
        print(str(randomNumber))
