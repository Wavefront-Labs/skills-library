---
id: computing-software.data-engineering.apache-kafka.connector-offsets-management
name: connector-offsets-management
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-connect, connector-offsets, kip-875, reset-connector, source-offsets, sink-offsets, debezium-offsets]
level: advanced
status: docs-checked
description: "Read, alter and reset Kafka Connect source and sink connector offsets with the KIP-875 REST API (Kafka 3.6+), plus the legacy offsets-topic workaround."
sources:
  - https://kafka.apache.org/documentation/#connect_rest
  - https://github.com/apache/kafka/blob/trunk/docs/kafka-connect/user-guide.md
  - https://github.com/apache/kafka/blob/trunk/connect/api/src/main/java/org/apache/kafka/connect/source/SourceConnector.java
  - https://github.com/apache/kafka/blob/trunk/connect/runtime/src/main/java/org/apache/kafka/connect/util/SinkUtils.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connector offsets management

**Goal:** make a connector reprocess, skip ahead, or start fresh without renaming it or hand-editing internal topics.

## Where offsets live
- **Source connectors:** connector-defined partition and offset maps stored in the Connect offsets topic (`offset.storage.topic`). The request body format depends on the connector implementation.
- **Sink connectors:** a normal consumer group named `connect-<connector-name>`; the sink request body format is common across all sink connectors (`kafka_topic`, `kafka_partition`, `kafka_offset`).

## Offsets API (KIP-875, Kafka 3.6)
```bash
curl -s $CONNECT/connectors/s3-sink/offsets
# Must STOP first (not pause)
curl -s -X PUT $CONNECT/connectors/s3-sink/stop
```
**Reset everything:**
```bash
curl -s -X DELETE $CONNECT/connectors/s3-sink/offsets
```
**Alter sink offsets:**
```bash
curl -s -X PATCH -H 'Content-Type: application/json' $CONNECT/connectors/s3-sink/offsets -d '{
  "offsets": [
    {"partition": {"kafka_topic": "orders", "kafka_partition": 0}, "offset": {"kafka_offset": 1500000}},
    {"partition": {"kafka_topic": "orders", "kafka_partition": 1}, "offset": {"kafka_offset": 1498000}}
  ]}'
```
**Alter source offsets** (format is connector-specific; copy the shape from GET):
```bash
curl -s -X PATCH -H 'Content-Type: application/json' $CONNECT/connectors/file-src/offsets -d '{
  "offsets": [{"partition": {"filename": "/data/in.txt"}, "offset": {"position": 0}}]}'
```
Then `PUT .../resume`.

A source connector must opt in by overriding `SourceConnector.alterOffsets` (since 3.6; the default implementation returns `false`, meaning not supported); check the connector's documentation.

A connector can also be created with `initial_offsets` in the `POST /connectors` body (same format as the PATCH body), which replaces any existing offsets for that name.

## Before Kafka 3.6
Sink: stop the connector, then use `kafka-consumer-groups.sh --reset-offsets` on the group `connect-<connector-name>` (consumers must be inactive; `--dry-run` is the default). Source offsets had no supported tool: editing the offsets topic by hand is error-prone, so prefer upgrading or using a new connector name. Connector-specific behaviour after a reset (for example a change-data-capture connector re-snapshotting) is described in that connector's documentation.

## Gotchas
- `PATCH` and `DELETE` on offsets require the connector to exist and be in the stopped state; `PUT /connectors/{name}/stop` first, `PUT .../resume` afterwards.
- With exactly-once source support a connector can have its own offsets topic (`offsets.storage.topic` in the connector config).
- MirrorMaker 2 source connectors are Connect source connectors too; resetting their offsets restarts their replication position.

## Verify
- [ ] `GET .../offsets` shows the intended positions before resuming.
- [ ] After resume, first records processed match the new starting point (check sink or connector logs).

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed (user guide REST section, SinkUtils and SourceConnector source): `GET`, `PATCH` and `DELETE /connectors/{name}/offsets`, the stopped-state requirement, the sink body format and `connect-<connector>` group naming, `initial_offsets` on create, `SourceConnector.alterOffsets` default `false` since 3.6, per-connector `offsets.storage.topic`, and `kafka-consumer-groups.sh --reset-offsets` semantics. Fixed: the earlier statement that reset works even when the connector has not implemented alteration is not supported by the API contract (the default means unsupported). Removed: Debezium and Postgres replication-slot specifics, `kcat` offsets-topic editing, the `consumer.override.group.id` remark, the 400 status code and the FilePulse and S3 examples.

Method: documentation only; no commands were run.
