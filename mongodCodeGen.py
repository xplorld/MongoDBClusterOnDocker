#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser(
    description='mongodb bootstrap code generator')
parser.add_argument('--shardSize', type=int, required=True)
parser.add_argument('--replicaSize', type=int, required=True)
parser.add_argument('--configSize', type=int, required=True)
parser.add_argument('--routerSize', type=int, required=True)
parser.add_argument('--configReplSetName', type=str,
                    default='mongoreplsetconfig')
parser.add_argument('--host', type=str, default='127.0.0.1',
                    help='host of this container. A process in the container '
                         'or in the client must be able to connect this host '
                         'to reach MongoDB servers. Default: 127.0.0.1')
parser.add_argument('--databases', type=str, nargs='*')
args = parser.parse_args()


def makeReplSetConfig(host, basePort, count, name, configsvr):
    member_doc = '{{ _id : {}, host : "{}:{}" }}'
    members = ','.join(member_doc.format(i, host, basePort + i)
                       for i in range(count))
    doc = 'rs.initiate({{_id: "{}", configsvr: {}, members: [{}] }});'
    return doc.format(name, 'true' if configsvr else 'false', members)


def makeAddShardConfig(host, basePort, name):
    doc = 'sh.addShard("{}/{}:{}");'.format(name, host, basePort)
    return doc


def makeEnableShardingConfig(name):
    doc = 'sh.enableSharding("{}");'.format(name)
    return doc


def makeConfigDbAddress(host, basePort, count, name):
    ips = ','.join('{}:{}'.format(host, basePort + i) for i in range(count))
    return '{}/{}'.format(name, ips)


def main():
    sys.stdout.write("set -ex;")

    # config servers first
    configBasePort = 47000
    configReplSetName = args.configReplSetName
    for i in range(args.configSize):
        port = configBasePort + i
        basePath = '/mongo/config/{}'.format(i)
        sys.stdout.write('mkdir -p {}/db\n'.format(basePath))
        sys.stdout.write('mongod --port {} --logpath {}/log --dbpath {}/db --configsvr --bind_ip_all --replSet {} --fork\n'.format(
            port, basePath, basePath, configReplSetName))
    replSetConfig = makeReplSetConfig(
        args.host, configBasePort, args.configSize, configReplSetName, True)
    sys.stdout.write(
        "mongo --port {} --eval '{}'\n".format(configBasePort, replSetConfig))

    # now routers
    routerBasePort = 27017
    for i in range(args.routerSize):
        basePath = '/mongo/router/{}'.format(i)
        dbAddress = makeConfigDbAddress(
            args.host, configBasePort, args.configSize, configReplSetName)
        sys.stdout.write('mkdir -p {}\n'.format(basePath))
        sys.stdout.write('mongos --port {} --logpath {}/log --configdb {} --bind_ip_all --fork\n'.format(
            routerBasePort + i, basePath, dbAddress))

    # shards
    for i in range(args.shardSize):
        basePort = 37000 + 100 * i
        replSetName = 'mongoreplsetshard{}'.format(i)
        # init all mongod's in this replSet
        for j in range(args.replicaSize):
            port = basePort + j
            basePath = '/mongo/{}/{}'.format(i, j)
            sys.stdout.write('mkdir -p {}/db\n'.format(basePath))
            sys.stdout.write('mongod --port {} --logpath {}/log --dbpath {}/db --shardsvr --bind_ip_all --replSet {} --fork\n'.format(
                port, basePath, basePath, replSetName))
        # mongod's in this replSet has all up, call rs.initiate
        replSetConfig = makeReplSetConfig(
            args.host, basePort, args.replicaSize, replSetName, False)
        sys.stdout.write(
            "mongo --port {} --eval '{}'\n".format(basePort, replSetConfig))
        # add shard to config server
        addShardConfig = makeAddShardConfig(args.host, basePort, replSetName)
        sys.stdout.write(
            "mongo --port {} --eval '{}'\n".format(routerBasePort, addShardConfig))

    # additionally shard some databases
    if args.databases:
        for db in args.databases:
            enableShardingConfig = makeEnableShardingConfig(db)
            sys.stdout.write(
                "mongo --port {} --eval '{}'\n".format(routerBasePort, enableShardingConfig))


if __name__ == '__main__':
    main()
