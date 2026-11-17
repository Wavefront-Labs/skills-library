---
id: computing-software.messaging-and-integration.redpanda.partition-autobalancing-modes-and-disk-triggers
name: partition-autobalancing-modes-and-disk-triggers
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [autobalancing, partition-balancing, continuous-data-balancing, node-add, disk-usage, enterprise]
level: advanced
status: docs-checked
description: "Choose partition_autobalancing_mode (node_add, continuous, off), what triggers replica moves, how moves are prioritized by size, and recovery bandwidth and concurrency properties."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/cluster-balancing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Partition replica balancing moves data to relieve disk pressure and keep replication and rack spread. It is topic-aware by default (`partition_autobalancing_topic_aware`): Redpanda aims for equal replica counts of each topic per broker as well as an equal overall count.

```bash
rpk cluster config get partition_autobalancing_mode
rpk cluster config set partition_autobalancing_mode <value>
```

| Mode | Behavior |
|---|---|
| `node_add` | Rebalance when brokers are added; the default without an enterprise license |
| `continuous` | Also reacts to broker failures, high disk usage and rack availability (Continuous Data Balancing, enterprise) |
| `off` | No automatic balancing; not recommended for production; use only for manual moves |

**Triggers.** A broker is added (moves replicas to it, with or without a license); a broker is down for the configured timeout (a replacement replica is built from online replicas); a broker's disk usage exceeds `partition_autobalancing_max_disk_usage_percent`. The last two need `continuous`. Below the hard free-space limit Redpanda blocks producers.

**Disk-triggered priority.** Among partitions at or above a size threshold, smaller ones move first, since the source replica is deleted only after the move finishes. Partitions below the threshold go last; internal partitions such as the consumer offsets topic are deprioritized. The threshold is computed automatically, about 20 MiB with the default `raft_learner_recovery_rate` (100 MiB/s) and `partition_autobalancing_concurrent_moves` (50).

Terminology: "cluster balancing" is the umbrella; "Continuous Data Balancing" is the `continuous` mode.

## Checked

2026-11-04. Modes, triggers, properties, defaults and move prioritization were confirmed on the Cluster Balancing page.

Method: documentation only; no commands were run.
