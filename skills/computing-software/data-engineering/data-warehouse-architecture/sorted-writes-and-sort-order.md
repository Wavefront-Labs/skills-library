---
id: computing-software.data-engineering.data-warehouse-architecture.sorted-writes-and-sort-order
name: sorted-writes-and-sort-order
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, sort-order, data-skipping, z-order, file-layout]
level: advanced
status: verified
description: "Lay out files with sorted writes for data skipping: Iceberg sort orders, Delta Z-order and liquid clustering, Parquet min/max stats, choosing sort columns and measuring."
sources:
  - https://iceberg.apache.org/docs/latest/spark-ddl/
  - https://iceberg.apache.org/docs/latest/spark-procedures/
  - https://docs.delta.io/latest/delta-clustering.html
  - https://docs.databricks.com/aws/en/delta/data-skipping
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sorted writes and sort order

**Goal:** queries filtering on common columns read a small fraction of files because min/max statistics are tight.

## Why sorting matters
Engines prune files/row groups using per-column min/max stats. If values are randomly spread, every file covers the full range and nothing is skipped. Sorting (or clustering) by filter columns makes ranges narrow. Local check (pyarrow 26, 20 Parquet files of 10,000 random user_ids from 0-99,999): a filter `user_id = 4242` could not skip any file when the data was unsorted (20 of 20 files' min/max ranges contained it), and read 1 of 20 after sorting.

## Iceberg
Spark SQL with an Iceberg catalog named `lake` (these statements come from the Iceberg Spark DDL/procedures docs; not run here, no Spark):
```sql
ALTER TABLE lake.db.events WRITE ORDERED BY event_type, user_id;     -- global order across tasks, table sort order used by writers
ALTER TABLE lake.db.events WRITE LOCALLY ORDERED BY user_id;         -- sort within tasks only (cheaper)
CALL lake.system.rewrite_data_files(table => 'db.events', strategy => 'sort',
     sort_order => 'zorder(user_id, device_id)');   -- table is relative to the catalog; hilbert(...) also exists, but cannot be mixed with zorder or plain columns
```

## Delta / Databricks
- Liquid clustering: `ALTER TABLE events CLUSTER BY (event_type, user_id)` (also `CLUSTER BY` at CREATE); `OPTIMIZE events` applies it incrementally. Up to 4 clustering columns in the Delta docs, keys need statistics, and it is not compatible with partitioning or ZORDER on the same table. Databricks recommends it over Z-order on Runtime 13.3+.
- Z-order (older): `OPTIMIZE events ZORDER BY (user_id)` on top of partitioning.
- Stats columns: by default the first 32 columns have statistics; ensure filter columns are within `delta.dataSkippingNumIndexedCols` or listed in `delta.dataSkippingStatsColumns` (Databricks Runtime 13.3+, supersedes the former).

## Choosing columns
- Columns used in selective equality/range filters and join keys; low-to-medium cardinality first for linear sorts (`event_type`, then `user_id`).
- Multi-dimensional filters with no dominant column: Z-order/Hilbert or liquid clustering.
- Time: usually partition or cluster by date; sort within by the next most-filtered column.
- Do not sort by high-entropy columns nobody filters on.

## Warehouses
Snowflake clustering keys, BigQuery clustering, Redshift sort keys implement the same idea; see platform-specific skills.

## Measure
Compare files/bytes scanned for representative queries before and after (Spark UI "files read", Databricks query profile "files pruned", Iceberg scan metrics, Trino `EXPLAIN ANALYZE`).

## Gotchas
- Sorting costs write time (shuffle); local sort is a cheaper middle ground.
- Appends of unsorted data degrade layout: schedule incremental compaction/clustering.

## Verify
Representative filtered query reads far fewer files/bytes after sorting/clustering (the local test above went from 20 files to 1); set your own target from a before/after measurement.
