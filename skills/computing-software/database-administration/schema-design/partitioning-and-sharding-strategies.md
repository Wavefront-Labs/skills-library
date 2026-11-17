---
id: computing-software.database-administration.schema-design.partitioning-and-sharding-strategies
name: partitioning-and-sharding-strategies
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, partitioning, sharding, shard-key, hot-partition, range-partition, hash-partition, partition-pruning, cross-shard-query, rebalancing, tenant-isolation]
level: advanced
status: draft
description: "Choose a partition or shard key from actual write/query patterns, and avoid the hot-partition and cross-shard-join traps that show up only at scale."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Partitioning and sharding — choosing a key that doesn't blow up later

**Goal:** pick a partition/shard key that matches how the data is actually
written and queried, and recognize the specific ways a reasonable-looking key
choice still creates a hot partition or an unworkable cross-shard query pattern.

## 1. Partitioning (single instance) vs. sharding (multiple instances)
**Partitioning** splits a table into physically separate segments within one
database instance (range, list, or hash partitions) — the engine still sees one
logical table; its benefit is partition pruning (skip irrelevant partitions
entirely for a query) and easier bulk operations (drop a whole partition instead
of a slow `DELETE`). **Sharding** distributes data across multiple separate
database instances/nodes — solves the problem partitioning can't (a single
instance's storage/throughput ceiling), but adds cross-shard query complexity and
a routing layer. Many systems need partitioning for manageability long before they
need sharding for scale — don't reach for sharding's complexity to solve a
problem partitioning already solves.

## 2. Range partitioning: the classic time-series pattern, and its trap
Partition by date range (`created_at` monthly/daily) — queries filtered by date
range prune to only the relevant partitions, and old data drops cheaply (`DROP
PARTITION` instead of a billion-row `DELETE`). The trap: if writes are
overwhelmingly to the *current* partition (the normal case for time-series
inserts), that one partition absorbs all the write load regardless of how many
partitions exist — partitioning here solves query pruning and retention, **not**
write throughput distribution. Don't expect range partitioning by itself to fix a
single-node write bottleneck.

## 3. Hash/key sharding: solves write distribution, breaks range queries
Hashing a key (customer ID, UUID) across shards distributes write load evenly —
but a query needing a range or ordered scan (e.g. "all orders in the last hour
across all customers") now has to fan out to every shard and merge results,
instead of hitting one. This is the fundamental tension: the property that makes
writes evenly distributed (hash randomizes locality) is the same property that
destroys range-query locality. Composite keys (hash the tenant/customer, keep a
natural range column secondary within that) are the usual compromise — see the
monotonic-key discussion in the MongoDB sharding skill for the same trade-off in
a specific engine.

## 4. The cardinality and monotonicity failures, generalized across engines
- **Low-cardinality key** (e.g. `region` with 4 values): caps parallelism/shard
  count at the key's cardinality — no rebalancing fixes a key that fundamentally
  can't subdivide further.
- **Monotonically increasing key** (auto-increment ID, timestamp) as a *range*
  partition/shard boundary concentrates all new writes on the newest
  partition/shard — fine for retention-by-drop use cases, bad for write
  throughput distribution; don't use the same key for both goals without
  reconciling the conflict (e.g. hash-shard first, range-partition within each
  shard for retention).
- **Tenant-size skew**: sharding by tenant ID works until one tenant is 1000x
  larger than the rest and its shard becomes hot regardless of hash quality — plan
  for an explicit "split this one tenant further" or dedicated-shard escape hatch
  before it's an emergency.

## 5. Cross-partition/cross-shard operations are the ongoing tax
Joins, transactions, and uniqueness constraints that span partitions/shards are
either unsupported, expensive (scatter-gather), or require application-level
coordination (two-phase commit, sagas) depending on the engine. Before choosing a
key, inventory the queries and constraints that **must** be transactional or
joined, and verify they stay within a single partition/shard under the proposed
key — discovering a cross-shard uniqueness requirement after sharding is live is
expensive to retrofit.

## 6. Rebalancing is not free
Growing past the current shard count requires moving data (resharding) — plan for
this from day one (consistent hashing, virtual shards/buckets that can be
reassigned without moving every key, or an engine with built-in resharding) rather
than a fixed modulo-N scheme that requires touching nearly every row's shard
assignment to add one node.

## Verify
- [ ] Partitioning vs. sharding was chosen based on an actual throughput/storage ceiling, not reached for pre-emptively.
- [ ] The chosen key was checked against real write patterns for hot-partition risk (monotonicity, tenant skew).
- [ ] Queries/constraints requiring joins, transactions, or uniqueness across rows were inventoried and confirmed to stay within one partition/shard.
- [ ] A rebalancing/resharding path exists that doesn't require touching every row to add capacity.
- [ ] Range-query needs and write-distribution needs on the same dataset were reconciled with a composite key, not left in conflict.
