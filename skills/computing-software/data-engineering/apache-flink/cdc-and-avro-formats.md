---
id: computing-software.data-engineering.apache-flink.cdc-and-avro-formats
name: cdc-and-avro-formats
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink-connectors, debezium-json-format, avro-confluent, changelog-formats, canal-json, schema-registry, kafka-sink]
level: practitioner
status: docs-checked
description: "Pick and configure Flink SQL formats for Kafka: json, avro-confluent with Schema Registry, and CDC changelog formats (debezium-json, debezium-avro-confluent) as update streams."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/table/formats/overview/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/table/formats/debezium/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/table/formats/avro-confluent/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CDC and Avro formats in Flink SQL

**Goal:** read Debezium change topics as proper changelog tables, and read/write Avro with Schema Registry, from Flink SQL.

## Debezium JSON as a changelog source
```sql
CREATE TABLE customers_cdc (
  id BIGINT,
  name STRING,
  segment STRING,
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'kafka',
  'topic' = 'pg.public.customers',
  'properties.bootstrap.servers' = '...',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'debezium-json',
  'debezium-json.schema-include' = 'false',          -- true if Connect JsonConverter schemas.enable=true
  'debezium-json.ignore-parse-errors' = 'true'
);
```
Flink interprets Debezium JSON and Avro messages as INSERT/UPDATE/DELETE changes, so downstream aggregations and joins see correct retractions.
- Duplicate change events (at-least-once Debezium after restarts) can corrupt results: set `table.exec.source.cdc-events-duplicate = true` with a PRIMARY KEY so Flink deduplicates (adds a stateful normalize operator).
- Metadata (Kafka connector only, read-only VIRTUAL columns): e.g. `event_time TIMESTAMP(3) METADATA FROM 'value.source.timestamp' VIRTUAL`, also `value.ingestion-timestamp`, `value.source.database`, `value.source.table`.

Avro variant: `debezium-avro-confluent` with the required `debezium-avro-confluent.url` option.

## Avro with Confluent Schema Registry
```sql
'format' = 'avro-confluent',
'avro-confluent.url' = 'https://sr:8081'
-- optional auth: avro-confluent.basic-auth.credentials-source and avro-confluent.basic-auth.user-info
```
For Avro in both key and value use `key.format` and `value.format` = `avro-confluent`, with `key.avro-confluent.url`, `value.avro-confluent.url`, `key.fields` and `'value.fields-include' = 'EXCEPT_KEY'`. Schema evolution of a Kafka key is almost never compatible because of hash partitioning. The format works only with the Kafka and Upsert Kafka connectors.
Writing: the Avro schema is inferred from the table schema. The `kafka` and `upsert-kafka` connectors use `<topic_name>-value` (or `-key`) as the default subject; override it with `avro-confluent.subject`.

## Writing changelogs
- Use `upsert-kafka` (requires a PRIMARY KEY), or the `debezium-json` format on a Kafka sink to emit a Debezium-style changelog.
- Flink cannot combine UPDATE_BEFORE and UPDATE_AFTER into one message, so the Debezium formats encode them as DELETE and INSERT messages.

## Gotchas
- Postgres: set the monitored table's `REPLICA IDENTITY` to FULL (`ALTER TABLE <table> REPLICA IDENTITY FULL`); with the default, Flink SQL currently fails to interpret the Debezium data.
- Avro reading: the writer schema comes from the Schema Registry by the schema id in each record; the reader schema is inferred from the table schema.

## Verify
- [ ] An update and delete in the source DB reflect correctly in a downstream aggregate.

## Checked

2026-10-31. Confirmed against the Flink stable Debezium and Confluent Avro format pages: option names and defaults, `table.exec.source.cdc-events-duplicate` with a PRIMARY KEY, Kafka-only format metadata keys, REPLICA IDENTITY FULL requirement, default subject names, UPDATE_BEFORE/AFTER encoded as DELETE/INSERT. Removed: canal/maxwell/ogg format list, `op_ts` metadata, decimal-handling and schema-evolution advice, the planner error text, upsert-kafka tombstone detail, the EXPLAIN CHANGELOG_MODE check.

Method: documentation only; no commands were run.
