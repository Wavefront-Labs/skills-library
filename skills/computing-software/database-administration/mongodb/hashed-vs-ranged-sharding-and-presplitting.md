---
id: computing-software.database-administration.mongodb.hashed-vs-ranged-sharding-and-presplitting
name: hashed-vs-ranged-sharding-and-presplitting
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, hashed-sharding, ranged-sharding, presplit, mongodb-sharding, shard-key]
level: practitioner
status: docs-checked
description: "Choose between hashed and ranged MongoDB shard keys for write distribution versus range-query targeting, and pre-split chunks before bulk loading."
sources:
  - https://www.mongodb.com/docs/manual/core/hashed-sharding/
  - https://www.mongodb.com/docs/manual/core/ranged-sharding/
  - https://www.mongodb.com/docs/manual/reference/method/sh.shardCollection/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hashed vs ranged sharding and pre-splitting

## Trade-off
| | Hashed | Ranged |
|---|---|---|
| Monotonic keys (ObjectId, timestamps) | Spreads inserts across shards | All inserts hit the max-chunk shard (hot shard) |
| Range queries on key | Broadcast | Targeted |
| Equality queries | Targeted | Targeted |
| Zones | Only with compound hashed (prefix ranged) | Natural |

Rule: ranged on a high-cardinality, non-monotonic key that matches queries (`{ tenantId: 1, createdAt: 1 }`); hashed when the natural key is monotonic and lookups are by equality.

## Hashed on an empty collection
```javascript
sh.shardCollection("logs.events", { deviceId: "hashed" })
```
With no zones, sharding an empty or non-existent collection on a single-field hashed key creates one empty chunk covering the whole key range; starting in 8.0 it creates one chunk per shard by default and migrates them across shards, which speeds up setup. After the initial distribution the balancer manages chunks.

## Compound hashed
```javascript
sh.shardCollection("logs.events", { region: 1, deviceId: "hashed" })
```
Compound hashed shard keys support zone sharding on the non-hashed prefix fields while the hashed field spreads data more evenly.

## Pre-splitting ranged keys before a bulk load
Only for an empty collection (pre-splitting a populated one can produce unpredictable range sizes and ineffective balancing). Since 6.0 the balancer does not distribute empty ranges, so use `moveRange`, which splits and moves in one step:
```javascript
db.adminCommand({ shardCollection: "crm.contacts", key: { lastName: 1 } })
db.adminCommand({ moveRange: "crm.contacts", min: { lastName: "k" }, max: { lastName: "p" }, toShard: "shard02" })
```
Alternatively define zones and zone ranges before sharding the empty collection so the initial ranges follow them. Without pre-splitting, a fresh collection starts as one range on one shard.

## Gotchas
- Shard key choice is hard to change (reshard copies data); test with real query logs.
- You cannot specify a unique constraint on a hashed index; hashed indexes truncate floating-point numbers to 64-bit integers before hashing.
- Low-cardinality keys produce jumbo chunks whatever the strategy.

## Verify
During a load test `db.events.getShardDistribution()` and `mongostat --discover` show inserts on all shards.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: hashed vs ranged trade-offs (monotonic keys, broadcast range queries), compound hashed keys with zone sharding on the prefix, empty-collection initial chunk behaviour (one chunk per shard by default from 8.0), hashed indexes cannot be unique and truncate floating-point values, pre-splitting only for empty collections and, since 6.0, distributing empty ranges with moveRange. Replaced the numInitialChunks, splitAt and moveChunk pre-split example with the documented moveRange procedure.

Method: documentation only; no commands were run.
