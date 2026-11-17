---
id: computing-software.database-administration.time-series-databases.timescale-compression-segmentby
name: timescale-compression-segmentby
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-compression, timescale-compression-segmentby, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Configure native compression so queries on a segment stay fast and ratio is high."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compression segmentby and orderby

**Goal:** Configure native compression so queries on a segment stay fast and ratio is high.

## Steps
```sql
ALTER TABLE conditions SET (timescaledb.compress,
  timescaledb.compress_segmentby = 'device_id',
  timescaledb.compress_orderby = 'time DESC');
```
- Newer releases use the columnstore form: `ALTER TABLE conditions SET (timescaledb.enable_columnstore, timescaledb.orderby = 'time DESC', timescaledb.segmentby = 'device_id');`.
- This alone does not compress anything: add a compression policy or call `compress_chunk`.
- `segmentby`: an identifier such as `device_id` that you filter or group by; the default is no segmentby columns. Lower-cardinality segmentby columns give better compression.
- `orderby`: defaults to the descending time column; ordering has a large effect on ratio and query performance. Delta, delta-of-delta, simple-8b and run-length encodings are used for integer-like and timestamp data.
- Batches hold up to 1000 rows per segment; a chunk without enough rows per segment to fill batches gets a lower ratio.

**Gotcha:** A unique or near-unique segmentby column (like a uuid) leaves each segment with too few rows to form batches, which hurts compression and query performance.

## Verify
- `SELECT * FROM hypertable_compression_stats('conditions');` shows before and after sizes.
- Queries filtering on the segmentby column stay fast.

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/compression/alter_table_compression, api/hypercore/alter_table, use-timescale/hypercore/secondary-indexes and real-time-analytics-in-hypercore, _partials/_hypercore-direct-compress, api/compression/hypertable_compression_stats. Removed: the 'about 100 rows per chunk' threshold and the '90 percent size reduction' figure, which are not in the docs.

Method: documentation only; no commands were run.
