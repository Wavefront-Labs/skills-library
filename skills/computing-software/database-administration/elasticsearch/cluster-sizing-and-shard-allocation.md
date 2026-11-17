---
id: computing-software.database-administration.elasticsearch.cluster-sizing-and-shard-allocation
name: cluster-sizing-and-shard-allocation
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, opensearch, shard-allocation, oversharding, cluster-health, red-cluster, yellow-cluster, disk-watermark, cat-shards, allocation-explain, heap-size, allocation-awareness, allocation-filtering]
level: advanced
status: docs-checked
description: "Size shards to avoid oversharding, read cluster health signals, and use allocation explain, watermarks and awareness settings to unblock unassigned shards."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/production-guidance/optimize-performance/size-shards.md
  - https://github.com/elastic/docs-content/blob/main/troubleshoot/elasticsearch/red-yellow-cluster-status.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/jvm-settings.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/circuit-breaker-settings.md
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Elasticsearch cluster sizing and shard allocation

**Goal:** avoid the oversharding trap that degrades every cluster operation, and go from a yellow or red cluster straight to the blocked shard and the reason, instead of restarting nodes.

## 1. Oversharding
Every shard has overhead in cluster management and search cost. Searching a thousand 50MB shards is substantially more expensive than one 50GB shard with the same data. Elastic's guidance:
- Aim for shards between 10GB and 50GB, with fewer than 200 million documents per shard.
- With ILM, set the rollover action's `max_primary_shard_size` to `50gb` and `min_primary_shard_size` to `10gb`.
- Master-eligible nodes should have at least 1GB of heap per 3000 indices (fewer than 3000 indices per GB of heap).
- Cluster shard limits prevent creating more than 1000 non-frozen shards per node and 3000 frozen shards per dedicated frozen node.
```
GET _cat/shards?v=true&h=index,shard,prirep,state,store
GET _cluster/health?pretty
GET _cat/nodes?v=true&h=heap.max
```
Shards are immutable, so fixing shard sizing means copying the data: reindex into an index with corrected settings, or, for an index you no longer write to, use the shrink index API (ILM also has a shrink action in the warm phase). You can also reindex many small time-based indices into one larger index.

## 2. Reading cluster health
- Red: some primary shards are unassigned, so searches and indexing may fail.
- Yellow: no unassigned primaries, some unassigned replicas.
- Green with zero `unassigned_shards` is healthy.
List unassigned shards and why:
```
GET _cat/shards?v=true&h=index,shard,prirep,state,node,unassigned.reason&s=state
GET _cluster/allocation/explain?filter_path=index,node_allocation_decisions.node_name,node_allocation_decisions.deciders.*
```
`prirep` is `p` for primaries and `r` for replicas. Run allocation explain first. A single-node cluster is always yellow because a replica is never assigned to the same node as its primary; set `number_of_replicas` to 0 only if you accept no redundancy. If a node holding a primary is lost with no usable replica, allocation explain reports `no_valid_shard_copy`; recovery options include restoring from a snapshot, or a cluster reroute `allocate_stale_primary` / `allocate_empty_primary` with `accept_data_loss: true`, which loses data.

## 3. Disk watermarks
Defaults: low 85% (no new shards allocated to a node above it; has no effect on primaries of new indices but blocks their replicas), high 90% (Elasticsearch tries to relocate shards away), flood stage 95% (an `index.blocks.read_only_allow_delete` block is put on every index with a shard on that node). The block is released automatically when disk use falls below the high watermark. Percentage watermarks are capped by max headroom settings on big disks. If every node is above the low watermark, no shards can be allocated or moved. Raising watermarks is usually a temporary fix.
```
GET _cat/allocation?v
```

## 4. Heap and circuit breakers
- Set `Xms` and `Xmx` to no more than 50% of the memory available to the node, and no more than the compressed-oops threshold: 26GB is safe on most systems and the limit can be as high as 30GB on some. The log line "compressed ordinary object pointers [true]" confirms you are under it.
- Circuit breakers (`indices.breaker.total.limit`, `indices.breaker.fielddata.limit`, `indices.breaker.request.limit`) throw a `CircuitBreakingException` instead of letting the node run out of memory. High JVM memory pressure can also stop allocation and leave shards unassigned.

## 5. Allocation awareness and filtering
`cluster.routing.allocation.awareness.attributes` (for example a `rack_id` attribute) keeps primary and replica copies from sharing a location. `cluster.routing.allocation.awareness.force.*` names values that must exist for shards to be reallocated after a location failure. Allocation filtering and forced awareness can prevent the shard movements that watermark handling or rebalancing needs, so check allocation explain when shards stay put.

## Verify
- [ ] Average shard size is checked against 10GB to 50GB, not left at defaults.
- [ ] `_cluster/allocation/explain` is the first command on any unassigned shard.
- [ ] Disk use is alerted below the 85% low watermark.
- [ ] Heap is at most 50% of node memory and under the compressed-oops threshold.

## Checked
2026-11-09. Checked against elastic/docs-content (size your shards; red or yellow cluster status) and the elastic/elasticsearch reference (cluster-level shard allocation settings, JVM settings, circuit breaker settings).
Corrected: the "31-32GB" compressed-oops ceiling (docs say 26GB safe, up to 30GB on some systems); the 50% heap rule is confirmed.
Removed as unsupported: the "20 shards per GB of heap" ceiling (current docs give 3000 indices per GB of heap on master-eligible nodes), "one index per day with 5 shards" anecdote, the node-restart cause of yellow, the fielddata-on-text advice, and the claim that flood stage is reapplied after clearing the block.
Method: documentation only; no commands were run.
