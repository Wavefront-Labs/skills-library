---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.nalsd-distributed-design-iteration
name: nalsd-distributed-design-iteration
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [distributed-design-iteration, scaling-by-sharding, nalsd, sharding, replication, system-design]
level: sme
status: docs-checked
description: "Iterate from a single-machine design to a distributed one: shard by the bottleneck, replicate shards, add datacenters with consensus, and recompute resources each time."
sources: ["https://sre.google/workbook/non-abstract-design/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iterating to a distributed design

Workbook NALSD: each iteration defines a design, examines its strengths and weaknesses, and either feeds the next
iteration or ends with a recommendation. In practice you bounce between questions (possible, better, feasible,
resilient) rather than following a strict order. When a design flounders, modify or replace components.

## The Workbook's iterations (AdWords click-through-rate example)
1. **One machine**: rejected on IOPS, capacity and single points of failure (see `nalsd-single-machine-design`).
2. **MapReduce**: scales horizontally, but as a batch processor it cannot meet the 5-minute freshness SLO; small
   non-overlapping batches miss clicks whose query landed in a different batch.
3. **LogJoiner**: scale the larger log (queries) as a store keyed by `query_id` (QueryStore); a LogJoiner reads the
   click stream and joins; results are kept by `ad_id` in ClickMap and QueryMap. Clicks with no matching query are
   set aside, retried until a time limit, then discarded. Compute network use per component (about 400 Mbps
   aggregate in the example) and daily storage (about 14 GB/day rounded to 20 GB for ClickMap, about 2 TB/day for
   QueryMap).
4. **Sharded LogJoiner**: a log sharder hashes the `query_id`, takes it modulo the number of shards and sends the
   record to that shard. QueryMap is sharded by `ad_id` since that is known before any read or write. Send each
   record to two shards so a LogJoiner failure does not stall results; keep the duplicates on different machines;
   the error budget covers a double failure, and logs can be reprocessed.
5. **Multi-datacenter**: one datacenter is a single point of failure, so replicate ClickMap with three or five
   replicas using a consensus algorithm such as Paxos. A write needs at least one network round trip, which
   bounds sequential throughput: at roughly 25 ms per operation (datacenters a few hundred kilometres apart) that
   is 40 operations per second per process, so 10^4 sequential operations per second needs at least 250
   processes per datacenter, sharded by `ad_id`, plus more for backlog.

## Per-iteration loop
- Name the bottleneck, change the design to remove it, recompute memory, network and process counts, then check
  every requirement again.

## Gotchas
- Consensus-based replication limits sequential throughput to the round-trip time; parallelise across shards.
- Recompute the numbers after every change; replicating work doubles the transaction rate downstream.
- The 25 ms and 40 ops/s figures are the chapter's assumption, not a measurement of your network.

## Verify
- [ ] Each iteration documented with the bottleneck it removes and the new resource table.
- [ ] Final design checked against every requirement.

## Checked
2026-11-01. Confirmed against the SRE Workbook chapter "Introducing Non-Abstract Large System Design": MapReduce and LogJoiner iterations, QueryStore/ClickMap/QueryMap, log sharder hash-modulo steps, duplicate shards, three or five replicas with Paxos, 25 ms operation, 40 ops/s, 250 processes.
Removed: invented shard arithmetic (950 TB, 34 machines), regions and worker counts, and generic pattern claims the chapter does not state.
Method: documentation only; no commands were run.
