import sys
import os
from os import listdir
from os.path import isfile, isdir, join

# The rankings data is of the form: pageUrl,pageRank,avgDuration
# Example: jdprdgnhwrygvizhwxttnprtftlqpncrssviaphxiqmjpkizjwdgxi,6040,8

# The uservisits data is of the form: sourceIP, destUrl, visitDate, adRevenue, userAgent, countryCode, languageCode, searchWord, duration
# Example: 21.55.20.121,eqimjsndrccgvhrfemiwagdmwzsihdrevgzoupwvescaywpxssnrebppkvpxrvy,1976-04-16,0.46327674,Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1),ESP,ESP-CA,drinking,10

def getHelpText():
	return "Usage: python XXX.py [input file or folder path] [outputfilepath] [data format (rankings/uservisits)] [maxlines (0 to turn off)] [use couch import format (true/false)]"

if len(sys.argv) == 2:
	if str(sys.argv[1]) == "help":
		print(getHelpText())
		sys.exit(0)

if len(sys.argv) != 6:
    print(getHelpText())
    sys.exit(0)

# Argument parsing

inputPath = str(sys.argv[1])

inputPathIsFolder = isdir(inputPath)

if inputPathIsFolder:
	print("Input path is folder, will import all files under that folder")

outputFilePath = str(sys.argv[2])
dataformat = str(sys.argv[3])

if not (dataformat == "rankings" or dataformat == "uservisits"):
	print("Data format parameter should be \"rankings\" or \"uservisits\"")
	sys.exit(0)

print("Parsing " + dataformat)

maxLinesPerFile = int(sys.argv[4])

limitNumberOfLines = False
if (maxLinesPerFile > 0):
	limitNumberOfLines = True

useCouchImportFormat = str(sys.argv[5]) == "true"

if (useCouchImportFormat):
	print "Using CouchDB import format"
	
if (limitNumberOfLines and maxLinesPerFile < 10000):
	print "You really shouldn't have max lines per file less than 10000 or something. You will create way to many files and freeze your system. Exiting ..."
	sys.exit(1)

if (limitNumberOfLines):
	print str("Limiting number of lines per output file to " + str(maxLinesPerFile))
	print str("Output files will be called " + outputFilePath + " + a counter as a suffix")

# Methods

def getOutputFileName(path, suffix):
	if (suffix != ""):
		# Need to add a suffix
		# Have to handle if the path has a file extension, the suffix should come before the file extension
		filename, file_extension = os.path.splitext(path)
		if (file_extension != ""):
			return filename + "_" + suffix + file_extension
		else:
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
	print("Closing output file: " + str(file))
	file.close()

def formatLine(line):
	# Use rstrip() to remove the newline
	splitLine = line.rstrip().split(",")
	if (dataformat == "rankings"):
		return "{{ \"pageUrl\":\"{}\", \"pageRank\":{}, \"avgDuration\":{} }}".format(splitLine[0], splitLine[1], splitLine[2])
	elif (dataformat == "uservisits"):
		return "{{ \"sourceIP\":\"{}\", \"destUrl\":\"{}\", \"visitDate\":\"{}\", \"adRevenue\":{}, \"userAgent\":\"{}\", \"countryCode\":\"{}\", \"languageCode\":\"{}\", \"searchWord\":\"{}\", \"duration\":{} }}".format(splitLine[0], splitLine[1], splitLine[2], splitLine[3], splitLine[4], splitLine[5], splitLine[6], splitLine[7], splitLine[8])
	else:
		print("Unknown data format: " + dataformat)
		sys.exit(1)

def processInputFile(inputFilePath, initialOutputFileCounter):
	inputFile = open(inputFilePath, "r")

	lineCount = 0
	outputFileCount = initialOutputFileCounter

	outputFile = openOutputFile(outputFilePath, str(outputFileCount) if limitNumberOfLines else "")

	for line in inputFile:

		if (limitNumberOfLines and lineCount == maxLinesPerFile):
			# Close the current file and open a new one
			lineCount = 0
			outputFileCount = outputFileCount + 1
			closeOutputFile(outputFile)		
			outputFile = openOutputFile(outputFilePath, str(outputFileCount))

		formattedOutput = formatLine(line)
		
		if (useCouchImportFormat):
			outputFile.write(str(formattedOutput) + ",\n")
		else:
			outputFile.write(str(formattedOutput) + "\n")
		
		lineCount = lineCount+1

	closeOutputFile(outputFile)

	return outputFileCount

# Processing

# Note: The output file counter is zero based
if not inputPathIsFolder:
	outputFileCounter = 0
	outputFileCounter = processInputFile(inputPath, outputFileCounter)
	print(str(outputFileCounter + 1) + " output files generated")
else:
	# This is a folder, let's process all files in the folder
	# Get the path to all the files in the directory
	inputFiles = [str(inputPath + "/" + f) for f in listdir(inputPath) if isfile(join(inputPath, f)) and f != ".DS_Store" and not f.startswith("Icon")]
	print("Processing " + str(len(inputFiles)) + " input files ...")
	outputFileCounter = 0
	for inputFile in inputFiles:
		outputFileCounter = processInputFile(inputFile, outputFileCounter)
		outputFileCounter = outputFileCounter + 1
	print(str(outputFileCounter) + " output files generated")






