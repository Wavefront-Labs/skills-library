---
id: computing-software.messaging-and-integration.redpanda.decommission-broker-procedure
name: decommission-broker-procedure
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [decommission, brokers, rpk-cluster-brokers, reallocation, node-id, autodecommission]
level: practitioner
status: docs-checked
description: "Decommission a Redpanda broker with rpk cluster brokers decommission and decommission-status, and what to do when reallocation stalls."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/decommission-brokers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Decommissioning reallocates a broker's partition replicas to the remaining brokers and removes it. Use it when a broker lost its storage and needs a new ID, when replacing hardware, or when shrinking the cluster. A decommissioned broker cannot rejoin; a broker with the same ID trying to rejoin is rejected, and a new broker must get a unique ID. Maintenance mode first is optional because decommissioning drains leadership itself.

**What happens.** The controller leader builds a reallocation plan, executed in batches of 50 by default (`partition_autobalancing_concurrent_moves`). Each move is a Raft group reconfiguration handled by the partition leader. No new partitions are allocated to the broker meanwhile. The process tolerates controller leadership transfers and succeeds only when every reallocation finishes.

**Steps**
```bash
rpk cluster info -X brokers=<broker-url>:<kafka-api-port>
rpk cluster brokers decommission <broker-id> -X admin.hosts=<broker-url>:<admin-api-port>
rpk cluster brokers decommission-status <broker-id> -X admin.hosts=<broker-url>:<admin-api-port>
```
Add `--skip-liveness-check` if the broker is not running, otherwise the command fails verifying its version. The start command returns `Success, broker <broker-id> decommission started.` The status output uses cached health data refreshed every 10 seconds; when completion is 100% on all rows, it is done.

**Automatic option.** With Continuous Data Balancing on, `partition_autobalancing_node_autodecommission_timeout_sec` decommissions brokers that stay unavailable that long.

**If it stalls**
- Make sure a controller leader exists and every reconfiguring partition has a leader.
- Raise `raft_learner_recovery_rate` and watch `redpanda_raft_recovery_partition_movement_available_bandwidth`.
- Otherwise enable TRACE logging on the controller leader.

## Checked

2026-11-08. Read the whole Decommission Brokers page and confirmed the circumstances, no-rejoin rule, optional maintenance mode, batches of 50 with partition_autobalancing_concurrent_moves, the controller-leader plan and Raft reconfiguration, the three commands, --skip-liveness-check, the success message, the 10-second cached status, 100% completion, the automatic option, unique ID advice and the troubleshooting list. Nothing removed.

Method: documentation only; no commands were run.
