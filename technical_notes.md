# Technical notes

## Docker

### Container and image management

Stop and remove all containers:

`docker stop $(docker ps -a -q)`

`docker rm $(docker ps -a -q)`

Delete all images:

`docker rmi $(docker images -q)`

### Set up mongoDB container from image

`docker pull mongo`

`docker run --name some-mongo -d mongo --auth`

(`docker ps`)

Add initial admin user

`docker exec -it some-mongo mongo admin`

`db.createUser({ user: 'jsmith', pwd: 'some-initial-password', roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });`

Connect externally (have to ctrl-c first to get out of the admin stuff)

`docker run -it --rm --link some-mongo:mongo mongo mongo -u jsmith -p some-initial-password --authenticationDatabase admin some-mongo/some-db`

