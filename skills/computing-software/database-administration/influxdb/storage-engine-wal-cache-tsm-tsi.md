---
id: computing-software.database-administration.influxdb.storage-engine-wal-cache-tsm-tsi
name: storage-engine-wal-cache-tsm-tsi
category: computing-software
field: database-administration
product: influxdb
tags: [storage-engine, wal, cache, tsm, tsi, compaction, fsync]
level: advanced
status: docs-checked
description: "How a write moves through the OSS storage engine: WAL with fsync, in-memory cache, TSM snapshots and compaction, and the TSI index for high cardinality."
sources:
  - https://docs.influxdata.com/influxdb/v2/reference/internals/storage-engine/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Write path: line protocol is POSTed to `/api/v2/write` (or the 1.x `/write` endpoint), compressed, appended to the WAL, and added to the in-memory cache, where it is immediately queryable.

WAL steps for each request: append to the WAL file, `fsync()` to disk, update the cache, then acknowledge. `fsync` is a costly syscall but guarantees durability. On restart the WAL is replayed into the cache.

Cache: points organised by series key and field, stored uncompressed, bounded by a maximum size (`maxSize`). Queries merge the cache with TSM files and run on a copy, so concurrent writes do not alter a running query. Deletes clear the key or range from the cache.

TSM (Time-Structured Merge Tree): field values grouped by series key and ordered by time, stored compressed and columnar with deltas. After a flush the WAL is truncated and the cache cleared. Compaction merges files into longer runs per series for better compression and scans.

TSI (Time Series Index): keeps queries fast as the number of series grows; answers which measurements, tags and fields exist, and which series keys exist for given ones.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 "InfluxDB storage engine" page, article body (lines 574-643) read in full from the downloaded text.

Confirmed: write path, WAL steps with `fsync()` and replay on restart, cache behaviour and `maxSize`, TSM flush, truncation and compaction goals, TSI purpose. Nothing removed.
