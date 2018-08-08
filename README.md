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
docker run -it -p 27017:27017 xplorld/mongodbclusterondocker --shardSize 2 --replicaSize 3 --configSize 4 --routerSize 5 --host 127.0.0.1 --databases db1 db2 db3
```

# host

All servers share a same host, as speficied in `--host`. This host must be reachable from both inside the container and the client. If you are just using `docker run`, you can leave it alone and we will use default `127.0.0.1`. If you are in a more complicated environment, e.g. Kubernetes, you may want to specify a DNS name, as the client may not be in the same host with processes in the container.

# ports

Suppose there is a cluster has `i` config servers, `j` routers, `n` shards, `z` replicas per shard, ports are:

| role | port |
|-|-|
config server | [`47000`, `47000+i`)
routers | [`27017`, `27017+j`)
shard #k | [`37000 + 100 * k`, `37000 + 100 * k + z`)

# Kubernetes support

If you want to start up a MongoDB cluster on Kubernetes, be sure to
1. define a headless service with all used ports: config servers, routers and shards
2. define a pod with all used ports: config servers, routers and shards, and use `--host` argument as the service DNS name.


# Contribution

Welcomed

# Me

xplorld AT gmail.com

# Lisence

MIT

