---
id: computing-software.database-administration.mongodb.targeted-vs-scatter-gather-queries
name: targeted-vs-scatter-gather-queries
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, scatter-gather, targeted-queries, mongodb-sharding, shard-key, mongos]
level: practitioner
status: docs-checked
description: "Tell whether MongoDB sharded queries are targeted or scatter-gather, why it matters for latency and scale, and how to rewrite queries or keys so mongos targets one shard."
sources:
  - https://www.mongodb.com/docs/manual/core/sharded-cluster-query-router/
  - https://www.mongodb.com/docs/manual/core/sharding-shard-key/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Targeted vs scatter-gather queries

**Goal:** most queries should hit one shard. Broadcast queries cost every shard's resources and run at the speed of the slowest shard.

## How mongos routes
- Query includes the shard key → can be **targeted** to the shards that own that data (it may still broadcast depending on data distribution and selectivity).
- No shard key → mongos performs a **broadcast** to all shards in the cluster, then merges the results (sorting is done on each shard first).

## Check
```javascript
db.orders.find({ customerId: 42, status: "open" }).explain()
```
Read the explain output for which shards were contacted; see Targeted Operations vs. Broadcast Operations in the query router page.

## Fixes
1. Include the shard key in the filter where the app already knows it (pass `tenantId` everywhere).
2. Choose the shard key from the dominant query predicate, not just write distribution (`{ tenantId: 1, _id: 1 }` for multi-tenant).
3. For secondary lookups (by email), keep a small lookup collection sharded by email that returns the shard key, then do a targeted read.
4. `refineCollectionShardKey` (adds suffix fields to the existing key) when the key has too little cardinality.

## Acceptable broadcasts
Rare admin/report queries and aggregations designed to run on all shards.

## Gotchas

## Verify
Profile a day of traffic: share of queries that broadcast vs target; aim to push hot paths to targeted queries.

## Checked

2026-10-28. Confirmed against MongoDB manual pages (query router, shard key, refineCollectionShardKey): queries without the shard key are broadcast to all shards, queries with it may still broadcast, merging and per-shard sorting, refineCollectionShardKey adds suffix fields. Removed unconfirmed: SINGLE_SHARD / SHARD_MERGE stage names, nShards log field and 4.4+ tag, hashed-range rule, reshardCollection, 7.1+ updateOne note, upsert rule, per-shard limit behaviour.

Method: documentation only; no commands were run.
