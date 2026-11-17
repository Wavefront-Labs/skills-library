---
id: computing-software.data-engineering.apache-pinot.apache-pinot-routing-and-segment-pruning
name: apache-pinot-routing-and-segment-pruning
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, routing, segment-pruning, segmentprunertypes, segmentpartitionconfig, columnpartitionmap, functionname, numpartitions, murmur, modulo, instanceselectortype, fanout]
level: advanced
status: docs-checked
description: "Reducing query fan-out: segmentPrunerTypes (time, partition), segmentPartitionConfig functions, broker vs server-side pruning."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/tuning/routing.md", "https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/tuning/segment-pruning.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Routing and segment pruning

Fan-out (how many servers and segments a query touches) drives tail latency. Pinot prunes on the broker and again on servers.

Broker pruners:
```
"routing": { "segmentPrunerTypes": ["partition", "time"] }
```
- `time` skips segments outside the query time range.
- `partition` skips segments whose partition value cannot match.

Partition pruning needs segment partition metadata:
```
"tableIndexConfig": { "segmentPartitionConfig": { "columnPartitionMap": {
  "memberId": { "functionName": "Murmur", "numPartitions": 16 } } } }
```
Functions: `Modulo`, `Murmur` / `Murmur2`, `Murmur3`, `FNV`, `HashCode`, `ByteArray`, `BoundedColumnValue`. The function and count must match how the data was produced (the stream partitioner for realtime).

Server-side pruning then drops segments using column metadata and **bloom filters** before scanning.

Partition pruning only applies to specific queries and needs a particular data distribution. The most consistent way to limit fan-out is replica-group segment alignment with `instanceSelectorType` set to `replicaGroup`, so each query fans out to a single replica group. Filter on the partition column to benefit from partition pruning, and keep each segment to one partition.

## Checked

2026-11-09: confirmed against the Pinot Routing and Segment pruning pages (pinot-docs operate-pinot/tuning/routing.md and segment-pruning.md): broker-side `segmentPrunerTypes` for time and partition, the `segmentPartitionConfig` example, the list of supported partition functions, server-side pruning by column metadata and bloom filters, and replica-group routing reducing fan-out to a single replica group.

Method: documentation only; no commands were run.
