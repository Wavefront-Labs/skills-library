---
id: computing-software.database-administration.time-series-databases.influxdb3-parquet-object-storage
name: influxdb3-parquet-object-storage
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-v3, influxdb3-parquet-object-storage, influxdb, flux]
level: practitioner
status: docs-checked
description: "Understand how InfluxDB 3 stores data so you can size, retain and back it up correctly."
sources:
  - https://docs.influxdata.com/influxdb3/core/reference/internals/durability/
  - https://docs.influxdata.com/influxdb3/core/reference/config-options/
  - https://docs.influxdata.com/influxdb3/core/reference/internals/data-retention/
  - https://docs.influxdata.com/influxdb3/core/admin/backup-restore/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InfluxDB 3 Parquet and object storage

**Goal:** Understand how InfluxDB 3 stores data so you can size, retain and back it up correctly.

## Steps
- The write buffer is flushed to the write-ahead log (WAL) in the object store every second by default, then the data moves to a queryable buffer. By default the server keeps up to 900 WAL files (15 minutes of data) buffered.
- Every ten minutes by default, the oldest data is persisted to Parquet files in the object store, keeping the most recent 5 minutes in memory.
- `--object-store` accepts `memory`, `memory-throttled`, `file` (also set `--data-dir`), `s3`, `google` and `azure`.
- Start a node: `influxdb3 serve --node-id node0 --object-store file --data-dir ./data`.
- Retention is set per database: `influxdb3 create database --retention-period 30d DATABASE_NAME` (`none` for no expiry).
- Backups are object-store level; see the backup-restore page for the supported procedure.

**Gotcha:** In Core, with the default settings queries can access up to 72 hours of data (see the `gen1-duration` and file-count options), so check the limits before promising dashboards on long ranges.

## Verify
- Parquet files appear in the object store after the persist interval.
- A restart replays the WAL with no data loss.

## Checked

2026-11-03. Confirmed in the InfluxDB 3 Core durability page (WAL flush interval, 900 WAL files, ten-minute Parquet persistence), the config-options page (`--object-store` values, `--node-id`, `--data-dir`, the 72-hour query window) and the data-retention page (`--retention-period`). Removed: the edition comparison, the compaction claim, the table-level retention claim and the cardinality remark.
Method: documentation only; no commands were run.

