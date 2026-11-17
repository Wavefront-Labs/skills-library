---
id: computing-software.messaging-and-integration.apache-kafka.kafka-partition-reassignment
name: kafka-partition-reassignment
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, kafka-reassign-partitions-sh, reassignment-json-file, increase-replication-factor]
level: advanced
status: docs-checked
description: "Move partitions to new brokers or raise replication factor with kafka-reassign-partitions.sh generate, execute and verify."
sources:
  - https://kafka.apache.org/42/operations/basic-kafka-operations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move partition replicas between brokers. New brokers get no existing data until partitions are moved.

The tool has three mutually exclusive modes:
- `--generate`: given topics and brokers, propose a plan that moves all partitions of those topics to the listed brokers. Nothing moves yet.
- `--execute`: start the reassignment from `--reassignment-json-file`.
- `--verify`: report completed, failed or in-progress status for the partitions of the last execute.

Generate a plan:
```
bin/kafka-reassign-partitions.sh --bootstrap-server localhost:9092 --topics-to-move-json-file topics-to-move.json --broker-list "5,6" --generate
```
with `{"topics":[{"topic":"foo1"},{"topic":"foo2"}],"version":1}` as the input. Save the printed current assignment for rollback, and save the proposed one as the file for `--execute`.

Custom plan: hand-write `{"version":1,"partitions":[{"topic":"foo1","partition":0,"replicas":[5,6]}]}` and run `--execute` directly.

Raise replication factor by listing extra replicas, for example `"replicas":[5,6,7]` for a partition that only had broker 5. Confirm with `kafka-topics.sh --describe`.

Always run `--verify` with the same JSON file. The tool does not choose what to move or auto-generate a decommissioning plan; you must craft that.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Basic Kafka operations page (Expanding your cluster, Decommissioning brokers, Increasing replication factor). Removed: unsupported 'Replication factor stays constant' sentence.

Method: documentation only; no commands were run.
