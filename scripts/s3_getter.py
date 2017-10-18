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

def format_part_number(input):	
	# The filenames are of the form part-00001
	# 5 characters, prepended with zeros
	if (len(input) == 5):
		return input
	elif (len(input) > 5):
		print("Part number should be 5 characters at most")
		sys.exit(0)
	else:
		# Need to prepend zeros
		prepend_length = 5-len(input)
		return "0" * prepend_length + input

print("Will get part numbers " + format_part_number(str(partnumber_from)) + " to " + format_part_number(str(partnumber_to)))

for partnumber in range(int(partnumber_from), int(partnumber_to) + 1):
	print("Getting part number " + format_part_number(str(partnumber)) + " going up to " + format_part_number(str(partnumber_to)) + " ...")
	call(["s3cmd", "get", "s3://big-data-benchmark/pavlo/text/5nodes/"+ data_type + "/part-" + format_part_number(str(partnumber)), local_save_path])