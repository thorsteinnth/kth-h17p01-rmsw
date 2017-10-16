import sys
from subprocess import call

# Script for getting specific partnumbers from the dataset on Amazon S3

def getHelpText():
	return "Usage: python XXX.py [rankings/uservisits] [partnumber from] [partnumber to] [local save path]"

# Input parameter parsing

if len(sys.argv) != 5:
    print(getHelpText())
    sys.exit(1)

data_type = str(sys.argv[1])

if not (data_type == "rankings" or data_type == "uservisits"):
	print("Wrong datatype: " + data_type)
	print(getHelpText())
	sys.exit(1)

partnumber_from = sys.argv[2]
partnumber_to = sys.argv[3]
local_save_path = sys.argv[4]

for partnumber in range(int(partnumber_from), int(partnumber_to) + 1):
	print("Getting part number " + str(partnumber) + " ...")
	call(["s3cmd", "get", "s3://big-data-benchmark/pavlo/text/5nodes/"+ data_type + "/part-000" + str(partnumber), local_save_path])