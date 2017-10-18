import sys
import pymongo
import pprint 
import timeit
import random
from pymongo import MongoClient
from pprint import pprint
from timeit import Timer
from functools import partial
from bson.code import Code
from multiprocessing.dummy import Pool as ThreadPool

# Functions

def getHelpText():
	return "Usage: python XXX.py [benchmark (range/mapreduce/workload)] [use authentication (true/false)]"

def rangeQuery(rankings):
	# SELECT pageURL, pageRank FROM rankings WHERE pageRank > X
	# The cursor that find() returns is probably lazy loaded, use count() to force load
	rankings.find({ "pageRank" : { "$gt": "26" }}).count()

def mapReduceTotalDurationPerDateQuery(uservisits):
	# Find the total duration of all visits on each date
	mapper = Code("""
		function() { emit( this.visitDate, this.duration ); }
		""")
	reducer = Code("""
		function(key, values) { return Array.sum( values ) }
		""")
	uservisits.map_reduce(mapper, reducer, "total_duration_per_date")

def workloadSimulation(params):
	db = params[0]
	resultList = params[1]
	saveResult = params[2]
	threadCount = 200
	pool = ThreadPool(threadCount)
	workloadInput = []
	for i in range (0, threadCount):
		workloadInput.append([db, i, resultList, saveResult])
	return pool.map(workloadInstance, workloadInput)

def workloadInstance(params):
	db = params[0]
	threadId = params[1]
	resultList = params[2]
	saveResult = params[3]
	# Let's make half of the threads do a read operation, and half do an update operation
	# Note: List.append is thread safe
	if threadId % 2 == 0:
		result = workflowReadOp(db.rankings)
		if (saveResult):
			resultList.append([threadId, "read", str(result)])
	else:
		result = workflowUpdateOp(db.rankings)
		if (saveResult):
			resultList.append([threadId, "update", str(result.raw_result)])

def workflowReadOp(rankings):
	randomRank = random.randint(100,500)
	return rankings.find_one({ "pageRank" : randomRank })

def workflowUpdateOp(rankings):
	randomRank1 = random.randint(100,500)
	randomRank2 = random.randint(100,500)
	return rankings.update_one(
		{ "pageRank" : randomRank1 },
		{
			"$set": {
				"pageRank" : randomRank2
			}

		}
	)
	
# Main

# Input parsing

if len(sys.argv) != 3:
    print(getHelpText())
    sys.exit(1)

benchmark = str(sys.argv[1])
useAuthentication = str(sys.argv[2]) == "true"

if not (benchmark == "range" or benchmark == "mapreduce" or benchmark == "workload"):
	print(getHelpText())
	sys.exit(1)

print("Use authentication: " + str(useAuthentication))

# Hardcoded authentication stuff
username = "jsmith"
password = "some-initial-password"
authenticationDatabase = "admin"

client = MongoClient('localhost', 32768)

if useAuthentication:
	authenticated = client['some-db'].authenticate(username, password, source=authenticationDatabase)
	print "Authenticated: " + str(authenticated)

db = client['some-db']

rankings = db.rankings
uservisits = db.uservisits

# Range query

if (benchmark == "range"):
	print("Running range query...")
	rangeResult = Timer(partial(rangeQuery, rankings)).repeat(10, 1)
	print("Range query result:")
	pprint(rangeResult)

# MapReduce query

if (benchmark == "mapreduce"):
	print("Running MapReduce query...")
	mapReduceResult = Timer(partial(mapReduceTotalDurationPerDateQuery, uservisits)).repeat(10, 1)
	print("MapReduce query result:")
	pprint(mapReduceResult)

# Workload simulation

if (benchmark == "workload"):
	print("Running workload simulation...")
	opResults = []
	saveOpResults = False
	workloadResults = Timer(partial(workloadSimulation, [db, opResults, saveOpResults])).repeat(10, 1)
	if saveOpResults:
		print("Operation results")
		readOps = [t for t in opResults if t[1] == "read"]
		updateOps = [t for t in opResults if t[1] == "update"]
		print("Read operations: " + str(len(readOps)))
		print("Update operations: " + str(len(updateOps)))
	print("Workload simulation result")
	pprint(workloadResults)

