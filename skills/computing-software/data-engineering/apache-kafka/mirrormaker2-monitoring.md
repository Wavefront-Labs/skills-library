---
id: computing-software.data-engineering.apache-kafka.mirrormaker2-monitoring
name: mirrormaker2-monitoring
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, mirrormaker2, mm2-monitoring, replication-latency, record-age, geo-replication, jmx, connect-metrics]
level: advanced
status: docs-checked
description: "Monitor MirrorMaker 2 replication health: replication latency and record-age JMX metrics, source-consumer lag, checkpoint freshness, task failures, and alert thresholds."
sources:
  - https://kafka.apache.org/39/operations/geo-replication-cross-cluster-data-mirroring/
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-382%3A+MirrorMaker+2.0
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring MirrorMaker 2

**Goal:** know how far behind the target cluster is, before a failover depends on it.

## Key MM2 metrics (JMX)
`kafka.connect.mirror:type=MirrorSourceConnector,target=<alias>,topic=<topic>,partition=<n>`:
| Metric | Meaning |
|---|---|
| `replication-latency-ms` (avg/max) | time from record timestamp at source to being written at target |
| `record-age-ms` (avg/max) | age of record when MM2 consumed it (source lag in time) |
| `record-count` | records replicated (rate) |
| `byte-rate` | throughput |

`kafka.connect.mirror:type=MirrorCheckpointConnector,source=<a>,target=<b>,group=<g>,topic=...,partition=...`:
| `checkpoint-latency-ms` | delay of consumer offset checkpoints; stale = offset translation for failover is stale |

Plus Connect worker/task metrics: `kafka.connect:type=connector-task-metrics` status, `kafka.connect:type=task-error-metrics` (`total-record-failures`), and the MM2 internal consumer's `records-lag-max`.

Export via JMX exporter (Prometheus) with a rule for `kafka.connect.mirror`.

## Alerts (set thresholds from your own RPO)
- `replication-latency-ms` max above your RPO for a sustained period.
- MM2 source consumer `records-lag-max` growing over time.
- Any MM2 task not RUNNING (`/connectors/<name>/status`).
- `checkpoint-latency-ms` far above `emit.checkpoints.interval.seconds`.
- Target topic partition count < source (config sync lagging or `sync.topic.configs.enabled=false`).

## End-to-end probe
Heartbeats: `MirrorHeartbeatConnector` emits heartbeats to a heartbeats topic in the source cluster, which is replicated to the target (KIP-382; interval set by `emit.heartbeats.interval.seconds`). Consume the replicated heartbeats topic at the target and compare the record timestamp to now: a simple, metric-independent check that the connector is running and the source is reachable.

## Throughput tuning when lagging
- Increase `tasks.max` (bounded by partition count).
- Producer: raise `linger.ms` and `batch.size` and set `compression.type` for the MM2 producer (Connect client override prefixes apply).
- Consumer: larger `fetch.max.bytes`, `max.partition.fetch.bytes`.

## Verify
- [ ] Dashboard shows per-topic replication latency and heartbeat age.
- [ ] Simulated pause of MM2 fires the latency alert within the expected time.

## Checked
2026-10-28. Confirmed in the Kafka 3.9 geo-replication page and KIP-382: MBeans `kafka.connect.mirror:type=MirrorSourceConnector,target=,topic=,partition=` and `MirrorCheckpointConnector`, metrics `replication-latency-ms`, `record-age-ms`, `checkpoint-latency-ms`, `emit.heartbeats.interval.seconds`, `emit.checkpoints.interval.seconds`, `sync.topic.configs.enabled`, the heartbeats topic replicated downstream. Removed: the HeartbeatFormatter class name and console-consumer command, numeric alert thresholds, the `producer.override.*` values and the placement advice (not found in the pages).
Method: documentation only; no commands were run.
