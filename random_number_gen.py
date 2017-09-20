import sys
import random

if len(sys.argv) == 2 and sys.argv[1] == "help":
    print("Usage: python random_number_gen.py [number of random numbers desired] [min] [max]")

numberCount = int(sys.argv[1])
minNumber = int(sys.argv[2])
maxNumber = int(sys.argv[3])

for x in range(numberCount):
    if (x != numberCount-1):
        print str(random.randint(minNumber, maxNumber))+",",
    else:
        print str(random.randint(minNumber, maxNumber)),
