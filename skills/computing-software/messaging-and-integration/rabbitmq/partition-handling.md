---
id: computing-software.messaging-and-integration.rabbitmq.partition-handling
name: partition-handling
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, partition-handling]
level: advanced
status: docs-checked
description: "Choose cluster_partition_handling (pause_minority, autoheal, ignore) and recover from a split brain."
sources:
  - https://www.rabbitmq.com/docs/partitions
  - https://www.rabbitmq.com/docs/configure
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network partition handling

**Goal:** Control behaviour when nodes lose contact.

## Steps
1. From RabbitMQ 4.3.0 the metadata store is Raft-based (Khepri), Mnesia is gone, and partition handling strategies were removed. `cluster_partition_handling` and its `pause_if_all_down` keys are accepted but have no effect; remove them.
2. Quorum queues, streams and the metadata store all need an online majority of members; without it, operations that need consensus wait or time out.
3. Use an odd number of nodes (3, 5, 7) so a clear majority exists.
4. On versions before 4.3 the strategy setting still applied; check that version's guide.

## Failure modes
- Without an online majority, publishes, acknowledgements and metadata updates cannot make progress.

## Verify
- `rabbitmq-diagnostics cluster_status` lists reachable peers; `rabbitmq-queues quorum_status <queue>` and `rabbitmq-streams stream_status <stream>` show replica state; `rabbitmq-diagnostics check_if_node_is_quorum_critical` warns before a shutdown.

## Checked

Date: 2026-11-02. Confirmed on the Partitions guide and Configuration page. Fixed: the skill recommended `pause_minority`, autoheal and `ignore` and restart-based recovery; the current guide says strategies were removed in 4.3.0 and the keys have no effect. Removed: the pause_minority and two-node claims.

Method: documentation only; no commands were run.
