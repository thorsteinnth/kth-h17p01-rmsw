import couchdb
import sys
import pprint 
import timeit
import random
from pprint import pprint
from timeit import Timer
from subprocess import call
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool

# CouchDB local benchmark
# We have already created views for the data

def getHelpText():
	return "Usage: python XXX.py [benchmark (range/mapreduce/workload)]"

def rangeQuery():
	for row in db.view("_design/benchmarks/_view/pagerankcount", startkey=26):
		print(row)

def mapReduceQuery():
	res = db.view("_design/benchmarks/_view/totalduration", group=True)
	length = len(res) # dummy op to access the view - iterate it

def mapReduceSlowQuery():
	res = db.view("_design/benchmarks/_view/totaldurationslow", group=True)
	length = len(res) # dummy op to access the view - iterate it

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
	client = params[0]
	threadId = params[1]
	resultList = params[2]
	saveResult = params[3]

	if threadId % 2 == 0:
		result = workflowReadOp()
		if (saveResult):
			resultList.append([threadId, "read", str(result)])
	else:
		result = workflowUpdateOp()
		if (saveResult):
			resultList.append([threadId, "update", str(result)])

def workflowReadOp():
	randomRank = random.randint(100,500)
	
	viewResult = db.view("_design/benchmarks/_view/pagerank", key=randomRank, limit=1)

	if(len(viewResult.rows) > 0):
		row = viewResult.rows[0]
		doc = row.value
		return doc['_id']
	else:
		return "get failed"

def workflowUpdateOp():
	randomRank1 = random.randint(100,500)
	randomRank2 = random.randint(100,500)

	viewResult = db.view("_design/benchmarks/_view/pagerank", key=randomRank1, limit=1)
	
	if(len(viewResult.rows) > 0):
		row = viewResult.rows[0]
		doc = row.value
		doc["pageRank"] = randomRank2
		try:
			docId, docRev = db.save(doc)
			return docId
		except Exception as e:
			return e
	else:
		return "get failed"

# MAIN

if len(sys.argv) != 2:
    print(getHelpText())
    sys.exit(1)

benchmark = str(sys.argv[1])

if not (benchmark == "range" or benchmark == "mapreduce" or benchmark == "workload"):
	print(getHelpText())
	sys.exit(1)

couchserver = couchdb.Server('http://127.0.0.1:5984/')
dbname = 'bench'
db = couchserver[dbname]

# BENCHMARK TEST #1 - RANGE QUERY

if (benchmark == "range"):
	rangeResult = Timer(rangeQuery).repeat(10, 1)
	print("Range query result:")
	pprint(rangeResult)


# BENCHMARK TEST #2 - MAPREDUCE

if(benchmark == "mapreduce"):
	mapReduceResult = Timer(mapReduceQuery).repeat(10, 1)
	print("MapReduce query result:")
	pprint(mapReduceResult)

	#mapReduceSlowResult = Timer(mapReduceSlowQuery).repeat(2, 1)
	#print("MapReduce SLOW query result:")
	#pprint(mapReduceSlowResult)


# BENCHMARK TEST #3 - WORKLOAD

if (benchmark == "workload"):
	opResults = []
	saveOpResults = True
	workloadResults = Timer(partial(workloadSimulation, 
		[db, opResults, saveOpResults])).repeat(10, 1)
	
	if saveOpResults:
		print("Operation results")
		readOps = [t for t in opResults if t[1] == "read"]
		updateOps = [t for t in opResults if t[1] == "update"]
		print("Read operations: " + str(len(readOps)))
		print("Update operations: " + str(len(updateOps)))
	
	print("Workload simulation result;")
	pprint(workloadResults)







