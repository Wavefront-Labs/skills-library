---
id: computing-software.database-administration.time-series-databases.timescale-chunk-interval
name: timescale-chunk-interval
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-hypertables, timescale-chunk-interval, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Choose a chunk interval so recent chunks and their indexes fit in memory."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chunk interval sizing

**Goal:** Choose a chunk interval so recent chunks and their indexes fit in memory.

## Steps
- Rule of thumb from the docs: the chunks currently being ingested into, with their indexes, should fit within 25 percent of main memory.
- By default each chunk holds 7 days of data.
- Set it at creation with `tsdb.chunk_interval='1 day'` in `CREATE TABLE ... WITH (tsdb.hypertable, ...)`, or change it later: `SELECT set_chunk_time_interval('conditions', INTERVAL '24 hours');`.
- For `TIMESTAMP`, `TIMESTAMPTZ` and `DATE` columns an integer interval is in microseconds; `SMALLINT`, `INT` and `BIGINT` time columns use the column's own unit.
- Too many small, sparsely filled chunks slow query planning and hurt compression.
- Check the current setting in `timescaledb_information.dimensions` (`time_interval`) and sizes with `SELECT chunk_name, pg_size_pretty(total_bytes) FROM chunks_detailed_size('conditions');` (columns `table_bytes`, `index_bytes`, `toast_bytes`, `total_bytes`).

**Gotcha:** The new interval applies to new chunks only; existing chunks keep their width, and a transition chunk can be shorter than the new interval. If you set an overly long interval (the docs example is 1 year) and insert data, you cannot shorten those chunks: create a new hypertable and migrate.

## Verify
- Active chunk plus indexes is within about a quarter of RAM.
- `timescaledb_information.dimensions` shows the interval you set.

## Checked

Checked 2026-11-03 against the timescale/docs repository: _partials/_chunk-interval (25 percent of main memory), use-timescale/hypertables/index and improve-query-performance, api/hypertable/set_chunk_time_interval, chunks_detailed_size. Removed: the 'thousands OK, hundreds of thousands not' planning figures and the 1 hour / 1 day ingest advice, which are not in these pages.

Method: documentation only; no commands were run.
