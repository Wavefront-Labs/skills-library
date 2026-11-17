---
id: computing-software.messaging-and-integration.apache-kafka.kafka-consumer-offset-tracking
name: kafka-consumer-offset-tracking
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, consumer-offsets-topic, group-coordinator, coordinator-load-in-progress]
level: practitioner
status: docs-checked
description: "How committed offsets are stored in the compacted __consumer_offsets topic via the group coordinator, and the CoordinatorLoadInProgressException retry case."
sources:
  - https://kafka.apache.org/42/implementation/distribution/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand where consumer group offsets live.

Each consumer group is assigned a designated broker, the group coordinator, based on the group name. Consumers find it by sending a FindCoordinatorRequest to any broker; if the coordinator moves, they must rediscover it. Offset commits (automatic or manual) and fetches all go to this coordinator.

On an OffsetCommitRequest, the coordinator appends the commit to the special compacted topic `__consumer_offsets`. It replies success only after all replicas of that topic have received the offsets. If replication does not finish within a configurable timeout, the commit fails and the consumer may retry after backing off. Brokers compact the topic periodically, since only the latest commit per partition is needed.

The coordinator also caches offsets in memory so offset fetches return the last committed offset vector quickly.

Failure mode: if the coordinator has just started, or has just become coordinator by taking leadership of an offsets-topic partition, it may need to load that partition into its cache. Offset fetches then fail with CoordinatorLoadInProgressException, and the consumer may retry the OffsetFetchRequest after backing off.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 implementation/distribution page. All claims matched; no content changes. No hands-on run.
