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
	return "Usage: python XXX.py [host] [port] [benchmark (range/mapreduce/aggregation/workload)] [use authentication (true/false)]"

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
	uservisits.map_reduce(mapper, reducer, "total_duration_per_date")#, sort={"visitDate": 1})

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
			resultList.append([threadId, "update", str(result)])

def workflowReadOp(rankings):
	randomRank = random.randint(100,500)
	return rankings.find_one({ "pageRank" : randomRank })

def workflowUpdateOp(rankings):
	randomRank1 = random.randint(100,500)
	randomRank2 = random.randint(100,500)
	doc = rankings.find_one({ "pageRank" : randomRank1 })
	if doc is not None:
		doc["pageRank"] = randomRank2
		db.rankings.save(doc)
		return "updated"
	else:
		return "miss"

	# Can't do an update operation on a sharded collection unless the query contains the shard key
	# We are hash sharding on the object IDs, so we don't use this.	
	#return rankings.update_one(
	#	{ "pageRank" : randomRank1 },
	#	{
	#		"$set": {
	#			"pageRank" : randomRank2
	#		}
	#	}
	#)

def aggregationPipelineSum(uservisits):
	uservisits.aggregate([ { "$group": { "_id": "$visitDate", "value": { "$sum": "$duration" }}}, { "$sort" : { "_id" : 1 }} ])
	
# Main

# Input parsing

if len(sys.argv) != 5:
    print(getHelpText())
    sys.exit(1)

host = str(sys.argv[1])
port = int(sys.argv[2])
benchmark = str(sys.argv[3])
useAuthentication = str(sys.argv[4]) == "true"

if not (benchmark == "range" or benchmark == "mapreduce" or benchmark == "workload" or benchmark == "aggregation"):
	print(getHelpText())
	sys.exit(1)

print("Use authentication: " + str(useAuthentication))

# Hardcoded authentication stuff
username = "jsmith"
password = "some-initial-password"
authenticationDatabase = "admin"

client = MongoClient(host, port)

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

# Aggregation pipeline query

if (benchmark == "aggregation"):
	print("Running aggregation pipeline query...")
	aggregationResult = Timer(partial(aggregationPipelineSum, uservisits)).repeat(10, 1)
	print("Aggregation pipeline query result:")
	pprint(aggregationResult)

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
		readOpsMissed = [t for t in readOps if t[2] == "None"]
		updateOpsMissed = [t for t in updateOps if t[2] == "miss"]
		updateOpsCompleted = [t for t in updateOps if t[2] == "updated"]
		print("Read operations: " + str(len(readOps)) + " - Missed: " + str(len(readOpsMissed)))
		print("Update operations: " + str(len(updateOps)) + " - Missed: " + str(len(updateOpsMissed)) + " - Completed: " + str(len(updateOpsCompleted)))
	print("Workload simulation result")
	pprint(workloadResults)

