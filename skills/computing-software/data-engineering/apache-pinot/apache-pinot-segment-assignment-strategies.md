---
id: computing-software.data-engineering.apache-pinot.apache-pinot-segment-assignment-strategies
name: apache-pinot-segment-assignment-strategies
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, segment-assignment, balanced, replica-group, partitioned-replica-group, segmentassignmentconfigmap, partitioncolumn, allservers, dimension-table, strict-replica-group]
level: advanced
status: docs-checked
description: "Choosing a segment assignment strategy: balanced, replica-group, partitioned, round-robin, partitionColumn, dimension tables, strict rules."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/segment-assignment.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Segment assignment strategies

Segment assignment assigns each segment of a table to the servers hosting it; the right strategy reduces query routing overhead. It is configured along with instance assignment.

Strategies:
- **Balanced** (default): each segment goes to the server with the fewest segments, so load is balanced but every query is routed to all servers. Fine for small use cases.
- **Replica-group**: servers are split into replica groups, each holding a full copy of all segments. A query is routed only to servers within one replica group, so adding groups raises throughput without raising fanout.
- **Partitioned replica-group**: extends replica-group by assigning segments of the same partition to the same set of servers, so a query filtering on the partition column (for example `memberId = 123`) only reaches the servers for that partition.
- **Round-robin**: for tables where new segments are in high demand. `roundRobin` extends the balanced strategy and `roundRobinReplicaGroup` extends the replica-group one, cycling through instances for new segments instead of always choosing the least loaded. The counter is in memory per controller, randomized at start; it applies to new assignment only.

Partition column, in the table-level `segmentAssignmentConfigMap` (OFFLINE entry, or a tier name as key):
```
"segmentAssignmentConfigMap": { "OFFLINE": { "partitionColumn": "memberId" } }
```
`segmentAssignmentStrategy` is optional in an entry (derived from the instance partitions if omitted). The column must occur in `segmentPartitionConfig`, and defaults to its sole column when none is configured. The legacy `instanceAssignmentConfigMap.<type>.replicaGroupPartitionConfig.partitionColumn` and `segmentsConfig.replicaGroupStrategyConfig.partitionColumn` are deprecated; all explicit columns must agree.

Dimension tables: Pinot always assigns their segments to all servers in the tenant for local lookups. You can make it explicit with `"segmentAssignmentConfigMap": { "OFFLINE": { "segmentAssignmentStrategy": "allservers" } }`; leaving it unset also works.

Strict replica-group routing, and upsert or dedup tables (dimension tables exempt), must use a layout that keeps partition consistency; existing tables are not grandfathered and can fail validation on their next update:
- OFFLINE: replica-group instance assignment with exactly one instance per partition in each replica group (`numInstancesPerPartition=1`); explicit OFFLINE segment strategy must be `replicagroup` or `roundrobinreplicagroup`.
- REALTIME: a partitioned CONSUMING layout must have one instance per partition, and COMPLETED segments must not be relocated through a separate instance assignment or `realtimeCompleted` tenant tag.
- After changing instance placement, use table rebalance to move pinned partitions.

## Checked

2026-11-08. Read the whole pinot-docs segment-assignment page. Confirmed strategies, partition-column configuration, dimension table behaviour and strict replica-group requirements. Removed the unsourced "changing strategy requires a rebalance" and the instanceSelectorType pairing advice; corrected partitioned replica-group (same set of servers, not a fixed instance); added the round-robin strategies.

Method: documentation only; no commands were run.
