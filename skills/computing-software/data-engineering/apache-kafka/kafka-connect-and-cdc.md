---
id: computing-software.data-engineering.apache-kafka.kafka-connect-and-cdc
name: kafka-connect-and-cdc
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-connect, debezium, cdc, change-data-capture, dead-letter-queue, single-message-transform, smt, distributed-mode, connect-rebalance, binlog, wal, snapshot-mode, converters]
level: practitioner
status: docs-checked
description: "Run Kafka Connect connectors and Debezium CDC reliably in production: snapshots, converters, dead letter queues and worker storage topics."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
  - https://kafka.apache.org/documentation/#connect
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka Connect and CDC in production

**Goal:** get database changes into Kafka (or Kafka into a sink) without silent drops, poison-pill crashes, or a connector that blocks replication on the source.

## 1. Debezium CDC basics
Debezium reads the source database's change log (for Postgres, logical decoding with `pgoutput` or `decoderbufs`) rather than polling queries. Most PostgreSQL servers do not retain the complete history in the WAL, so the first time the connector starts it performs an initial consistent snapshot, then streams from the position it read. The `snapshot.mode` property controls this: `initial` (default) snapshots when no Kafka offsets topic exists; `initial_only` snapshots and stops; `when_needed` snapshots only if it finds no offsets or a recorded log position that is no longer available on the server. Check the specific connector's snapshot behavior before pointing it at a busy production primary.
- **Gotcha:** the Debezium PostgreSQL docs have a section on WAL disk space consumption; read it and monitor replication-slot lag on the source database, not just connector status.

## 2. Converters and schema evolution
Connect's `key.converter` and `value.converter` control the serialized format written to Kafka, independent of the connector, so any connector can work with any serialization format (for example JSON or Avro). Audit converters across all connectors and consumers sharing a topic. For schema evolution see computing-software.data-engineering.apache-kafka.schema-registry-and-compatibility.

## 3. Dead letter queues and poison pills
The default is `errors.tolerance=none`, which fails the task on an error. To report errors in a connector's converter, transforms or the sink connector itself to a dead letter queue topic, set `errors.tolerance=all` and `errors.deadletterqueue.topic.name=<dlq-topic>`, and optionally `errors.deadletterqueue.context.headers.enable=true` for error context. The Kafka documentation describes this for sink connectors.
- Monitor the DLQ topic actively: records silently routed to a DLQ nobody reads are a data-loss incident.

## 4. Distributed mode operations
Distributed-mode workers store connector and task configurations, offsets and statuses in three topics: `config.storage.topic` (single partition, replicated, compacted), `offset.storage.topic` (many partitions, replicated, compacted) and `status.storage.topic` (multiple partitions allowed, replicated, compacted). Test a worker restart in staging and measure the pipeline pause.

## Verify
- [ ] Replication slot/WAL lag is monitored independently of connector status.
- [ ] `errors.tolerance=all` + DLQ configured on every sink connector that can receive malformed records, and the DLQ topic has an actual consumer/alert, not just existence.
- [ ] Converters match (schema-registry-aware or not) across every connector/consumer sharing a topic.
- [ ] A connector restart was tested in staging and its pause duration is within SLA.

## Checked
2026-11-01. Confirmed: Debezium PostgreSQL connector page (initial snapshot rationale, `snapshot.mode` values `initial`, `initial_only`, `when_needed`, `pgoutput`/`decoderbufs`, WAL disk space section); Kafka Connect user guide in the apache/kafka docs source (`key.converter`, `errors.tolerance`, DLQ properties, the three storage topics and their settings). Removed: MySQL binlog and SQL Server CDC claims, `no_data`/`schema_only` modes, lock behaviour, source-connector DLQ claim, cooperative-rebalance version claim and rebalance pause claim, the 5 percent example.
Method: documentation only; no commands were run.
