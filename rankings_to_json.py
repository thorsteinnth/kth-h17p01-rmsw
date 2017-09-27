import sys

# The data is of the form: pageUrl,pageRank,avgDuration
# Example: jdprdgnhwrygvizhwxttnprtftlqpncrssviaphxiqmjpkizjwdgxi,6040,8

if len(sys.argv) != 3:
    print("Usage: python XXX.py [inputfilepath] [outputfilepath]")
    sys.exit(0)

inputFilePath = str(sys.argv[1])
inputFile = open(inputFilePath, "r")

outputFilePath = str(sys.argv[2])
outputFile = open(outputFilePath, "w")

for line in inputFile:
	# Use rstrip() to remove the newline
	splitLine = line.rstrip().split(",")
	formattedOutput = "{{ \"pageUrl\":\"{}\", \"pageRank\":\"{}\", \"avgDuration\":\"{}\" }}".format(splitLine[0], splitLine[1], splitLine[2])
	outputFile.write(str(formattedOutput) + ",\n")

outputFile.close()