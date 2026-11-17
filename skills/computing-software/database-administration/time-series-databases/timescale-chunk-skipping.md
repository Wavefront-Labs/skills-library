---
id: computing-software.database-administration.time-series-databases.timescale-chunk-skipping
name: timescale-chunk-skipping
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-reorder, timescale-chunk-skipping, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Ensure queries exclude chunks that cannot match."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chunk exclusion and skipping

**Goal:** Ensure queries exclude chunks that cannot match.

## Steps
- Queries that filter on the partitioning (time) column only access the chunks needed, for example one day's chunk for a query on a single day. Always include a bounded time range in `WHERE`.
- Chunk skipping extends this to non-partitioning columns. It is marked experimental and needs TimescaleDB 2.17.1 or later. It is off by default: set `timescaledb.enable_chunk_skipping = on` in `postgresql.conf`.
- Enable it per column on a hypertable with compression/columnstore: `SELECT enable_chunk_skipping('conditions', 'device_id');`. Remove with `disable_chunk_skipping`.
- It tracks min and max per chunk (in the `chunk_column_stats` catalog table) for `smallint`, `int`, `bigint`, `serial`, `bigserial`, `date`, `timestamp` and `timestamptz` columns, and applies only to chunks compressed after you enable it. `decompress_chunk` resets that chunk's entry.
- Best columns are correlated with the partitioning column and appear in `WHERE` ranges (for example an insert timestamp or a sequential id).
- Run `ANALYZE` so the planner has current statistics.
- Check with `EXPLAIN` that only the expected chunks are scanned.

**Gotcha:** Chunk skipping only works on chunks converted to the columnstore after you call `enable_chunk_skipping`; recompress older chunks (after an upgrade from a version without it) for them to benefit.

## Verify
- `EXPLAIN` lists only chunks in the range.
- Query time scales with window size, not table size.

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/hypertable/enable_chunk_skipping, use-timescale/hypertables/improve-query-performance. Removed: the claims about runtime exclusion for `now()`, wrapping the time column in functions, and subqueries blocking exclusion, and the unconfirmed 2.16 version (the docs say 2.17.1, early access).

Method: documentation only; no commands were run.
