import sys
from os import listdir
from os.path import isfile, join
from subprocess import call

def getHelpText():
	return "Usage: python XXX.py [folder] [dbname] [collection] [port] [drop collection before import (true/false)]"

# Input parameter parsing

if len(sys.argv) != 6:
    print(getHelpText())
    sys.exit(0)

folderPath = str(sys.argv[1])
dbname = str(sys.argv[2])
collection = str(sys.argv[3])
port = str(sys.argv[4])
dropCollection = str(sys.argv[5]) == "true"

# Import stuff

# https://docs.mongodb.com/manual/tutorial/write-scripts-for-the-mongo-shell/#scripting

if dropCollection:
	# Lets drop the collection before importing
	# mongo <dbname> --eval 'db.<collection>.drop()'
	print("Current collections:")
	call(["mongo", "localhost:" + port + "/" + dbname, "--eval", "db.getCollectionNames()"])
	print("Dropping collection " + collection)
	call(["mongo", "localhost:" + port + "/" + dbname, "--eval", "db." + collection + ".drop()"])
	print("Current collections after delete:")
	call(["mongo", "localhost:" + port + "/" + dbname, "--eval", "db.getCollectionNames()"])

# Get the path to all the files in the directory
files = [str(folderPath + "/" + f) for f in listdir(folderPath) if isfile(join(folderPath, f)) and f != ".DS_Store"]

# Run the import command for all the files
# mongoimport --db some-db --collection rankings --drop --port 32768 --file /Users/tts/Google\ Drive/School/MSc/KTH/H17P01/Research\ Methodology\ and\ Scientific\ Writing/Project/data/mongo_local/rankings/rankings_json_mongo_0
for file in files:
	# NOTE: Can add parameter "--drop" here to to drop the collection before each import
	print("Importing file: " + file)
	call(["mongoimport", "--db", dbname, "--collection", collection, "--port", port, "--file", file])

# Print total number of items in collection
print("Number of items in collection " + collection + ":")
call(["mongo", "localhost:" + port + "/" + dbname, "--eval", "db." + collection + ".find().count()"])


