---
id: computing-software.data-engineering.apache-kafka.sink-connectors-s3-and-jdbc
name: sink-connectors-s3-and-jdbc
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-connect, s3-sink-connector, jdbc-sink-connector, sink-connector, flush-size, rotate-interval-ms, partitioner, upsert, pk-mode, tasks-max]
level: advanced
status: docs-checked
description: "Configure Kafka Connect sinks: S3 sink partitioning, flush.size/rotation and exactly-once file naming; JDBC sink upsert with pk.mode, auto-evolve risks and tasks.max sizing."
sources:
  - https://docs.confluent.io/kafka-connectors/s3-sink/current/overview.html
  - https://docs.confluent.io/kafka-connectors/jdbc/current/sink-connector/sink_config_options.html
  - https://kafka.apache.org/39/kafka-connect/user-guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sink connectors: S3 and JDBC

**Goal:** land topics in object storage or a relational DB reliably, with sensible file sizes and idempotent writes.

## S3 sink (Confluent S3 sink connector)
```json
{
  "name": "orders-s3-sink",
  "config": {
    "connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "topics": "orders.checkout.order-placed.v1",
    "tasks.max": "6",
    "s3.bucket.name": "<BUCKET>", "s3.region": "eu-west-1",
    "topics.dir": "raw/kafka",
    "storage.class": "io.confluent.connect.s3.storage.S3Storage",
    "format.class": "io.confluent.connect.s3.format.parquet.ParquetFormat",
    "parquet.codec": "snappy",
    "partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",
    "path.format": "'dt'=YYYY-MM-dd/'hr'=HH",
    "partition.duration.ms": "3600000",
    "timestamp.extractor": "Record",
    "locale": "en-US", "timezone": "UTC",
    "flush.size": "50000",
    "rotate.interval.ms": "600000",
    "rotate.schedule.interval.ms": "900000"
  }
}
```
- `rotate.interval.ms` is the maximum span of record time a file stays open (it starts from the first record's timestamp via `timestamp.extractor`); a file is closed only when a later record does not fit, so a quiet topic leaves the last file open. `rotate.schedule.interval.ms` closes files on a wall-clock schedule even with no new records, and needs `timezone` set (the connector throws an exception otherwise).
- Exactly-once delivery to S3 needs a deterministic partitioner, a deterministic `timestamp.extractor` (`Record` or `RecordField`) and `rotate.interval.ms`; setting `rotate.schedule.interval.ms` is nondeterministic and invalidates the exactly-once guarantee.
- Set the number of tasks with `tasks.max`.

## JDBC sink (Confluent JDBC sink)
```json
{
  "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
  "topics": "crm.customer.state.v2",
  "connection.url": "jdbc:postgresql://<HOST>:5432/dw",
  "connection.user": "${file:/secrets/db.properties:user}",
  "connection.password": "${file:/secrets/db.properties:password}",
  "insert.mode": "upsert",
  "pk.mode": "record_key", "pk.fields": "customer_id",
  "delete.enabled": "true",
  "auto.create": "false", "auto.evolve": "false",
  "table.name.format": "stage.${topic}",
  "batch.size": "3000",
  "tasks.max": "4"
}
```
- `insert.mode=upsert` + a primary key makes redelivery idempotent; `insert` duplicates on retries.
- `delete.enabled=true` turns tombstones (null value) into deletes; requires `pk.mode=record_key`.
- Leave `auto.create` off: the connector maps STRING to a variable-length type such as TEXT, which can fail for primary keys on some dialects (the config page says not to set it with `pk.mode=kafka` on Oracle or MySQL). Create tables via migrations and review `auto.evolve` before enabling it.
- Do not put real credentials inline in connector configs; the example uses `${file:...}` placeholders, which need a config provider configured in the worker.

## Operate
```bash
curl -X PUT -H 'Content-Type: application/json' localhost:8083/connectors/orders-s3-sink/config -d @cfg.json   # create or update a connector
```
See the Connect REST API documentation for status and restart endpoints.

## Checked
2026-10-28. Confirmed on the Confluent S3 sink and JDBC sink configuration pages: exactly-once conditions, `rotate.interval.ms` versus `rotate.schedule.interval.ms` behaviour, `timezone` requirement, `timestamp.extractor` values, `tasks.max`, `pk.mode`, `pk.fields`, `delete.enabled` requiring `pk.mode=record_key`, `auto.create` caution; Kafka 3.9 Connect guide: `PUT /connectors/{name}/config`. Removed: file-naming, small-file, schema-format, Debezium, config-topic exposure, status/restart REST and `connect-<name>` consumer group claims.
Method: documentation only; no commands were run.

## Verify
- [ ] Objects appear under `dt=/hr=` paths with expected sizes; restarting the connector creates no duplicate files.
- [ ] JDBC table row count equals distinct keys in the compacted topic; tombstoned keys absent.
- [ ] Sink consumer lag stays bounded.
