---
id: computing-software.data-engineering.druid.druid-coordinator-segment-management
name: druid-coordinator-segment-management
category: computing-software
field: data-engineering
product: druid
tags: [coordinator, segments, replication, balancing, historical, tiers]
level: practitioner
status: docs-checked
description: "Describe the Druid Coordinator's cycle: load, drop, replicate and balance segments, balancer strategies, cleanup and compaction duties."
sources:
  - https://github.com/apache/druid/blob/master/docs/design/coordinator.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Coordinator manages segment distribution: it tells Historicals to load or drop segments per configuration. It loads new segments, drops outdated ones, keeps each segment replicated the configured number of times, and moves ("balances") segments so Historicals are evenly loaded.

## How it runs

It runs its duties periodically (the period is configurable), assessing cluster state each run. It uses ZooKeeper for leader election and service discovery, polls each Historical over HTTP for its served segments, and reads used segments and loading rules from the metadata database. For unassigned segments, the Historicals of each tier are sorted by capacity and the least-capacity servers get priority, which keeps balance; load and drop requests go to Historicals over HTTP. Start: `org.apache.druid.cli.Main server coordinator`. Segments load and drop according to retention rules.

## Cleanup each run

- Overshadowed segments (old versions fully replaced by newer ones) are marked unused, then unloaded on the next run. Segments the database no longer lists as used are unloaded too.
- Non-overshadowed eternity tombstones are cleaned up when they start at -INF or end at INF, do not overlap any overshadowed segment, and have 0 core partitions.

## Segment availability

If a Historical disappears, its segments are treated as dropped, but each dropped segment sits in a transitional structure with a lifetime during which it is not reassigned. A Historical that returns within that window serves from its local cache with no cluster-wide reshuffle.

## Balancing within a tier

Replication alone does not balance a tier with few Historicals or low replication, so the Coordinator moves segments using a strategy:
- `cost` (default): picks the server with minimum placement cost, avoiding adjacent or overlapping intervals on one server (they are likely queried together, skewing CPU).
- `diskNormalized`: `cost` adjusted for disk use; candidates within `druid.coordinator.balancer.diskNormalized.utilizationThreshold` (default 0.05) of the least-used candidate use normal cost, others are exponentially penalized.
- `random`: experimental, not for production.
All strategies prioritize moving segments off the Historical with the least available disk.

## Automatic compaction duty

Max running compaction tasks is `min(sum of worker capacity * slotRatio, maxSlots)`, but at least one task is always submitted when a datasource has compaction enabled. Tasks fail if input segments are removed or overshadowed first, or if a higher-priority task takes an overlapping time chunk lock; the Coordinator re-checks the interval next run. The search policy scans time chunks newest to oldest and selects a chunk when its total size is at most `inputSegmentSizeBytes` and it is uncompacted or its `maxTotalRows`/`indexSpec` spec changed. `skipOffsetFromLatest` moves the start point; realtime tasks outrank compaction by default and revoke its locks. Known gap: many small same-interval segments totalling more than `inputSegmentSizeBytes` are skipped.

The compaction duty runs in the Indexing Service duty group; to run it on its own period set `druid.coordinator.dutyGroups=[<group>]`, `druid.coordinator.<group>.duties=["compactSegments"]` and `druid.coordinator.<group>.period`.

## FAQ points

- Clients never contact the Coordinator for queries, and Brokers and Historicals are unaware of it as a query dependency.
- Start order does not matter. If all Coordinators die the cluster keeps serving, but loading and dropping stops, so the data topology freezes.

## Checked

2026-11-08. Read the cited coordinator page in full. Extended the draft with cleanup duties, availability handling, balancer strategies, the compaction duty rules and FAQ. Omitted one FAQ phrase about ZooKeeper load/drop signalling because it conflicts with the page's own HTTP description.

Method: documentation only; no commands were run.
