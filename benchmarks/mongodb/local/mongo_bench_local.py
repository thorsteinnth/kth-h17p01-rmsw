import pymongo
import pprint 
import timeit
from pymongo import MongoClient
from pprint import pprint
from timeit import Timer
from functools import partial
from bson.code import Code

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

print("Running range query...")
rangeResult = Timer(partial(rangeQuery, rankings)).repeat(10, 1)
print("Range query result:")
pprint(rangeResult)

print("Running MapReduce query...")
mapReduceResult = Timer(partial(mapReduceTotalDurationPerDateQuery, uservisits)).repeat(10, 1)
print("MapReduce query result:")
pprint(mapReduceResult)