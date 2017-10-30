YCSB-couchdb-binding
====================

CouchDB database interface for YCSB

Installation guide
==================

Download the YCSB project as follows:
```
git clone https://github.com/brianfrankcooper/YCSB.git
```
Change to the YCSB directory and checkout the latest stable version:
```
cd YCSB
git checkout 0.11.0
```
Include the YCSB CouchDB binding within the YCSB directory:
```
git clone https://github.com/arnaudsjs/YCSB-couchdb-binding.git couchdb
```
* Add `<module>couchdb</module>` to the list of modules in YCSB/pom.xml
* Add the following lines to the DATABASE section in YCSB/bin/ycsb:
`"couchdb" : "couchdb.CouchdbClient",`

Compile everything by executing the following command within the YCSB
directory:
```
mvn clean package
```
