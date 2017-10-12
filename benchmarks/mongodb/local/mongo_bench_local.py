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

def workloadSimulation(mongoClient):
	threadCount = 200
	pool = ThreadPool(threadCount)
	workloadInput = []
	for i in range (0, threadCount):
		workloadInput.append([mongoClient, i])
	return pool.map(workloadInstance, workloadInput)

def workloadInstance(params):
	client = params[0]
	threadId = params[1]
	# Let's make half of the threads do a read operation, and half do an update operation
	if threadId % 2 == 0:
		#print "MY ID IS: " + str(threadId) + " and my read result is " + str(workflowReadOp(db.rankings))
		workflowReadOp(db.rankings)
	else:
		#print "MY ID IS: " + str(threadId) + " and my update result is " + str(workflowUpdateOp(db.rankings))
		workflowUpdateOp(db.rankings)

def workflowReadOp(rankings):
	randomRank = random.randint(100,500)
	return rankings.find_one({ "pageRank" : randomRank })

def workflowUpdateOp(rankings):
	randomRank1 = random.randint(100,500)
	randomRank2 = random.randint(100,500)
	return rankings.update(
		{ "pageRank" : randomRank1 },
		{
			"$set": {
				"pageRank" : randomRank2
			}

		}
	)
	
# Main

# Hardcoded authentication stuff
username = "jsmith"
password = "some-initial-password"
authenticationDatabase = "admin"

client = MongoClient('localhost', 32768)

authenticated = client['some-db'].authenticate(username, password, source=authenticationDatabase)
print "Authenticated: " + str(authenticated)

db = client['some-db']

rankings = db.rankings
uservisits = db.uservisits

# Range query

print("Running range query...")
rangeResult = Timer(partial(rangeQuery, rankings)).repeat(10, 1)
print("Range query result:")
pprint(rangeResult)

# MapReduce query

print("Running MapReduce query...")
mapReduceResult = Timer(partial(mapReduceTotalDurationPerDateQuery, uservisits)).repeat(10, 1)
print("MapReduce query result:")
pprint(mapReduceResult)

# Workload simulation

print("Running workload simulation...")
workloadResults = Timer(partial(workloadSimulation, db)).repeat(10, 1)
print("Workload simulation result")
pprint(workloadResults)
