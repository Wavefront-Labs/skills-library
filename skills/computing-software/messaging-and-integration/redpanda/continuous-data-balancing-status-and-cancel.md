---
id: computing-software.messaging-and-integration.redpanda.continuous-data-balancing-status-and-cancel
name: continuous-data-balancing-status-and-cancel
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [continuous-data-balancing, balancer-status, movement-cancel, disk-threshold, space-management, enterprise]
level: advanced
status: docs-checked
description: "Operate Continuous Data Balancing: node availability and autodecommission timeouts, how the 80 percent disk threshold is computed, balancer-status states and canceling moves."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/continuous-data-balancing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Continuous Data Balancing (enterprise license) watches node and rack availability and disk usage and keeps the configured replication level after failures. Node availability has the highest priority, so after a rack is lost replicas move to the remaining nodes even when that violates rack awareness. Enable it with `partition_autobalancing_mode=continuous`.

| Property | Effect |
|---|---|
| `partition_autobalancing_node_availability_timeout_sec` | After this much unreachability Redpanda re-creates the node's replicas elsewhere; the node stays a member and can rejoin |
| `partition_autobalancing_node_autodecommission_timeout_sec` | After this, the node is permanently decommissioned |
| `partition_autobalancing_max_disk_usage_percent` | Move replicas off a node at this usage; default 80 |

**Disk threshold math.** With space management on (default) the percentage applies to the log-storage target, not raw disk: the lower of `retention_local_target_capacity_bytes` and the percentage-derived value. With defaults `disk_reservation_percent` 25 and `retention_local_target_capacity_percent` 80, a node reaches the 80% threshold at about 48% of raw disk (0.75 x 0.80 x 0.80). Data already uploaded to Tiered Storage counts as free since it can be evicted.

**Status**
```bash
rpk cluster partitions balancer-status
```
It reports time since last balancing, moves in progress, unavailable nodes and nodes over the threshold, with a state of `off`, `ready`, `starting`, `in-progress` or `stalled`. For `stalled`, check: enough healthy nodes (a three-node cluster cannot move three-replica partitions), free space below thresholds somewhere, quorum for the partitions, and no node in maintenance mode.

**Cancel**
```bash
rpk cluster partitions movement-cancel
rpk cluster partitions movement-cancel --node 1
```
If continuous balancing stays on, another round is scheduled. To stop everything, set the mode to `off` first, then cancel.

## Checked

2026-11-04. The property table, threshold calculation, status states, stalled checklist and cancel commands were confirmed on the Continuous Data Balancing page.

Method: documentation only; no commands were run.
