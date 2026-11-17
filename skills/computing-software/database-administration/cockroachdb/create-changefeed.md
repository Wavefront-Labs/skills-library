---
id: computing-software.database-administration.cockroachdb.create-changefeed
name: create-changefeed
category: computing-software
field: database-administration
product: cockroachdb
tags: [change-data-capture, changefeed, create-changefeed, rangefeed, initial-scan, resolved]
level: practitioner
status: docs-checked
description: "Create CockroachDB changefeeds with CREATE CHANGEFEED: rangefeed prerequisite, sink URIs, key options, CDC queries, sinkless feeds, resuming from a cursor and job control."
sources:
  - https://www.cockroachlabs.com/docs/stable/create-changefeed
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stream row-level changes to a sink in a configurable format.

Prerequisite: enable rangefeeds with the cluster setting `kv.rangefeed.enabled`.

Forms:
```sql
CREATE CHANGEFEED FOR TABLE table_name, table_name2
  INTO 'scheme://host:port'
  WITH updated, resolved;
-- sinkless: omit INTO and the feed streams to the SQL client
CREATE CHANGEFEED FOR TABLE table_name WITH updated, resolved;
-- via an external connection
CREATE EXTERNAL CONNECTION kafka_sink AS 'kafka://...';
CREATE CHANGEFEED FOR TABLE table_name INTO 'external://kafka_sink';
```
CDC queries use `CREATE CHANGEFEED INTO '...' AS SELECT <target_list> FROM <table> WHERE <filter>` to filter and transform emitted data.

Key options (value types in parentheses): `format` (`json`, `avro`, `csv`, `parquet`, `protobuf`), `envelope` (`wrapped` default, `enriched`, `bare`, `key_only`, `row`), `initial_scan` (`yes`, `no`, `only`; only one may be used), `cursor` (emit changes after a timestamp; does not emit current table state first), `end_time` (complete as `successful` at that timestamp), `diff` (adds `before`), `updated`, `mvcc_timestamp`, `resolved` (duration), `min_checkpoint_frequency`, `compression` (`gzip`, `zstd`), `on_error` (`pause` or `fail`), `schema_change_policy` (`backfill`, `nobackfill`, `stop`), `split_column_families`, `key_column` (requires `unordered`), `kafka_sink_config`, `execution_locality`, `confluent_schema_registry`. `protect_data_from_gc_on_pause` is deprecated as of v23.2; `gc_protect_expires_after` expires protected timestamp records older than the given duration.

Manage: `SHOW CHANGEFEED JOBS;`, `PAUSE JOB`, `RESUME JOB`, `CANCEL JOB`, `ALTER CHANGEFEED`. To continue where one ended, find the last resolved timestamp via `SHOW CHANGEFEED JOB {job_id};` and create a new feed with `cursor`.

Cloud storage file layouts partition by `daily` (default), `hourly` or `flat`.

Verify: `SHOW CHANGEFEED JOBS;` shows status `running` and the sink receives rows after a test insert.

## Checked
2026-11-03. Confirmed on the CREATE CHANGEFEED page: formats, envelope values, `initial_scan` (only one of yes/no/only), `cursor` semantics, `end_time` completing as successful, `diff`, `compression` gzip/zstd, `on_error`, `key_column` requiring `unordered`, `execution_locality`, partition formats daily (default)/hourly/flat, `SHOW CHANGEFEED JOB`, and the `protect_data_from_gc_on_pause` deprecation. Corrected: the replacement-option wording.
Method: documentation only; no commands were run.
