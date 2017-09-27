import sys
import os

# The data is of the form: pageUrl,pageRank,avgDuration
# Example: jdprdgnhwrygvizhwxttnprtftlqpncrssviaphxiqmjpkizjwdgxi,6040,8

if len(sys.argv) != 4:
    print("Usage: python XXX.py [inputfilepath] [outputfilepath] [use couch import format (true/false)]")
    sys.exit(0)

inputFilePath = str(sys.argv[1])
inputFile = open(inputFilePath, "r")

outputFilePath = str(sys.argv[2])
outputFile = open(outputFilePath, "w")

useCouchImportFormat = str(sys.argv[3]) == "true"

if (useCouchImportFormat):
	print "Using CouchDB import format"

if (useCouchImportFormat):
	outputFile.write("{\n\"docs\": [\n")

for line in inputFile:
	# Use rstrip() to remove the newline
	splitLine = line.rstrip().split(",")
	formattedOutput = "{{ \"pageUrl\":\"{}\", \"pageRank\":\"{}\", \"avgDuration\":\"{}\" }}".format(splitLine[0], splitLine[1], splitLine[2])
	if (useCouchImportFormat):
		outputFile.write(str(formattedOutput) + ",\n")
	else:
		outputFile.write(str(formattedOutput) + "\n")

if (useCouchImportFormat):
	# Need to remove the trailing comma, lets just remove the last two characters
	outputFile.seek(-2, os.SEEK_END)
	outputFile.truncate()
	outputFile.write("\n]\n}")

outputFile.close()