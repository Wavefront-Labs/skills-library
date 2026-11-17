---
id: computing-software.data-engineering.apache-flink.watermarks-in-flink-sql
name: watermarks-in-flink-sql
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink-sql, sql-watermark, watermark-for, rowtime, idle-timeout, timestamp-ltz, event-time]
level: practitioner
status: docs-checked
description: "Declare event time in Flink SQL: WATERMARK FOR in CREATE TABLE, TIMESTAMP vs TIMESTAMP_LTZ rowtime, computed columns from epoch fields, source idle timeout and alignment options."
sources:
  - https://raw.githubusercontent.com/apache/flink/release-2.4/docs/content/docs/sql/reference/ddl/create.md
  - https://raw.githubusercontent.com/apache/flink/release-2.4/docs/content/docs/concepts/sql-table-concepts/time_attributes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Watermarks in Flink SQL

**Goal:** a table's event-time attribute is declared so windows and other time-based operations work and fire on time.

## DDL
```sql
CREATE TABLE user_actions (
  user_name STRING,
  data STRING,
  ts BIGINT,
  time_ltz AS TO_TIMESTAMP_LTZ(ts, 3),                         -- computed column from epoch ms
  WATERMARK FOR time_ltz AS time_ltz - INTERVAL '5' SECOND     -- bounded out-of-orderness
) WITH ( ... );
```
- `WATERMARK FOR rowtime_column AS expression` marks the column as the event time attribute. The expression may be any non-query expression, including computed columns, and must return TIMESTAMP(3). It is evaluated for every record.
- Event time can be defined on a TIMESTAMP or TIMESTAMP_LTZ column. The time attributes page recommends TIMESTAMP for zone-less date-time values (e.g. `2020-04-15 20:13:40.564`) and TIMESTAMP_LTZ for epoch values (e.g. a long such as `1618989564564`).
- A watermark is emitted only if non-null and larger than the previous one. Emission is periodic, by default every 200 ms (`pipeline.auto-watermark-interval`); with an interval of 0ms it is per record.
- Event-time semantics need both an event time attribute and a watermark strategy.

## Strategies
- Strictly ascending: `WATERMARK FOR t AS t`.
- Ascending: `t - INTERVAL '0.001' SECOND`.
- Bounded out-of-orderness: `t - INTERVAL 'N' <unit>`, e.g. 5 seconds delayed.

## Idle sources, emit strategy and alignment (since Flink 1.18)
Only source connectors implementing `SupportsWatermarkPushDown` (e.g. Kafka, Pulsar) honour these; otherwise the job runs but the options have no effect. Set them as table options or with an `OPTIONS` hint; the hint wins if both are set.
```sql
-- global idle timeout
SET 'table.exec.source.idle-timeout' = '1 min';
-- per table (preferred over the global setting)
SELECT ... FROM source_table /*+ OPTIONS('scan.watermark.idle-timeout'='1min',
    'scan.watermark.alignment.group'='alignment-group-1',
    'scan.watermark.alignment.max-drift'='1min',
    'scan.watermark.alignment.update-interval'='1s') */;
```
- An idle split/partition would otherwise hold back the downstream watermark (the minimum of all inputs); after the timeout it is ignored.
- `scan.watermark.emit.strategy` is `on-periodic` (default) or `on-event`.
- Alignment keeps fast splits from running too far ahead (max-drift); `update-interval` defaults to 1s. Connectors must implement split alignment (FLIP-217), else the task errors; `pipeline.watermark-alignment.allow-unaligned-source-splits: true` disables split alignment, which works correctly only when splits equal source parallelism.

## Time attributes
A time attribute stays valid while it is only forwarded unchanged; when used in calculations it is materialised into a plain timestamp, and ordinary timestamps cannot be converted back to time attributes.

## Processing time
`proc_time AS PROCTIME()` (computed column, type TIMESTAMP_LTZ) declares a processing-time attribute; results are non-deterministic.

## Checked
Method: 2026-11-08 read the DDL CREATE page (watermark section) and the time attributes page from the Flink release-2.4 docs source. Dropped unsupported claims: Kafka metadata timestamp and DDL options, the 1970 wrong-unit gotcha, CDC/upsert late-update behaviour, the numLateRecordsDropped metric and lookup-join note, the DESCRIBE *ROWTIME* check, the table.local-time-zone claim and the config page citation (not read). Strategies and idle/alignment options confirmed.
