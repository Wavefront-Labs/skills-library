---
id: computing-software.messaging-and-integration.apache-kafka.kafka-eligible-leader-replicas
name: kafka-eligible-leader-replicas
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, elr, eligible-leader-replicas-version, min-insync-replicas, kip-966]
level: advanced
status: docs-checked
description: "Enable Eligible Leader Replicas with eligible.leader.replicas.version=1 and understand the min.insync.replicas side effects."
sources:
  - https://kafka.apache.org/42/operations/eligible-leader-replicas/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use ELR (KIP-966 part 1) so replicas outside the ISR can safely become leader.

Because the strict min ISR rule stops the high watermark from advancing when the ISR is smaller than `min.insync.replicas`, some non-ISR replicas are safe leaders. The KRaft controller records them in the PartitionRecord field Eligible Leader Replicas. Leader selection order:
1. If the ISR is not empty, select one of them.
2. If the ELR is not empty, select one that is not fenced.
3. Select the last known leader if it is unfenced.

Availability: introduced in 4.0, enabled by default on new clusters from 4.1. To enable on the server, set `eligible.leader.replicas.version=1`; the controller then starts tracking ELR. Downgrade safely with `eligible.leader.replicas.version=0`.

Inspect: the ELR fields come from the DescribeTopicPartitions API; the admin client reads them by describing topics.

Side effects while ELR is enabled:
- A cluster-level `min.insync.replicas` is added if absent, equal to the static config on the active controller, and cannot be removed.
- Updating the cluster-level value, even to the same value, clears all ELR state.
- The broker-level value is removed and cannot be altered; set it at cluster level.
- Updating a topic's `min.insync.replicas` clears ELR state.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 eligible-leader-replicas page. All claims matched the page; no changes to content. No hands-on run.
