import pymongo
import pprint 
import timeit
from pymongo import MongoClient
from pprint import pprint
from timeit import Timer
from functools import partial

def rangeQuery(rankings):
	# SELECT pageURL, pageRank FROM rankings WHERE pageRank > X
	# The cursor that find() returns is probably lazy loaded, use count() to force load
	rankings.find({ "pageRank" : { "$gt": "26" }}).count()

client = MongoClient('localhost', 32768)
db = client['some-db']

rankings = db.rankings

rangeResult = Timer(partial(rangeQuery, rankings)).repeat(10, 1)
print("Range query result:")
pprint(rangeResult)