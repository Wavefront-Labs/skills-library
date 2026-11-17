---
id: computing-software.database-administration.mongodb.removing-a-shard
name: removing-a-shard
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, sharding, remove-shard, drain-shard, moveprimary, balancer]
level: advanced
status: docs-checked
description: "Drain and remove a shard from a MongoDB cluster: removeShard progress, moving primary databases and unsharded collections, jumbo chunks blocking the drain."
sources:
  - https://www.mongodb.com/docs/manual/tutorial/remove-shards-from-cluster/
  - https://www.mongodb.com/docs/manual/reference/command/removeShard/
  - https://www.mongodb.com/docs/manual/reference/command/movePrimary/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Removing (draining) a shard

## Pre-checks
```js
sh.getBalancerState()            // must be true: the balancer moves the chunks
db.adminCommand({ listShards: 1 })
```
Make sure remaining shards have disk and capacity for the drained data.

## Start draining
```js
db.adminCommand({ removeShard: "shard03" })
// { msg: "draining started successfully", state: "started", dbsToMove: ["reports"], ... }
```
Run the same command again to see progress:
```js
db.adminCommand({ removeShard: "shard03" })
// state: "ongoing", remaining: { chunks: 412, dbs: 1, jumboChunks: 0 }
```
Draining is done by the balancer, which migrates chunks slowly to avoid load on the cluster.

## Move primaries and unsharded collections
Databases whose **primary shard** is shard03 hold unsharded collections there. Move them:
```js
db.adminCommand({ movePrimary: "reports", to: "shard01" })      // moves all unsharded collections of the db
// 8.0+: move unsharded collections first (see the Remove Shards tutorial)
db.adminCommand({ moveCollection: "reports.daily", toShard: "shard01" })
```
Run movePrimary during planned downtime with reads and writes stopped, as the movePrimary page advises; from 8.0, unmoved unsharded collections are unavailable during movePrimary.

## Jumbo chunks block completion
`remaining.jumboChunks > 0`: wait until only the jumbo chunks remain on the shard, then follow the jumbo chunk steps on the removeShard page. Refining the shard key can address jumbo chunks caused by low cardinality.

## Finish
When `removeShard` reports the drain has completed, the shard is gone from `listShards`. Shut down
its replica set members and remove them from monitoring/backup.

## Gotchas
- The balancer must stay enabled: with it disabled, removeShard stays in the draining state.
- If a DDL operation such as reshardCollection is running, removeShard executes only after it finishes.

## Verify
`db.adminCommand({ listShards: 1 })` no longer lists the shard and applications see no errors.

## Checked

2026-10-28. Confirmed against MongoDB manual removeShard, movePrimary and Remove Shards from a Sharded Cluster pages: balancer must be enabled (sh.getBalancerState()), listShards, started/ongoing output with dbsToMove and jumboChunks, slow balancer-driven migration, movePrimary during planned downtime, sh.moveCollection from 8.0 and the adminCommand form with toShard, removeShard waits for concurrent DDL. Removed unconfirmed: clearJumboFlag and forceJumbo, flushRouterConfig, zone note, duration estimate, one-way drain note.

Method: documentation only; no commands were run.
