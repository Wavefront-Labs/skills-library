---
id: computing-software.database-administration.mongodb.jumbo-chunks
name: jumbo-chunks
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, sharding, jumbo-chunk, shard-key-cardinality, refine-collection-shard-key, cleardjumboflag, split-chunk, low-cardinality]
level: practitioner
status: docs-checked
description: "Find and fix MongoDB jumbo chunks that the balancer cannot move: split them, clear the jumbo flag, or refine the shard key when cardinality is too low."
sources:
  - https://www.mongodb.com/docs/manual/core/sharding-data-partitioning/#jumbo-chunks
  - https://www.mongodb.com/docs/manual/tutorial/clear-jumbo-flag/
  - https://www.mongodb.com/docs/manual/reference/command/refineCollectionShardKey/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jumbo chunks

**Goal:** remove the chunks that pin data to one shard and block balancing.

## What makes a chunk jumbo
A chunk that exceeds the configured range size and is labelled `jumbo`. It may be indivisible, for example a chunk with a range of a single shard key value. The balancer does not migrate ranges labelled jumbo (its `attemptToBalanceJumboChunks` setting lets it migrate large ranges that are not yet labelled jumbo), so one shard can keep growing.

## Find them
```javascript
sh.status(true)                       // "jumbo" marks
// size of a chunk:
db.getSiblingDB("app").runCommand({ dataSize: "app.orders", keyPattern: { customerId: 1 }, min: { customerId: 4711 }, max: { customerId: 4712 } })
```

## Fix: chunk is splittable (many key values)
```javascript
sh.splitFind("app.orders", { customerId: 4711 })                  // splits the chunk holding the first matching document into two equal halves
sh.splitAt("app.orders", { customerId: 4800 })                    // split at a point
db.adminCommand({ clearJumboFlag: "app.orders", bounds: [ { customerId: 4711 }, { customerId: 5000 } ] })
```
A successful split of a divisible chunk removes the flag, so splitting is the preferred method; use `clearJumboFlag` only when it does not apply (if the chunk still exceeds the range size, MongoDB re-labels it jumbo when it tries to move it). For hashed shard keys use `bounds`, not `find`. Then the balancer can move the pieces, or move a range manually with `moveRange` (6.0+); `forceJumbo: true` on `moveRange` / `moveChunk` migrates a range even if larger than the chunk size and may block writes to the collection.

## Fix: unsplittable (single hot key value)
The shard key has too low cardinality. Refine it by adding a suffix field (`refineCollectionShardKey` needs FCV 4.4 or later and an index starting with the new key):
```javascript
db.orders.createIndex({ customerId: 1, _id: 1 })
db.adminCommand({ refineCollectionShardKey: "app.orders", key: { customerId: 1, _id: 1 } })
db.adminCommand({ clearJumboFlag: "app.orders", find: { customerId: 4711 } })
```
Now the chunk can split by `_id` within the customer. Or reshard (5.0+).

## Prevention
Shard keys with high cardinality and even frequency; compound keys like `{ tenantId: 1, _id: 1 }`; monitor `getShardDistribution()` skew.

## Verify
`sh.status(true)` shows no chunk labelled `jumbo` and data per shard converges over the next balancer windows.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: jumbo label semantics, sh.status(true) to find jumbo chunks, splitting as the preferred way to clear the flag, sh.splitFind / sh.splitAt, clearJumboFlag with bounds or find (bounds for hashed keys; flag returns if the chunk is still too big), refineCollectionShardKey (FCV 4.4, supporting index), attemptToBalanceJumboChunks (large ranges not yet labelled jumbo), moveRange (6.0) with forceJumbo, dataSize keyPattern/min/max, resharding since 5.0. Removed the unconfirmed config.chunks jumbo query.

Method: documentation only; no commands were run.
