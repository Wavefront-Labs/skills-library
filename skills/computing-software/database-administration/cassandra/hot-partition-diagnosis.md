---
id: computing-software.database-administration.cassandra.hot-partition-diagnosis
name: hot-partition-diagnosis
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, hot-spot, nodetool-toppartitions, key-skew, latency-troubleshooting, hot-partition, read-latency-tuning, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Finding skew"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/toppartitions.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/nodetool.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing hot partitions and nodes

Goal: locate skew.
- `nodetool toppartitions <ks> <table> <duration>` samples and prints the most active partitions; the duration is in milliseconds (for example 10000).
- Compare nodes with `nodetool tablestats`, `nodetool tablehistograms` and `nodetool tpstats`.
- Fix by changing the partition key so load spreads.
Verify: per-node request rates even out.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: `toppartitions` synopsis and duration units, plus the other nodetool command descriptions. Removed: the caching suggestion.

Method: documentation only; no commands were run.
