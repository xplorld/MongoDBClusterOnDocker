# MongoDBClusterOnDocker


[![Docker build](https://img.shields.io/docker/build/xplorld/mongodbclusterondocker.svg)](https://hub.docker.com/r/xplorld/mongodbclusterondocker/)


To let anyone open a mongoDB cluster without pain. (and without persistence)

# Usage
```bash
docker pull xplorld/mongodbclusterondocker
# create a cluster with:
# 5 routers
# 4 config servers
# 3 replicas per shard
# 2 shards
# db1 db2 db3 are sharded
# port 27017, 27018, 27019, 27020, 27021 are 5 routers
docker run -it -p 27017:27017 xplorld/mongodbclusterondocker --shardSize 2 --replicaSize 3 --configSize 4 --routerSize 5 --databases db1 db2 db3 
```

# ports

Suppose there is a cluster has `i` config servers, `j` routers, `n` shards, `z` replicas per shard, ports are:

| role | port |
|-|-|
config server | [`47000`, `47000+i`)
routers | [`27017`, `27017+j`)
shard #k | [`37000 + 100 * k`, `37000 + 100 * k + z`)

# Contribution

Welcomed

# Me

xplorld AT gmail.com

# Lisence

MIT

