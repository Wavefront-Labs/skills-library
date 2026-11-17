---
id: computing-software.messaging-and-integration.apache-kafka.kafka-controlled-shutdown-and-preferred-leaders
name: kafka-controlled-shutdown-and-preferred-leaders
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, controlled-shutdown-enable, auto-leader-rebalance-enable, kafka-leader-election-sh]
level: practitioner
status: docs-checked
description: "Stop brokers gracefully with controlled.shutdown.enable and restore preferred leaders with auto.leader.rebalance.enable or kafka-leader-election.sh."
sources:
  - https://kafka.apache.org/42/operations/basic-kafka-operations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restart brokers with minimal unavailability and keep leadership balanced.

Graceful shutdown: when a server is stopped other than by a hard kill, it syncs all its logs to disk (avoiding log recovery on restart) and, with
`controlled.shutdown.enable=true`
it migrates the partitions it leads to other replicas before stopping, cutting each partition's unavailability to a few milliseconds. Controlled shutdown only succeeds if every partition on the broker has replicas, meaning replication factor above 1 and at least one other replica alive. This is intended: shutting down the last replica would make that partition unavailable.

Balancing leadership: when a broker restarts it returns only as a follower, so it serves no client reads or writes. Kafka uses preferred replicas: with replica list 1,5,9, node 1 is preferred leader because it appears first. By default the cluster tries to restore preferred leaders:
`auto.leader.rebalance.enable=true`

If you set it to false, restore leadership manually:
`bin/kafka-leader-election.sh --bootstrap-server localhost:9092 --election-type preferred --all-topic-partitions`

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Basic Kafka operations page (Graceful shutdown, Balancing leadership). Removed: nothing.

Method: documentation only; no commands were run.
