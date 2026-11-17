---
id: computing-software.database-administration.mongodb.replica-sets-elections-and-sharding
name: replica-sets-elections-and-sharding
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, replica-set, election, write-concern, read-concern, rollback, sharding, mongos, chunk-balancer, config-server, shard-key, zone-sharding]
level: advanced
status: docs-checked
description: "Reason about MongoDB replica-set elections and write concern for durability, and design a shard key that doesn't create a hot chunk."
sources:
  - https://www.mongodb.com/docs/manual/core/replica-set-elections/
  - https://www.mongodb.com/docs/manual/core/sharding-shard-key/
  - https://www.mongodb.com/docs/manual/core/sharding-choose-a-shard-key/
  - https://www.mongodb.com/docs/manual/core/hashed-sharding/
  - https://www.mongodb.com/docs/manual/core/sharding-balancer-administration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MongoDB replica sets and sharding — elections, write concern, and shard-key design

**Goal:** know what actually happens during a primary step-down, pick a write
concern that matches the durability you promised, and avoid the shard-key choice
that creates a permanently hot shard.

## 1. Elections: not instant, and can roll back writes
Elections are triggered by events such as adding a node, initiating the set, `rs.stepDown()` or
`rs.reconfig()`, or secondaries losing contact with the primary for longer than the configured
timeout (10 seconds by default; `settings.electionTimeoutMillis`). Members exchange heartbeats
every two seconds. The set cannot process writes until the election completes. The manual puts the
median time to elect a new primary at no more than about 12 seconds with default settings, and network
latency can extend it. Compatible drivers enable retryable writes by default and retry certain
write operations a single time, so build tolerance for failover into the application as well.

Priority affects timing and outcome: higher-priority secondaries call elections sooner and are more
likely to win; priority 0 members never seek election. A primary that can see only a minority of
voting members steps down. Only voting members (`votes: 1`) vote; a replica set can have up to 50
members but only 7 voting. Do not use `votes` to steer who becomes primary; use `priority`.

**Rollback**: if the old primary had accepted writes not yet replicated to the
majority before it stepped down/crashed, those writes are rolled back when the old
primary rejoins as a secondary (written to rollback files, not silently discarded;
recoverable manually, but the application already got acks for writes that no
longer exist in the data unless write concern prevented this).

## 2. Write concern is the actual durability control, not replication topology
- `{w: 1}`: acked once the primary applies it. Data can be rolled back if the primary steps down
  before any secondary has it. Fast, least durable.
- `{w: "majority"}`: acked once a majority of the replica set has it; this prevents rollback of
  acknowledged data (run all voting members with journaling). Since 5.0 it is the implicit default write
  concern for most deployments (a PSA set with an arbiter falls back to `{w: 1}`); check the actual default
  on your deployment rather than assuming.
- `{w: "majority", j: true}`: majority and journaled on the members. `writeConcernMajorityJournalDefault`
  (default true) already makes plain `majority` wait for the journal.
Clients reading at `local` or `available` read concern can see data that is later rolled back, so use
`"majority"` read concern where that matters.

## 3. Shard key: the decision that's expensive to reverse
Consider cardinality, frequency and monotonic change, plus your query patterns:
- **Monotonically increasing key** (ObjectId, timestamp, auto-increment) routes all new inserts to the
  chunk whose upper bound is `MaxKey` (decreasing keys go to the `MinKey` chunk), so the shard holding
  it becomes the write bottleneck. MongoDB places the split-off max chunk on a different shard, but
  the pattern remains. Hashed sharding (`{_id: "hashed"}`) distributes such inserts, at the cost of
  more broadcast (scatter-gather) operations for ranged queries; equality matches can still be
  targeted to one shard.
- **Low-cardinality key** (for example a continent field with 7 values) caps the number of chunks at
  the number of distinct values, so adding more shards than that gives no benefit. Use a compound key
  to raise cardinality.
- **High-frequency values** make the chunks holding them a bottleneck and eventually indivisible.
- **Compound shard key** (for example `{customerId: 1, createdAt: 1}`) is a common way to raise
  cardinality and keep related documents together for range queries.
- Queries without the shard key are broadcast to all shards (scatter-gather) and do not scale linearly.
- Since 5.0 you can change a shard key with `reshardCollection`, and `refineCollectionShardKey` adds
  suffix fields, but resharding is a major operation: treat the initial choice as close to permanent.
  From 7.0, `analyzeShardKey` (with query sampling enabled via `configureQueryAnalyzer`) calculates
  metrics to evaluate a candidate key.

## 4. Balancer and chunk migration
The balancer runs by default and migrates ranges when the data-size difference between the shard with
the most and least data for a collection reaches the migration threshold (three times the range size;
with the default 128 MB that is 384 MB). A shard takes part in at most one migration at a time, so a
cluster of n shards runs at most n/2 (rounded down) simultaneous migrations. Migrations cost bandwidth
and workload; you can limit the balancing window so the balancer does not compete with production
traffic.

## Verify
- [ ] Write concern for any data that matters uses at least `{w: "majority"}`, confirmed per deployment default rather than assumed.
- [ ] A primary step-down was tested and the application's retry/backoff behavior observed, not assumed.
- [ ] The shard key was checked for cardinality, frequency and monotonicity against the real write pattern before going live.
- [ ] `sh.status()` shows chunks reasonably balanced, with no shard permanently hot.
- [ ] Read concern is set deliberately where read-your-write consistency across a rollback matters.

## Checked
2026-10-31. Against the MongoDB manual pages Replica Set Elections, Rollbacks During Replica Set Failover, Write Concern, Shard Keys, Choose a Shard Key, Hashed Sharding and Balancer Administration: 10 second timeout, two second heartbeats, 12 second median, retryable-write default, priority and voting rules (50 members / 7 voting), write concern semantics and the 5.0 default with its arbiter exception, monotonic/low-cardinality/frequency shard-key effects, 5.0 `reshardCollection`, 7.0 `analyzeShardKey`, migration threshold (3x range size, 128 MB default), one migration per shard and n/2 limit. Removed unconfirmed details: "100% of insert load", `balancerStatus`, `sh.startBalancer`/`stopBalancer` window advice, "migrations can fail to converge", "default for most drivers", and the 4.4+ `reshardCollection` gate (corrected to 5.0).
Method: documentation only; no commands were run.
