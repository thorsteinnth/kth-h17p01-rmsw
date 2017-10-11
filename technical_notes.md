# Technical notes

## Docker

### Container and image management

Stop and remove all containers:

`docker stop $(docker ps -a -q)`

`docker rm $(docker ps -a -q)`

Delete all images:

`docker rmi $(docker images -q)`

### Set up mongoDB container from image

Get the image if you don't have it already:

`docker pull mongo`

`docker run --name some-mongo -p 32768:27017 -d mongo --auth`

(`docker ps`)

Add initial admin user

`docker exec -it some-mongo mongo admin`

`db.createUser({ user: 'jsmith', pwd: 'some-initial-password', roles: [ { role: "root", db: "admin" } ] });`

*Note: Was running into some authorization issues, so the role was changed to root instead of userAdminAnyDatabase*

Connect externally (have to ctrl-c first to get out of the admin stuff)

`docker run -it --rm --link some-mongo:mongo mongo mongo -u jsmith -p some-initial-password --authenticationDatabase admin some-mongo/some-db`

### Import data to mongo via script

`python mongo_import_files_in_folder.py /Users/tts/Google\ Drive/School/MSc/KTH/H17P01/Research\ Methodology\ and\ Scientific\ Writing/Project/data/mongo_local/rankings some-db rankings 32768 true`

*Note: The container needs to have an access URL and port set, at least on the mac, so you can forward from a port on your machine into the docker container's VM. Can set that manually using Kitematic, or use the -p parameter in the first run command you use to start the container.*

## MongoDB

List all collections:

`db.getCollectionNames()`

