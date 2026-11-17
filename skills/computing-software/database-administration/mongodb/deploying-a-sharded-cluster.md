---
id: computing-software.database-administration.mongodb.deploying-a-sharded-cluster
name: deploying-a-sharded-cluster
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, sharding, mongos, sh-addshard, config-server, shardcollection]
level: advanced
status: docs-checked
description: "Stand up a MongoDB sharded cluster: config server replica set, shard replica sets, mongos routers, sh.addShard, enabling sharding on a collection, and checks."
sources:
  - https://www.mongodb.com/docs/manual/tutorial/deploy-shard-cluster/
  - https://www.mongodb.com/docs/manual/core/sharded-cluster-components/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying a sharded cluster

## Components
- **Config server replica set** (CSRS): stores cluster metadata (3 members in production). From 8.0 a config server can also store application data ("config shard").
- **Shards**: each a replica set (3 data members).
- **mongos**: stateless routers; run several, close to the applications (often on app hosts or
  behind a load balancer).
All members share the same keyFile (or x.509 member certs) for internal auth.

## 1. Config servers
```yaml
# mongod.conf on cfg1..cfg3
sharding: { clusterRole: configsvr }
replication: { replSetName: cfgRS }
net: { port: 27019, bindIp: 0.0.0.0 }   # 27019 is the default config server port
security: { keyFile: /etc/mongod/keyfile }
```
```js
rs.initiate({ _id: "cfgRS", configsvr: true,
  members: [{ _id: 0, host: "cfg1:27019" }, { _id: 1, host: "cfg2:27019" }, { _id: 2, host: "cfg3:27019" }] })
```

## 2. Shard replica sets
```yaml
sharding: { clusterRole: shardsvr }
replication: { replSetName: shard01 }
net: { port: 27018 }   # default shard member port
```
`rs.initiate(...)` each shard as a normal replica set.

## 3. mongos
```yaml
# mongos.conf
sharding: { configDB: cfgRS/cfg1:27019,cfg2:27019,cfg3:27019 }
net: { port: 27017, bindIp: 0.0.0.0 }
security: { keyFile: /etc/mongod/keyfile }
```
Start `mongos --config /etc/mongos.conf`. Create the admin user through mongos (sharded cluster users); create shard-local admin users on each shard too for maintenance (they exist only on that shard and cannot connect to mongos).

## 4. Add shards and shard collections
```js
sh.addShard("shard01/sh01a:27018,sh01b:27018,sh01c:27018")
sh.addShard("shard02/sh02a:27018,sh02b:27018,sh02c:27018")
sh.enableSharding("app")                                  // optional in 6.0+
db.orders.createIndex({ customerId: 1, orderId: 1 })      // index supporting the shard key
sh.shardCollection("app.orders", { customerId: 1, orderId: 1 })
// or hashed: sh.shardCollection("app.events", { deviceId: "hashed" })
sh.status()
```
Before 8.0, unsharded collections live on the database's **primary shard**; since 8.0 `moveCollection` (`sh.moveCollection("db.coll", "shardName")`) can place an unsharded collection on any shard.

## Checks
```js
sh.status()                          // shards, balancer state, chunk distribution
db.adminCommand({ listShards: 1 })
sh.getBalancerState(); sh.isBalancerRunning()
db.orders.getShardDistribution()
```
Applications connect only to mongos addresses, never directly to shards.

## Gotchas
- Choose the shard key carefully up front (you can reshard since 5.0 or refine a key by adding a suffix field).
- Time sync (NTP) and DNS must be solid across all components.
- Backups need a consistent approach across shards (Ops Manager/Atlas, or coordinated snapshots).

## Verify
`sh.status()` lists all shards, the collection is sharded with chunks on each shard after
the balancer runs, and an app write via mongos is routed (explain shows `SINGLE_SHARD` for
queries with the shard key).

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: default ports 27018 (shard) and 27019 (config), sharding.configDB form and mongos --configdb, sh.addShard replica set form, sh.enableSharding not required since 6.0, config shard from 8.0, moveCollection / sh.moveCollection in 8.0 (before 8.0 unsharded collections stay on the primary shard), resharding since 5.0, refineCollectionShardKey, shard-local users exist only on their shard and cannot connect to mongos. Removed the numInitialChunks shardCollection option (not documented for shardCollection) and unconfirmed claims.

Method: documentation only; no commands were run.
