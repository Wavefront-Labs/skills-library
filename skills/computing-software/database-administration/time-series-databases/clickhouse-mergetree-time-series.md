---
id: computing-software.database-administration.time-series-databases.clickhouse-mergetree-time-series
name: clickhouse-mergetree-time-series
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-clickhouse, clickhouse-mergetree-time-series, clickhouse]
level: practitioner
status: draft
description: "Model time-series data in ClickHouse with a good sorting key and partitioning."
sources:
  - https://clickhouse.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MergeTree for time series

**Goal:** Model time-series data in ClickHouse with a good sorting key and partitioning.

## Steps
```
CREATE TABLE metrics (ts DateTime64(3) CODEC(DoubleDelta, ZSTD), series_id UInt64, value Float64 CODEC(Gorilla, ZSTD))
ENGINE = MergeTree PARTITION BY toYYYYMM(ts) ORDER BY (series_id, ts);
```
- `ORDER BY` is the sparse primary index; put low-cardinality or filter columns first, then time.
- Partition by month or day; avoid fine partitions (parts count limit).
- `LowCardinality(String)` for repeated labels; `Map` or `JSON` for rare tags.
- Insert in batches of at least 10,000 rows (ideally 100k+), not row by row, or use async inserts.
- Fill gaps: `ORDER BY ts WITH FILL STEP INTERVAL 1 MINUTE`.
- Downsample on read: `toStartOfInterval(ts, INTERVAL 5 MINUTE)`.

**Gotcha:** Too many small inserts create too many parts and trigger "too many parts" errors.

## Verify
- `system.parts` shows a moderate part count per partition.
- Per-series queries read few granules (check `EXPLAIN indexes = 1`).
