---
id: computing-software.database-administration.postgresql.timescaledb-hypertables-and-compression
name: timescaledb-hypertables-and-compression
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, timescaledb, hypertables, chunks, columnstore-compression, retention-policy, continuous-aggregates, time-series]
level: practitioner
status: gated
description: "Run TimescaleDB on PostgreSQL: create hypertables, size chunks, enable compression and retention policies, continuous aggregates and safe upgrades."
sources:
  - https://docs.timescale.com/
  - https://docs.timescale.com/use-timescale/latest/hypertables/
  - https://docs.timescale.com/use-timescale/latest/compression/
  - https://docs.timescale.com/self-hosted/latest/upgrades/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TimescaleDB hypertables and compression

## Install
```ini
shared_preload_libraries = 'timescaledb'     # restart
```
```sql
CREATE EXTENSION timescaledb;
SELECT extversion FROM pg_extension WHERE extname = 'timescaledb';
```
`timescaledb-tune` suggests memory/worker settings. License note: compression, continuous aggregates and policies are in the Timescale License (TSL) build, not the Apache-only build some distributions ship.

## Hypertable
```sql
CREATE TABLE metrics (time timestamptz NOT NULL, device_id int, value double precision);
SELECT create_hypertable('metrics', by_range('time', INTERVAL '1 day'));   -- 2.13+ syntax
CREATE INDEX ON metrics (device_id, time DESC);
```
Chunk size: aim for recent chunks (all their indexes) to fit in ~25% of memory. Change for future chunks with `set_chunk_time_interval('metrics', INTERVAL '6 hours')`.

## Compression (columnstore)
```sql
ALTER TABLE metrics SET (timescaledb.compress, timescaledb.compress_segmentby = 'device_id', timescaledb.compress_orderby = 'time DESC');
SELECT add_compression_policy('metrics', INTERVAL '7 days');
SELECT pg_size_pretty(before_compression_total_bytes), pg_size_pretty(after_compression_total_bytes)
FROM hypertable_compression_stats('metrics');
```
`segmentby` = column you filter by (device/tenant); bad choice (high cardinality like a UUID per row) gives poor ratios. Updates/deletes on compressed chunks work in 2.11+ but are slower; compress only data that is settled.

## Retention and aggregates
```sql
SELECT add_retention_policy('metrics', INTERVAL '90 days');      -- drops whole chunks: instant, no bloat
CREATE MATERIALIZED VIEW metrics_hourly WITH (timescaledb.continuous) AS
  SELECT time_bucket('1 hour', time) AS bucket, device_id, avg(value) FROM metrics GROUP BY 1, 2;
SELECT add_continuous_aggregate_policy('metrics_hourly', start_offset => INTERVAL '3 days', end_offset => INTERVAL '1 hour', schedule_interval => INTERVAL '30 min');
SELECT * FROM timescaledb_information.jobs; SELECT * FROM timescaledb_information.job_stats;
```

## Upgrades
```sql
-- after installing the new package; first command in a fresh session
ALTER EXTENSION timescaledb UPDATE;
```
Use `psql -X` (no psqlrc) for the update. Before a PostgreSQL major upgrade, ensure the TimescaleDB version you run is available for both majors.

## Gotchas
- `pg_dump` of hypertables works but restore needs `timescaledb_pre_restore()` / `timescaledb_post_restore()`.
- Too many tiny chunks (interval too small) slow planning; check `SELECT count(*) FROM show_chunks('metrics');`.
- Background jobs need `timescaledb.max_background_workers` sized to the number of databases plus jobs.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; Timescale docs landing pages only; function and view names (create_hypertable, compression policies, stats views) not found on them. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
