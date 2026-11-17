---
id: computing-software.messaging-and-integration.apache-kafka.kafka-mirrormaker-replication-flows
name: kafka-mirrormaker-replication-flows
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, mirrormaker-2, replication-flows, connect-mirror-maker-properties, topics-exclude]
level: practitioner
status: docs-checked
description: "Define MirrorMaker 2 clusters and directional replication flows in connect-mirror-maker.properties with topics and groups filters."
sources:
  - https://kafka.apache.org/42/operations/geo-replication-cross-cluster-data-mirroring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replicate topics, topic configs, consumer groups with offsets, and ACLs between Kafka clusters. MirrorMaker 2 is built on Kafka Connect and also preserves partitioning and detects new topics and partitions.

Minimal config:
```
clusters = primary, secondary
primary.bootstrap.servers = broker10-primary:9092,broker-11-primary:9092
secondary.bootstrap.servers = broker5-secondary:9092,broker6-secondary:9092
primary->secondary.enabled = true
```
`clusters` and `{alias}.bootstrap.servers` are required. Flows are written `{source}->{target}` and are directional; a flow does nothing until `{source}->{target}.enabled = true` (default false). For two-way replication enable both directions.

Filters, with defaults:
- `topics = .*`; `topics.exclude = .*[\-\.]internal, .*\.replica, __.*`
- `groups = .*`; `groups.exclude = console-consumer-.*, connect-.*, __.*`

Top-level settings are defaults; override per flow with `{source}->{target}.{config}`, for example `us-west->us-east.topics = foo.*`. Patterns:
- Active/passive: A->B
- Active/active: A->B, B->A (no need for topics.exclude to prevent loops if defined in one file)
- Aggregation: A->K, B->K, C->K; fan-out: K->A, K->B, K->C

Testing note: groups created by kafka-console-consumer.sh are excluded by default; adjust `groups.exclude` while testing, then restore it.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 geo-replication page (replication flow section). Config names, defaults, per-flow override syntax and topologies matched; the intro feature list and the loop-prevention remark were not re-confirmed in my read. No hands-on run.
