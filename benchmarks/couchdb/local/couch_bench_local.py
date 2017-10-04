import couchdb

#CouchDB local benchmark

couchserver = couchdb.Server("http://127.0.0.1:5984/")

for dbname in couchserver:
    print(dbname)