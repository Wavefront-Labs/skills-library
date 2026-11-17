---
id: computing-software.messaging-and-integration.apache-kafka.kafka-replication-isr-model
name: kafka-replication-isr-model
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, replication, isr, replica-lag-time-max-ms, broker-session-timeout-ms]
level: advanced
status: docs-checked
description: "Understand how the ISR defines liveness and commit: broker.session.timeout.ms, replica.lag.time.max.ms and why f+1 replicas tolerate f failures."
sources:
  - https://kafka.apache.org/42/design/design/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reason correctly about Kafka replication and failure tolerance.

Each partition has one leader and zero or more followers; the replica count including the leader is the replication factor. Writes go to the leader, and followers pull from it like normal consumers. Reads can go to the leader or followers.

A broker is "in sync" when it satisfies two conditions:
1. It keeps an active session with the controller. In KRaft clusters this means periodic heartbeats; if none arrives before `broker.session.timeout.ms` expires, the node is considered offline.
2. A follower replicates the leader's writes and does not fall too far behind. Replicas that cannot catch up to the leader's log end within `replica.lag.time.max.ms` are removed from the ISR.

The ISR is persisted in cluster metadata when it changes; any ISR member is eligible for leader election. A write is committed only when all in-sync replicas have it. With f+1 replicas a topic tolerates f failures without losing committed messages, versus 2f+1 replicas for a majority-vote quorum.

Kafka assumes fail/recover failures only (no Byzantine faults). Crashed nodes need not recover data intact: a replica must fully resync before rejoining the ISR. Kafka stays available after a short failover for node failures, but may not remain available during network partitions.

## Checked

Method: docs-checked 2026-11-09 against kafka.apache.org/42/design/design/ (Replication, Replicated Logs, Unclean Leader Election, Availability and Durability, Log Compaction sections read in full)
