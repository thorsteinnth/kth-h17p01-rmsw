import couchdb
import sys
from os import listdir
from os.path import isfile, join
from subprocess import call

#Imports all file in the current directory 

def getHelpText():
	return "Usage: python XXX.py [dbname]"

couchserver = couchdb.Server('http://127.0.0.1:5984/')

# Input parameter parsing

if len(sys.argv) != 2:
    print(getHelpText())
    sys.exit(0)

dbname = str(sys.argv[1])
folderPath = "."

# import files

files = [str(folderPath + "/" + f) for f in listdir(folderPath) if isfile(join(folderPath, f)) and f != ".DS_Store"]

if dbname not in couchserver:
	db = couchserver.create(dbname)
else:
	db = couchserver[dbname]

# Run the import command for all the files
# curl -vX POST http://127.0.0.1:5984/dbname/_bulk_docs -d @bulk1.json -H
for file in files:
	print("Importing file: " + file)

	call(["curl", "--silent", "--output", "/dev/null", "-X", "POST", "http://127.0.0.1:5984/" + dbname + "/_bulk_docs",
		"-d", "@" + file, "-H", "Content-type: application/json"])



