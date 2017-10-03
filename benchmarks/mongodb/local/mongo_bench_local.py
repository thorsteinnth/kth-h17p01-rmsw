import pymongo
import pprint 
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 32768)
db = client['some-db']

rankings = db.rankings

# SELECT pageURL, pageRank FROM rankings WHERE pageRank > X
cursor = rankings.find({ "pageRank" : { "$gt": "26" }})

pprint(cursor.count())