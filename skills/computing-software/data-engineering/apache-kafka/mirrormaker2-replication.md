---
id: computing-software.data-engineering.apache-kafka.mirrormaker2-replication
name: mirrormaker2-replication
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, mirrormaker, mirrormaker2, geo-replication, mm2-properties, replication-policy, identityreplicationpolicy, sync-topic-configs, heartbeats, connect-mirror-maker]
level: advanced
status: docs-checked
description: "Replicate Kafka topics with MirrorMaker 2: dedicated mm2.properties, topic/group filters, replication policies and topic naming, config sync, and monitoring."
sources:
  - https://kafka.apache.org/documentation/#georeplication
  - https://github.com/apache/kafka/blob/trunk/connect/mirror/src/main/java/org/apache/kafka/connect/mirror/MirrorCheckpointConfig.java
  - https://github.com/apache/kafka/blob/trunk/connect/mirror-client/src/main/java/org/apache/kafka/connect/mirror/IdentityReplicationPolicy.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MirrorMaker 2 replication

**Goal:** continuously copy selected topics (and consumer offsets) from one Kafka cluster to another for DR, migration or regional aggregation.

## Run it
MM2 is a set of Kafka Connect connectors (MirrorSourceConnector, MirrorCheckpointConnector, MirrorHeartbeatConnector). Simplest: dedicated mode.
```properties
# mm2.properties
clusters = primary, dr
primary.bootstrap.servers = p1:9093,p2:9093
dr.bootstrap.servers = d1:9093,d2:9093
primary.security.protocol = SASL_SSL      # per-cluster client configs prefixed by alias
primary->dr.enabled = true
primary->dr.topics = orders\..*, crm\..*
primary->dr.topics.exclude = .*[\-\.]internal, .*\.replica, __.*
primary->dr.groups = billing-.*, analytics-.*
replication.factor = 3
sync.topic.configs.enabled = true
sync.topic.acls.enabled = false            # default true; only literal topic ACLs are synced, see the config-and-ACL skill
emit.checkpoints.enabled = true
sync.group.offsets.enabled = true          # write translated offsets into the target cluster's consumer offsets
emit.heartbeats.enabled = true
tasks.max = 8
# internal topics RF
checkpoints.topic.replication.factor = 3
heartbeats.topic.replication.factor = 3
offset-syncs.topic.replication.factor = 3
```
```bash
connect-mirror-maker.sh mm2.properties
```
Run MM2 in the data center of the target cluster, reading from the remote source (the docs pass `--clusters <nearby alias>` so the process only replicates into nearby clusters). For multi-node dedicated deployments set `dedicated.mode.enable.internal.rest=true` (KIP-710) for intra-cluster communication; the Connect REST settings can also be given in the MirrorMaker config. The connectors can also be deployed on an existing Connect cluster.

## Replication policies
- `DefaultReplicationPolicy`: remote topics are prefixed with the source cluster alias (`primary.orders.v1`), so records from different clusters are never written to the same topic-partition. Consumers in DR must subscribe to the prefixed name (or a pattern matching both).
- `IdentityReplicationPolicy`: does not rename remote topics. It suits migrating from legacy MirrorMaker and one-way replication, but MirrorMaker cannot prevent cycles with it, so keep the topology acyclic.

## Limits
- Replication is asynchronous: RPO = replication lag at failure time.
- Offsets differ between clusters (that's why checkpoints/offset translation exist).
- MirrorMaker preserves partitioning, and it detects new topics and partitions automatically.
- Exactly-once is supported on dedicated MirrorMaker clusters as of Kafka 3.5.0: set `exactly.once.source.support=enabled` for each target cluster that should be written with exactly-once semantics (existing clusters go through `preparing` first). Otherwise duplicates are possible after restarts.

## Monitor
- MirrorSourceConnector metrics `replication-latency-ms` (with `-min`, `-max`, `-avg` variants), `record-age-ms`, `byte-rate` and `record-rate`, under `kafka.connect.mirror`.
- The heartbeat connector writes to the `heartbeats` topic (default policy): it confirms end-to-end flow.
- Connect REST status of each connector/task.

## Verify
- [ ] New messages in `orders.v1` on primary appear in DR within the target latency.
- [ ] Topic configs (retention, cleanup.policy) match on both sides.
- [ ] An alert on `replication-latency-ms` (max or avg) is defined.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: MirrorSourceConnector, MirrorCheckpointConnector and MirrorHeartbeatConnector roles, `topics` default `.*` and `topics.exclude` default `.*[\-\.]internal, .*\.replica, __.*`, `emit.checkpoints.enabled`, `sync.group.offsets.enabled`, `emit.heartbeats.enabled` and the topic replication-factor property names (MirrorCheckpointConfig, MirrorHeartbeatConfig, MirrorConnectorConfig source), the `--clusters` flag and running near the target, `dedicated.mode.enable.internal.rest` (KIP-710), DefaultReplicationPolicy prefixing, IdentityReplicationPolicy cycle warning, partition preservation, exactly-once as of 3.5.0, the MirrorSource metric names, and the default `heartbeats` topic name. Removed: the 2.7, 3.0 and 3.3 version labels, the "3.5+ multi-node" label, the `p99` metric claim (the docs list min, max and avg) and the KIP-382 link.

Method: documentation only; no commands were run.
