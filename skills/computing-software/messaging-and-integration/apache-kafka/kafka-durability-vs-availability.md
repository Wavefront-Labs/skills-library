---
id: computing-software.messaging-and-integration.apache-kafka.kafka-durability-vs-availability
name: kafka-durability-vs-availability
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, acks, min-insync-replicas, unclean-leader-election-enable]
level: advanced
status: docs-checked
description: "Trade durability against availability with acks, min.insync.replicas and unclean.leader.election.enable."
sources:
  - https://kafka.apache.org/42/design/design/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure how much data loss risk a topic accepts.

Producers choose acknowledgment with `acks`: 0 (none), 1 (leader only), or all (-1). With acks=all, acknowledgement happens once all current in-sync replicas have the message. If a two-replica topic is down to one in-sync replica, acks=all writes still succeed, and may be lost if that replica also fails.

Two topic-level settings prefer durability over availability:
- Disable unclean leader election: if all replicas are unavailable, the partition stays unavailable until the most recent leader returns. This prefers unavailability over message loss.
- Set `min.insync.replicas`: the partition accepts acks=all writes only while the ISR is at least that size. A higher value improves consistency but makes the partition unavailable for writes if the ISR drops below it.

Messages are not visible to consumers until they are replicated to all in-sync replicas and the ISR size is at least `min.insync.replicas`, regardless of acks.

Unclean election: when all replicas die, Kafka can wait for an ISR replica (default since 0.11.0.0) or elect the first replica that returns even if it was out of sync. Change this with `unclean.leader.election.enable` when uptime matters more than consistency.

The guarantee: a committed message is not lost while at least one in-sync replica stays alive.

## Checked

Method: docs-checked 2026-11-09 against kafka.apache.org/42/design/design/ (Replication, Replicated Logs, Unclean Leader Election, Availability and Durability, Log Compaction sections read in full)
