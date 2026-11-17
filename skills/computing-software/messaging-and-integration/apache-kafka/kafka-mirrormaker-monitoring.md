---
id: computing-software.messaging-and-integration.apache-kafka.kafka-mirrormaker-monitoring
name: kafka-mirrormaker-monitoring
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, mirrormaker-2, replication-latency-ms, record-age-ms, checkpoint-latency-ms]
level: practitioner
status: docs-checked
description: "Monitor MirrorMaker 2 via kafka.connect.mirror MBeans: replication-latency-ms, record-age-ms, byte-rate and checkpoint-latency-ms."
sources:
  - https://kafka.apache.org/42/operations/geo-replication-cross-cluster-data-mirroring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: confirm every defined replication flow is up and keeping pace.

MirrorMaker inherits all Kafka Connect metrics (such as `source-record-poll-rate`) and adds its own in the `kafka.connect.mirror` metric group. Tags: `source` (source cluster alias), `target` (target alias), `topic` (replicated topic on the target) and `partition`. Metrics are per replicated topic; the source cluster can be inferred from the topic name, so replicating topic1 from primary to secondary yields target=secondary, topic=primary.topic1.

MBean `kafka.connect.mirror:type=MirrorSourceConnector,target=...,topic=...,partition=...`:
- `record-count`, `record-rate`
- `record-age-ms` with min/max/avg: age of records when replicated
- `replication-latency-ms` with min/max/avg: time for records to propagate source to target
- `byte-rate`, `byte-count`

MBean `kafka.connect.mirror:type=MirrorCheckpointConnector,source=...,target=...,group=...,topic=...,partition=...`:
- `checkpoint-latency-ms` with min/max/avg: time to replicate consumer offsets

These metrics do not differentiate between create-time and log-append timestamps.

Practical use (this skill's own suggestion, not stated by the docs): watch replication-latency-ms and record-age-ms per topic to see whether a flow keeps pace, byte-rate to see throughput, and checkpoint-latency-ms to see how quickly consumer group offsets reach the target cluster. Because the source can be read from the topic name, one dashboard per target cluster covers every incoming flow, and each metric is reported per topic and partition, so aggregate across partitions when you want a topic-level view.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 geo-replication page (monitoring section). Metric names, MBeans and tags matched; the practical-use paragraph is the author's inference and is now labelled so. No hands-on run.
