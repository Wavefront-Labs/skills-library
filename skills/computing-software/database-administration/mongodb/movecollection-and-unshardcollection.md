---
id: computing-software.database-administration.mongodb.movecollection-and-unshardcollection
name: movecollection-and-unshardcollection
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, movecollection, unshardcollection, mongodb-sharding, primary-shard]
level: practitioner
status: docs-checked
description: "Move an unsharded MongoDB collection to another shard with moveCollection, or unshard a sharded collection (8.0+), including prerequisites, impact and monitoring."
sources:
  - https://www.mongodb.com/docs/manual/reference/command/moveCollection/
  - https://www.mongodb.com/docs/manual/reference/command/unshardCollection/
  - https://www.mongodb.com/docs/manual/core/sharded-cluster-shards/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# moveCollection (8.0+) and unshardCollection

**Goal:** rebalance unsharded collections off an overloaded primary shard, or undo sharding of a collection that never needed it.

## Move an unsharded collection
```javascript
db.adminCommand({ moveCollection: "app.audit", toShard: "shard03" })
```
- Run it through `mongos` against the `admin` database. It moves one unsharded collection at a time; there is a 5 minute minimum duration; `writeConcernMajorityJournalDefault` must be `true`.
- Your application must tolerate about two seconds during which the collection blocks writes.
- The destination shard needs at least (collection storage size + index size) x 2 bytes free; these resource requirements are not enforced, so running short can fill the disk or slow the operation.
- While it runs you cannot run `collMod`, `createIndexes`, `dropIndexes`, `drop`, `renameCollection` or `convertToCapped` on the collection, nor `addShard`, `removeShard`, `createCollection`, `dropDatabase` or the config server transition commands on the cluster; index builds during the move might silently fail.
- Before 8.0 unsharded collections were restricted to the database's primary shard; `movePrimary` reassigns the primary shard and migrates all unsharded collections of the database.

## Unshard
```javascript
db.adminCommand({ unshardCollection: "app.settings", toShard: "shard01" })
```
Moves all data to one shard (`toShard` is optional; without it the cluster picks the shard with the least data) and removes the shard key. Useful for small collections sharded by mistake that now pay broadcast costs. It has a 5 minute minimum duration and similar restrictions to `moveCollection`; if the collection has a zone configuration, remove its zone ranges and shard associations first. Unsharding is write-intensive and can increase oplog growth.

## Abort
```javascript
db.adminCommand({ abortMoveCollection: "app.audit" })
db.adminCommand({ abortUnshardCollection: "app.settings" })
```

## Prerequisites
- Sharded clusters only; `moveCollection` needs MongoDB 8.0 and moves only unsharded collections, `unshardCollection` operates only on sharded collections. Neither supports collections using Queryable Encryption. Search indexes must be rebuilt afterwards.
- Run during a low-traffic period if possible (the manual advises this because of the resource requirements).

## Verify
`sh.status()` shows the collection on the new shard; app latency stable after cutover.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: moveCollection (8.0) and unshardCollection command syntax with toShard (optional for unshard), abortMoveCollection and abortUnshardCollection, two-second write block, 5 minute minimum duration, destination space of (collection + index size) x 2, writeConcernMajorityJournalDefault true, operations blocked during the move, zone ranges removed before unsharding, QE unsupported, search indexes need rebuilding, movePrimary reassigns the primary shard. Removed the unconfirmed resharding-machinery description, $currentOp monitoring, FCV and balancer/time-series claims.

Method: documentation only; no commands were run.
