# Technical notes

## Data formatting

**Script usage**

`python XXX.py [inputfilepath] [outputfilepath] [data format (rankings/uservisits)][maxlines (0 to turn off)] [use couch import format (true/false)]`

**Rankings for MongoDB**

`python json_convert.py /Users/tts/Google\ Drive/School/MSc/KTH/H17P01/Research\ Methodology\ and\ Scientific\ Writing/Project/sample_data/rankings /Users/tts/Desktop/rankings_json_mongo rankings 50000 false`

You can also point the script to a single file instead of a folder. If it is a folder, it will process all files under that folder

**Uservisits for MongoDB**

`python json_convert.py /Users/tts/Google\ Drive/School/MSc/KTH/H17P01/Research\ Methodology\ and\ Scientific\ Writing/Project/sample_data/uservisits /Users/tts/Desktop/uservisits_json_mongo uservisits 50000 false`

## Docker

###Misc

Open container shell:

`docker exec -i -t [container name] /bin/bash`

Install ping:

`apt-get update && apt-get install iputils-ping`

### Container and image management

Stop and remove all containers:

`docker stop $(docker ps -a -q)`

`docker rm $(docker ps -a -q)`

Delete all images:

`docker rmi $(docker images -q)`

### Set up mongoDB container from image

Get the image if you don't have it already:

`docker pull mongo`

Start container with authentication:

`docker run --name some-mongo -p 32768:27017 -d mongo --auth`

or without authentication:

`docker run --name some-mongo -p 32768:27017 -d mongo`

(`docker ps`)

Add initial admin user (only needed if you have authentication on):

`docker exec -it some-mongo mongo admin`

`db.createUser({ user: 'jsmith', pwd: 'some-initial-password', roles: [ { role: "root", db: "admin" } ] });`

*Note: Was running into some authorization issues, so the role was changed to root instead of userAdminAnyDatabase*

Connect externally (have to ctrl-c first to get out of the admin stuff)

If the conainer isn't running:

`docker start some-mongo`

`docker run -it --rm --link some-mongo:mongo mongo mongo -u jsmith -p some-initial-password --authenticationDatabase admin some-mongo/some-db`

or without authentication:

`docker run -it --rm --link some-mongo:mongo mongo mongo some-mongo/some-db`

### Import data to mongo via script

**Rankings**

`python mongo_import_files_in_folder.py /Users/tts/Google\ Drive/School/MSc/KTH/H17P01/Research\ Methodology\ and\ Scientific\ Writing/Project/data/mongo_local/rankings some-db rankings 32902 false false`

**Uservisits**

`python mongo_import_files_in_folder.py /Users/tts/Google\ Drive/School/MSc/KTH/H17P01/Research\ Methodology\ and\ Scientific\ Writing/Project/data/mongo_local/uservisits some-db uservisits 32902 false false`

*Note: The container needs to have an access URL and port set, at least on the mac, so you can forward from a port on your machine into the docker container's VM. Can set that manually using Kitematic, or use the -p parameter in the first run command you use to start the container.*

## MongoDB

List all collections:

`db.getCollectionNames()`

Mongostat:

`mongostat -h localhost:32768 --username jsmith --password some-initial-password --authenticationDatabase admin`

Get shard distribution for a collection:

`db.[collection].getShardDistribution()`

Get cluster status:

`sh.status()`

