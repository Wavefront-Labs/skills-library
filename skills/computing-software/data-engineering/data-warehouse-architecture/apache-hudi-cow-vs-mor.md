---
id: computing-software.data-engineering.data-warehouse-architecture.apache-hudi-cow-vs-mor
name: apache-hudi-cow-vs-mor
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, open-table-formats, apache-hudi, copy-on-write, merge-on-read, record-key, precombine, compaction, hudi-streamer, upserts]
level: practitioner
status: docs-checked
description: "Choose Apache Hudi copy-on-write or merge-on-read, set record and precombine keys, configure compaction and cleaning, and query snapshot, read-optimized and incremental views."
sources:
  - https://hudi.apache.org/docs/table_types
  - https://hudi.apache.org/docs/writing_data
  - https://hudi.apache.org/docs/compaction
  - https://hudi.apache.org/docs/sql_queries
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Apache Hudi: copy-on-write vs merge-on-read

**Goal:** pick the Hudi table type that matches your write/read balance, and configure keys and table services so upserts stay fast.

## 1. The two table types
| | Copy-on-write (COW) | Merge-on-read (MOR) |
|---|---|---|
| Update cost | rewrites the whole base Parquet file | appends to row-based log files (Avro) |
| Read cost | plain Parquet, fastest | merges base + logs at read (snapshot query) |
| Write latency | higher | low — suited to streaming upserts / CDC |
| Needs compaction | no | yes (logs → new base files) |
| Query views | snapshot, incremental | snapshot, read-optimized (base only, stale), incremental |
Rule: read-heavy, hourly/daily batch → COW. High-frequency upserts or CDC with minute latency → MOR.

## 2. Keys
- `hoodie.datasource.write.recordkey.field` — unique key (composite allowed: `order_id,line_no`).
- `hoodie.datasource.write.precombine.field` (deprecated; use `hoodie.table.ordering.fields`) — when two records share a key, the one with the larger value wins. Use the source change timestamp or LSN, never ingestion time.
- `partitionpath.field` — keep coarse (day); use a global index if keys move across partitions.

## 3. Spark write
```python
opts = {
  "hoodie.table.name": "orders",
  "hoodie.datasource.write.table.type": "MERGE_ON_READ",
  "hoodie.datasource.write.operation": "upsert",          # insert / bulk_insert / delete
  "hoodie.datasource.write.recordkey.field": "order_id",
  "hoodie.table.ordering.fields": "updated_at",
  "hoodie.datasource.write.partitionpath.field": "order_date",
  "hoodie.compact.inline": "false",
}
df.write.format("hudi").options(**opts).mode("append").save("s3://lake/orders")
```
Use `bulk_insert` for the initial historical load (no index lookup), then `upsert`.

## 4. Table services
- **Compaction** (MOR): run async (separate job / `HoodieCompactor`, or async in streaming writers) so writers aren't blocked; trigger by number of delta commits (`hoodie.compact.inline.max.delta.commits`).
- **Cleaning**: removes old file versions; the cleaner retention settings bound time travel and incremental lookback.
- **Clustering**: re-sorts / resizes files for query layout.
- **Archival** of the timeline keeps metadata small.
- Index: bloom or the record-level index in the metadata table (`hoodie.metadata.record.index.enable`) for large tables with random-key upserts.

## 5. Queries
```sql
SELECT * FROM orders;                    -- snapshot (MOR merges logs)
SELECT * FROM orders_ro;                 -- read-optimized view, base files only (registered by Hive sync)
SELECT * FROM hudi_table_changes('db.orders', 'cdc', 'earliest');  -- change feed (also accepts a start time)
```
Incremental queries give downstream jobs only records changed since a commit time — Hudi's main strength for chaining pipelines.

## Verify
- [ ] Precombine field is a source-side ordering column.
- [ ] MOR compaction lag (pending compactions on the timeline) stays bounded.
- [ ] Cleaner retention exceeds the longest incremental consumer's lookback.

## Checked

2026-10-28. Confirmed in the Hudi writing data page: `hoodie.datasource.write.precombine.field` is deprecated in favour of `hoodie.table.ordering.fields`, operations `upsert` (default), `bulk_insert`, `insert`, `delete`; compaction page: `hoodie.compact.inline.max.delta.commits`; SQL queries page: `hudi_table_changes` signature, read-optimized queries on MERGE_ON_READ, `hoodie.metadata.record.index.enable`. Removed: the default of 5, `hoodie.compact.schedule.inline`, `hoodie.cleaner.commits.retained`, the `latest_state` mode and the bloom-default claim (not found in the fetched pages).

Method: documentation only; no commands were run.
