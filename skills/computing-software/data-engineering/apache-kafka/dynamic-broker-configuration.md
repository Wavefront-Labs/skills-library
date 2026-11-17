---
id: computing-software.data-engineering.apache-kafka.dynamic-broker-configuration
name: dynamic-broker-configuration
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-operations, dynamic-broker-config, kafka-configs, cluster-default, per-broker-config, config-precedence, throttles]
level: practitioner
status: docs-checked
description: "Change Kafka broker, topic, client and user configs live with kafka-configs.sh: cluster-wide vs per-broker dynamic updates, precedence, and which settings need a restart."
sources:
  - https://kafka.apache.org/documentation/#dynamicbrokerconfigs
  - https://kafka.apache.org/documentation/#basic_ops_modify_topic
  - https://github.com/apache/kafka/blob/trunk/docs/configuration/broker-configs.md
  - https://github.com/apache/kafka/blob/trunk/tools/src/main/java/org/apache/kafka/tools/ConfigCommand.java
  - https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/clients/admin/ConfigEntry.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic broker configuration

**Goal:** change settings on a running cluster without rolling restarts, and know where an effective value comes from.

## Precedence (highest first)
1. Dynamic per-broker config (`--entity-type brokers --entity-name 2`)
2. Dynamic cluster-wide default (`--entity-type brokers --entity-default`)
3. Static `server.properties`
4. Kafka default

Topic configs override broker defaults for that topic (`log.retention.ms` -> topic `retention.ms`).

## Describe
```bash
kafka-configs.sh --bootstrap-server $BS --describe --entity-type brokers --entity-name 1 --all   # every value + source
kafka-configs.sh --bootstrap-server $BS --describe --entity-type brokers --entity-default
kafka-configs.sh --bootstrap-server $BS --describe --entity-type topics --entity-name orders
```
`--all` includes static and default values; each entry carries a source from the Admin API `ConfigEntry.ConfigSource` enum: `DYNAMIC_BROKER_CONFIG`, `DYNAMIC_DEFAULT_BROKER_CONFIG`, `STATIC_BROKER_CONFIG` or `DEFAULT_CONFIG`.

## Alter
```bash
# cluster-wide default
kafka-configs.sh --bootstrap-server $BS --alter --entity-type brokers --entity-default \
  --add-config log.cleaner.threads=4
# single broker
kafka-configs.sh --bootstrap-server $BS --alter --entity-type brokers --entity-name 3 \
  --add-config num.io.threads=16
# topic
kafka-configs.sh --bootstrap-server $BS --alter --entity-type topics --entity-name orders \
  --add-config retention.ms=604800000,min.insync.replicas=2
# remove override
kafka-configs.sh --bootstrap-server $BS --alter --entity-type topics --entity-name orders --delete-config retention.ms
```
Values containing commas are grouped with square brackets, as in `--add-config 'key=[val1,val2]'`. `--broker-logger <id>` changes a logger level on one broker.

## Commonly changed live
- Thread pools, at cluster-default level and limited to the range `currentSize / 2` to `currentSize * 2`: `num.network.threads`, `num.io.threads`, `num.replica.fetchers`, `num.recovery.threads.per.data.dir`, `log.cleaner.threads`, `background.threads` (plus the `remote.log.*` pool sizes).
- Default topic configs, applied to topics without an override: `log.segment.bytes`, `log.retention.ms`, `log.cleanup.policy`, `max.message.bytes`, `min.insync.replicas`, `unclean.leader.election.enable`, `compression.type` and others in the "Updating Default Topic Configuration" list.
- Log cleaner configs (cluster-default): `log.cleaner.threads`, `log.cleaner.io.max.bytes.per.second`, `log.cleaner.dedupe.buffer.size` and others.
- Replication throttles: `leader.replication.throttled.rate`, `follower.replication.throttled.rate`.
- SSL keystore and truststore per listener, using the `listener.name.<l>.` prefix (`ssl.keystore.type`, `ssl.keystore.location`, `ssl.keystore.password`, `ssl.key.password` in one per-broker alter request).
- Connection limits: `max.connections.per.ip`, `max.connections.per.ip.overrides`.
- Listeners can be added or removed dynamically (`listeners`, `advertised.listeners`, `listener.security.protocol.map`, per broker); the inter-broker listener stays a static setting (`inter.broker.listener.name`).
- Quotas: `--entity-type users/clients --add-config producer_byte_rate=...`.

The "Dynamic Update Mode" column of the broker config docs lists `read-only` (restart required), `per-broker`, or `cluster-wide` for each config; check it before relying on a live change.

## Where it is stored
Dynamic broker configs are stored in the cluster metadata log. Static `server.properties` is not rewritten, so record dynamic changes in version-controlled configuration or they drift from what a rebuilt cluster gets.

## Verify
- [ ] `--describe --all` shows the new value with `DYNAMIC_*` source on every broker.
- [ ] Change is recorded in version-controlled configuration so a rebuilt cluster gets it.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: precedence order (dynamic per-broker, dynamic cluster-wide default, static, Kafka default), the `read-only`/`per-broker`/`cluster-wide` update modes, `--entity-default`, `--add-config`/`--delete-config`, bracket grouping for comma values and `--all` (ConfigCommand source), the config source names (ConfigEntry source), the dynamic lists for thread pools, default topic configs, log cleaner, SSL keystore and truststore, connection quotas and listeners. Fixed: `message.max.bytes` is not on the dynamic default-topic list (it is `max.message.bytes`), `log.dirs`/`broker.id` read-only claims dropped as unconfirmed, `listeners` is dynamic per broker, and ZooKeeper storage removed.

Method: documentation only; no commands were run.
