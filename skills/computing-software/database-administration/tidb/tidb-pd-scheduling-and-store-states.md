---
id: computing-software.database-administration.tidb.tidb-pd-scheduling-and-store-states
name: tidb-pd-scheduling-and-store-states
category: computing-software
field: database-administration
product: tidb
tags: [tidb, pd, scheduling, store-state, max-store-down-time, operators, location-labels, hot-region, tombstone]
level: advanced
status: docs-checked
description: "Reason about PD scheduling in TiDB: heartbeats, store states Up/Disconnect/Down/Offline/Tombstone, the seven scheduling strategies and the three basic operators."
sources: ["https://docs.pingcap.com/tidb/stable/tidb-scheduling"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb pd scheduling and store states

PD schedules Regions using information from two heartbeat types. TiKV stores report `StoreState` (disk capacity and availability, Region count, read/write speed, snapshots in flight, overload flag, labels). Region leaders report `RegionState` (leader and replica positions, offline replicas, read/write speed).

Store states seen in PD Control:
- Up: in service.
- Disconnect: heartbeats lost for more than 20 seconds; becomes Down past `max-store-down-time`.
- Down: heartbeats lost longer than `max-store-down-time` (30 minutes by default); PD starts replenishing replicas on surviving stores.
- Offline: manually taken offline via PD Control; Regions migrate off. It becomes Tombstone when `leader_count` and `region_count` both reach 0.
- Tombstone: fully offline; clean up with the `remove-tombstone` interface. From v6.5.0 PD auto-deletes Tombstone records after one month.

Scheduling plans consist of three basic operators: add a replica, remove a replica, transfer a Region leader (Raft commands AddReplica, RemoveReplica, TransferLeader). Operators are suggestions delivered in Region heartbeat responses, and a Region leader may skip them.

Strategies PD applies: correct replica count (`max-replicas`); replicas at different "positions" using TiKV `labels` and PD `location-labels` (rack, data center); balanced replicas, leaders, hot spots and storage size across stores; and a throttle on concurrent scheduling tasks so online traffic stays stable (conservative by default, adjustable if faster rebalancing is needed).

## Checked

2026-11-04. Confirmed against the TiDB Scheduling page: heartbeat contents, store states and their thresholds, v6.5.0 Tombstone clean-up, three operators, strategies 1 to 7.
Method: documentation only; no commands were run.
