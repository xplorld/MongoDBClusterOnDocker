# MongoDBClusterOnDocker
To let anyone open a mongoDB cluster without pain. (and without persistence)

# Usage
```
docker pull xplorld/mongodbclusterondocker
# create a cluster with:
# 5 routers
# 4 config servers
# 3 replicas per shard
# 2 shards
# db1 db2 db3 are sharded
# port 27017, 27018, 27019, 27020, 27021 are 5 routers
docker run -it -p 27017:27017 xplorld/mongodbclusterondocker 2 3 4 5 -dbs db1 db2 db3
```

# Contribution

Welcomed

# Me

xplorld AT gmail.com

# Lisence

MIT

