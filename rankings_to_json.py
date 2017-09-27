import sys
import os

# The data is of the form: pageUrl,pageRank,avgDuration
# Example: jdprdgnhwrygvizhwxttnprtftlqpncrssviaphxiqmjpkizjwdgxi,6040,8

if len(sys.argv) != 5:
    print("Usage: python XXX.py [inputfilepath] [outputfilepath] [maxlines (0 to turn off)] [use couch import format (true/false)]")
    sys.exit(0)

# Argument parsing

inputFilePath = str(sys.argv[1])
outputFilePath = str(sys.argv[2])
maxLinesPerFile = int(sys.argv[3])

limitNumberOfLines = False
if (maxLinesPerFile > 0):
	limitNumberOfLines = True

useCouchImportFormat = str(sys.argv[4]) == "true"

if (useCouchImportFormat):
	print "Using CouchDB import format"
	
if (limitNumberOfLines and maxLinesPerFile < 10000):
	print "You really shouldn't have max lines per file less than 10000 or something. You will create way to many files and freeze your system. Exiting ..."
	sys.exit(1)

if (limitNumberOfLines):
	print str("Limiting number of lines per output file to " + str(maxLinesPerFile))
	print str("Output files will be called " + outputFilePath + "_XXX")

# Methods

def getOutputFileName(path, suffix):
	if (suffix != ""):
		return path + "_" + suffix
	else:
		return path

def openOutputFile(path, suffix):
	outputFile = open(getOutputFileName(path, suffix), "w")
	# Couch DB needs output docs to contain a single JSON document
	if (useCouchImportFormat):
		outputFile.write("{\n\"docs\": [\n")
	return outputFile

def closeOutputFile(file):
	if (useCouchImportFormat):
		# Couch DB needs output docs to contain a single JSON document
		# Need to remove the trailing comma, lets just remove the last two characters
		file.seek(-2, os.SEEK_END)
		file.truncate()
		file.write("\n]\n}")
	file.close()

# Processing

inputFile = open(inputFilePath, "r")

lineCount = 0
outputFileCount = 0

outputFile = openOutputFile(outputFilePath, str(outputFileCount) if limitNumberOfLines else "")

for line in inputFile:

	if (limitNumberOfLines and lineCount == maxLinesPerFile):
		# Close the current file and open a new one
		lineCount = 0
		outputFileCount = outputFileCount + 1
		closeOutputFile(outputFile)		
		outputFile = openOutputFile(outputFilePath, str(outputFileCount))

	# Use rstrip() to remove the newline
	splitLine = line.rstrip().split(",")
	formattedOutput = "{{ \"pageUrl\":\"{}\", \"pageRank\":\"{}\", \"avgDuration\":\"{}\" }}".format(splitLine[0], splitLine[1], splitLine[2])
	
	if (useCouchImportFormat):
		outputFile.write(str(formattedOutput) + ",\n")
	else:
		outputFile.write(str(formattedOutput) + "\n")
	
	lineCount = lineCount+1

closeOutputFile(outputFile)






