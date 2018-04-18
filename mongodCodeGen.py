#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser(description='mongodb bootstrap code generator')
parser.add_argument('shardSize', type=int)
parser.add_argument('replicaSize', type=int)
parser.add_argument('configSize', type=int)
parser.add_argument('routerSize', type=int)
parser.add_argument('-dbs', '--databases', type=str, nargs='*')
args = parser.parse_args()

def makeReplSetConfig(basePort, count, name, configsvr):
	member_doc = '{{ _id : {}, host : "127.0.0.1:{}" }}'
	members = ','.join(member_doc.format(i, basePort + i) for i in range(count))
	doc = 'rs.initiate({{_id: "{}", configsvr: {}, members: [{}] }});'
	return doc.format(name, 'true' if configsvr else 'false', members)


def makeAddShardConfig(basePort, name):
	doc = 'sh.addShard("{}/127.0.0.1:{}");'.format(name, basePort)
	return doc

def makeEnableShardingConfig(name):
	doc = 'sh.enableSharding("{}");'.format(name)
	return doc


def makeConfigDbAddress(basePort, count, name):
	ips = ','.join('127.0.0.1:{}'.format(basePort + i) for i in range(count))
	return '{}/{}'.format(name, ips)


def main():
	sys.stdout.write("set -e;")

	# config servers first
	configBasePort = 47000
	configReplSetName = 'mongoreplsetconfig'
	for i in range(args.configSize):
		port = configBasePort + i
		basePath = '/mongo/config/{}'.format(i)
		sys.stdout.write('mkdir -p {}/db\n'.format(basePath))
		sys.stdout.write('mongod --port {} --logpath {}/log --dbpath {}/db --configsvr --replSet {} --fork\n'.format(port, basePath, basePath, configReplSetName))
	replSetConfig = makeReplSetConfig(configBasePort, args.configSize, configReplSetName, True)
	sys.stdout.write("mongo --port {} --eval '{}'\n".format(configBasePort, replSetConfig))
	
	# now routers
	routerBasePort = 27017
	for i in range(args.routerSize):
		basePath = '/mongo/router/{}'.format(i)
		dbAddress = makeConfigDbAddress(configBasePort, args.configSize, configReplSetName)
		sys.stdout.write('mkdir -p {}\n'.format(basePath))
		sys.stdout.write('mongos --port {} --logpath {}/log --configdb {} --bind_ip_all --fork\n'.format(routerBasePort + i, basePath, dbAddress))
	
	# shards
	for i in range(args.shardSize):
		basePort = 37000 + 100 * i
		replSetName = 'mongoreplsetshard{}'.format(i)
		# init all mongod's in this replSet
		for j in range(args.replicaSize):
			port = basePort + j
			basePath = '/mongo/{}/{}'.format(i,j)
			sys.stdout.write('mkdir -p {}/db\n'.format(basePath))	
			sys.stdout.write('mongod --port {} --logpath {}/log --dbpath {}/db --shardsvr --replSet {} --fork\n'.format(port, basePath, basePath, replSetName))
		# mongod's in this replSet has all up, call rs.initiate
		replSetConfig = makeReplSetConfig(basePort, args.replicaSize, replSetName, False)
		sys.stdout.write("mongo --port {} --eval '{}'\n".format(basePort, replSetConfig))
		# add shard to config server
		addShardConfig = makeAddShardConfig(basePort, replSetName)
		sys.stdout.write("mongo --port {} --eval '{}'\n".format(routerBasePort, addShardConfig))

	# additionally shard some databases
	if args.databases:
		for db in args.databases:
			enableShardingConfig = makeEnableShardingConfig(db)
			sys.stdout.write("mongo --port {} --eval '{}'\n".format(routerBasePort, enableShardingConfig))

if __name__ == '__main__':
	main()