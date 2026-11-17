---
id: computing-software.database-administration.mongodb.hashed-indexes
name: hashed-indexes
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, hashed-index, mongodb-indexes, hashed-sharding, equality-index]
level: practitioner
status: verified
description: "Use MongoDB hashed indexes for equality lookups and hashed shard keys, knowing their limits (no ranges, no multikey, no unique) and compound hashed indexes."
sources:
  - https://www.mongodb.com/docs/manual/core/indexes/index-types/index-hashed/
  - https://www.mongodb.com/docs/manual/core/hashed-sharding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hashed indexes

**Goal:** an index storing a 64-bit hash of a field, used mainly to support hashed sharding and even data distribution of monotonically increasing keys.

## Create
```javascript
db.events.createIndex({ deviceId: "hashed" })
db.events.createIndex({ tenantId: 1, deviceId: "hashed" })   // compound hashed, one hashed field max
```

## What it supports
- Equality: `find({deviceId: "abc"})` uses it.
- **Not** range queries (`$gt`, `$lt`), sorts by the field, or prefix regex: hashing destroys order.
- **Not** multikey: the hashed field cannot hold arrays (insert fails with "hashed indexes do not currently support array values").
- **Not** `unique: true` ("hashed indexes cannot guarantee uniqueness"). For uniqueness keep a separate non-hashed unique index on the same field.
- Floating points are truncated to 64-bit integers before hashing: `2.3` and `2.2` hash the same. Avoid hashed indexes on floats.

## When to use
- Required for a hashed shard key (`sh.shardCollection("db.c", {deviceId: "hashed"})`); MongoDB creates it automatically for an empty collection.
- Not a general speed-up: a normal ascending index already does equality equally well and supports ranges too. Do not add hashed indexes just for lookups.

## Hash collisions
Different values can share a hash; the server re-checks the actual document value, so results stay correct but `docsExamined` can slightly exceed `nReturned`.

## Verify
`explain()` shows `IXSCAN` with `keyPattern: {deviceId: "hashed"}` for equality; a range query on the same field shows `COLLSCAN` or another index, which proves the limitation in your workload.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. Single and compound (`tenantId: 1, deviceId: "hashed"`) hashed indexes built; two hashed fields, `unique: true` and an array value were each rejected with the quoted messages. `convertShardKeyToHashed` gave the same hash for 2.3 and 2.2 and a different one for 3.
- Equality query: `IXSCAN` with `keyPattern: {deviceId: "hashed"}`; `$gt` range and a sort on the field gave `COLLSCAN` (and `SORT`) even with the hashed index present.
- Docs fetched: hashed index page (floating-point truncation, 2.3/2.2/2.9 share a hash). The "4.4+" gate was not confirmed and was removed.
