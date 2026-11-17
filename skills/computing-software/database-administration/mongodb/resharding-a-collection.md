---
id: computing-software.database-administration.mongodb.resharding-a-collection
name: resharding-a-collection
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, sharding, reshardcollection, shard-key, refine-collection-shard-key, resharding-progress, commit-reshard-collection, mongos]
level: practitioner
status: docs-checked
description: "Change a MongoDB collection's shard key online with reshardCollection: prerequisites, monitoring, abort/commit, and refineCollectionShardKey as the lighter option."
sources:
  - https://www.mongodb.com/docs/manual/core/sharding-reshard-a-collection/
  - https://www.mongodb.com/docs/manual/reference/command/reshardCollection/
  - https://www.mongodb.com/docs/manual/reference/command/refineCollectionShardKey/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resharding a collection

**Goal:** fix a bad shard key (hot shard, jumbo chunks, scatter-gather queries) without dumping and reloading. `reshardCollection` is available from MongoDB 5.0.

## Lighter option first: refine
If the existing key is right but too coarse (jumbo chunks from low cardinality), append suffix fields. The new key must start with the existing key and be supported by an index that already exists (not partial or sparse; simple collation if the collection has a non-simple default collation):
```javascript
db.orders.createIndex({ customerId: 1, orderId: 1 })
db.adminCommand({ refineCollectionShardKey: "app.orders", key: { customerId: 1, orderId: 1 } })
```
It updates chunk and zone ranges without immediately redistributing data; later splits and migrations happen through normal sharding operations. Requires feature compatibility version 4.4. Never change the range/hashed type of existing key fields (data inconsistency).

## Full reshard
Prerequisites (not enforced by the database; failing them can fill the disk and shut the database down):
- Free storage on each recipient shard of at least `((collection_storage_size + index_size) * 2) / shard_count`.
- I/O capacity below 50% and CPU load below 80%.
- No index builds in progress, and the application tolerates a period of two seconds where the collection blocks writes (otherwise refine instead).
- Balancer disabled for the duration; re-enable it afterwards. Only one collection can be resharded at a time.
- `writeConcernMajorityJournalDefault` is `true`; consider a larger or fixed oplog because resharding is write-intensive.
- You do not need to create the new key's index first: the index phase builds it.
```javascript
db.adminCommand({ reshardCollection: "app.orders", key: { region: 1, orderId: 1 } })   // or sh.reshardCollection()
// same key, redistribute (8.0+): add forceRedistribution: true (optionally with zones)
```
Optional fields include `numInitialChunks` (default 90) and `zones`. A collection with a default collation needs `collation: { locale: "simple" }`.

Phases: initialization, clone (recipients copy data), index, apply and catch-up, commit. Writes are blocked briefly near the end. The minimum duration is always 5 minutes (`demoMode: true` bypasses it for testing). While resharding, `collMod`, `createIndexes`, `dropIndexes`, `drop`, `renameCollection` and `convertToCapped` are not supported on the collection, and `addShard`, `removeShard` and `dropDatabase` wait. Resharding fails if `_id` values are not globally unique.

## Monitor
```javascript
db.getSiblingDB("admin").aggregate([ { $currentOp: { allUsers: true, localOps: false } },
  { $match: { type: "op", "originatingCommand.reshardCollection": "app.orders" } } ])
// totalOperationTimeElapsedSecs, remainingOperationTimeEstimatedSecs (-1 at start; a pessimistic estimate)
```
Re-run the pipeline to see updated values.

## Control
```javascript
db.adminCommand({ commitReshardCollection: "app.orders" })   // block writes early and finish
db.adminCommand({ abortReshardCollection: "app.orders" })    // not possible once the commit phase is reached
```
Use commit when the remaining-time estimate is an acceptable write-block duration.

## Gotchas
- Queries that use the old key instead of the new one use the two-phase write protocol (broadcast to several shards); update application filters to include the full new shard key after the reshard.
- Retryable writes started before or during resharding can be retried for up to 5 minutes afterwards.
- A search index on the collection becomes unavailable after the operation and must be rebuilt. Queryable-encryption collections are not supported.
- Only one of `moveCollection`, `reshardCollection`, `rewriteCollection` and `unshardCollection` can run on the cluster at a time.

## Verify
`sh.status()` shows the new shard key.

## Checked
2026-10-31. Against the MongoDB manual pages Reshard a Collection, reshardCollection and refineCollectionShardKey: refine prerequisites and behaviour, storage formula, I/O and CPU thresholds, two-second write block, balancer step, `$currentOp` pipeline and fields, 5-minute minimum, `numInitialChunks` default 90, `forceRedistribution`, `commitReshardCollection` / `abortReshardCollection` behaviour, unsupported operations, two-phase write protocol and retryable-write window. The 5.0 availability of `reshardCollection` is stated on the Choose a Shard Key page. Removed unconfirmed details: the 1.2x disk figure, `reshardingCriticalSectionTimeoutMillis` and its 5 s default, 7.2/8.0 speed claims, change-stream and `$lookup` remarks, `getShardDistribution()`/`explain()` verification, and specific `$currentOp` copy-progress field names.
Method: documentation only; no commands were run.
