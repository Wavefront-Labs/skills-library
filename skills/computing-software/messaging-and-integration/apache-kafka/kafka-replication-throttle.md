---
id: computing-software.messaging-and-integration.apache-kafka.kafka-replication-throttle
name: kafka-replication-throttle
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, replication-throttle, leader-replication-throttled-rate, replica-alter-log-dirs-io-max-bytes-per-second]
level: advanced
status: docs-checked
description: "Cap rebalance traffic with kafka-reassign-partitions.sh --throttle and clear it with --verify, using the five throttle configs."
sources:
  - https://kafka.apache.org/42/operations/basic-kafka-operations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: limit bandwidth used by replica movement.

Apply a throttle when executing a reassignment:
`bin/kafka-reassign-partitions.sh --bootstrap-server localhost:9092 --execute --reassignment-json-file bigger-cluster.json --throttle 50000000 --replica-alter-log-dirs-throttle 100000000`
This caps inter-broker movement at 50MB/s and disk-to-disk movement at 100MB/s.

Change it mid-flight by re-running execute with `--additional` and the same JSON file, for example `--additional --execute ... --throttle 700000000`.

Cleanup: the throttle is removed by `--verify` once the reassignment completes. The page says to remove it in a timely manner.

Config keys, all set automatically by the tool:
- Broker dynamic: `leader.replication.throttled.rate`, `follower.replication.throttled.rate`, `replica.alter.log.dirs.io.max.bytes.per.second`
- Per topic: `leader.replication.throttled.replicas`, `follower.replication.throttled.replicas`

By default the leader throttle covers all pre-existing replicas of a partition, and the follower throttle covers only move destinations. Inspect with `kafka-configs.sh --describe --entity-type brokers` or `--entity-type topics`.

Failure mode: if the throttle is below the write rate (max(BytesInPerSec) > throttle), replication may never make progress. Watch `kafka.server:type=FetcherLagMetrics,name=ConsumerLag,clientId=...,topic=...,partition=...`; it should steadily decrease, otherwise raise the throttle.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Basic Kafka operations page (Limiting bandwidth usage during data migration, Safe usage of throttled replication). Removed: wording that unremoved throttle keeps normal traffic throttled (page says remove in a timely manner).

Method: documentation only; no commands were run.
