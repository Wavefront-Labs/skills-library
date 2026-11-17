---
id: computing-software.database-administration.time-series-databases.timescale-compressed-chunk-changes
name: timescale-compressed-chunk-changes
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-compression, timescale-compressed-chunk-changes, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Insert, update and alter schema on tables with compressed chunks safely."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Changing compressed data

**Goal:** Insert, update and alter schema on tables with compressed chunks safely.

## Steps
- You can `INSERT`, `UPDATE` and `DELETE` data in compressed (columnstore) chunks, even with unique constraints; inserting decompresses a small amount of data for a speculative insertion that blocks constraint violations.
- When deleting whole segments, filter on the `segmentby` column instead of running separate deletes; the docs say this considerably increases performance.
- For large changes or a backfill: stop the conversion job (`SELECT alter_job(<job_id>, scheduled => false);`), run `CALL convert_to_rowstore('<chunk>');`, make the change, then `CALL convert_to_columnstore('<chunk>');` and re-enable the job with `scheduled => true`.
- Schema changes on compressed hypertables (2.6 and later): add a nullable column, add a column with `NOT NULL DEFAULT`, rename a column, and drop a column that is not an `orderby` or `segmentby` column. Changing a column's data type is not supported; decompress first for unsupported operations.
- Backfill pattern: load into a staging table and `INSERT ... SELECT` in time order.

**Gotcha:** A large `UPDATE` across many compressed segments is the case the docs route through convert-to-rowstore first; do not run it directly against compressed chunks.

## Verify
- `SELECT * FROM chunk_compression_stats('conditions');` shows the chunks compressed again after the change.
- Table size returns to the pre-change level.

## Checked

Checked 2026-11-03 against the timescale/docs repository: use-timescale/hypercore/modify-data-in-hypercore, use-timescale/compression/modify-a-schema, api/compression/chunk_compression_stats. Removed: the 'uncompressed staging area' description, the unconfirmed 2.11 version gate, and the memory and WAL exhaustion claim.

Method: documentation only; no commands were run.
