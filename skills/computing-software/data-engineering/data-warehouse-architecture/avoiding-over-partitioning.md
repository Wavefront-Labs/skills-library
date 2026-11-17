---
id: computing-software.data-engineering.data-warehouse-architecture.avoiding-over-partitioning
name: avoiding-over-partitioning
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, partitioning, over-partitioning, hive-style-partitions, small-files, partition-granularity, clustering]
level: practitioner
status: verified
description: "Size Hive-style and table-format partitions correctly: target partition sizes, symptoms of over-partitioning, coarsening granularity, and clustering instead of more partitions."
sources:
  - https://docs.databricks.com/aws/en/tables/partitions
  - https://docs.cloud.google.com/bigquery/quotas
  - https://docs.cloud.google.com/bigquery/docs/clustered-tables
  - https://iceberg.apache.org/docs/latest/spark-ddl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Avoiding over-partitioning

**Goal:** partitions large enough to keep files healthy and metadata small, while still pruning the common queries.

## Symptoms
- Thousands to millions of partition directories (`dt=.../hour=.../customer=...`).
- Average file size in KB-low MB; listing or planning takes longer than reading.
- Metastore/catalog slow (`MSCK REPAIR` takes hours, Glue partition limits, BigQuery 10,000-partitions-per-partitioned-table quota).
- Writes create one file per partition per task: a job writing 500 partitions x 200 tasks = 100k files.

## Rules of thumb
- Each partition should hold at least ~1 GB (Databricks guidance, which also says to prefer liquid clustering over partitioning above 1 TB), ideally several files of 128 MB-1 GB.
- Partition only by low-cardinality columns that appear in most filters: usually a date. Never by high-cardinality ids (customer_id, user_id).
- Total partitions in the low thousands, not millions.
- Small tables (< 1 TB on Databricks: its guidance is not to partition; or a few GB anywhere) often need no partitioning at all.

## Choosing granularity
| Daily volume | Granularity |
|---|---|
| < 1 GB/day | month (or none + clustering) |
| 1-100 GB/day | day |
| > 100 GB/day and hour-level queries | hour (or day + clustering on ts) |

## Use clustering for the second dimension
Instead of `PARTITIONED BY (dt, country, customer_id)`:
- Delta: liquid clustering `CLUSTER BY (country, customer_id)` (no physical partitions needed; it cannot be combined with partitioning or ZORDER on the same table) or partition by dt + `OPTIMIZE ZORDER BY (customer_id)`.
- Iceberg: partition `days(ts)` + table sort order `country, customer_id`, or `bucket(16, customer_id)` partition transform for joins/point lookups.
- BigQuery: partition by date + cluster by up to four columns (per BigQuery docs).
- Snowflake: no user partitions; clustering keys on large tables.

## Fixing an over-partitioned table
1. Create a new table with coarser partitioning / clustering.
2. Rewrite data (`INSERT INTO new SELECT * FROM old` or `CREATE TABLE AS`), compacting files.
3. Swap names/views; update writers to the new spec.
Iceberg supports **partition evolution** (`ALTER TABLE ... REPLACE PARTITION FIELD hour(ts) WITH day(ts)` (the Iceberg Spark docs use `REPLACE PARTITION FIELD ts_day WITH day(ts)`; plural `days(ts)` is the older, still supported spelling; not run here, no Spark)) without rewriting old data; new data uses the new spec, and rewrite old data later via compaction.

## Gotchas
- Filters on derived values (`where to_date(ts) = ...`) do not prune partitions on `dt` unless the engine maps them (Iceberg hidden partitioning does; Hive-style does not).
- Streaming writers with short triggers multiply small files; combine coarse partitions with compaction.

## Verify
- [ ] Partition count and average file size per partition reported for top tables.
- [ ] Typical queries still prune (bytes scanned) after coarsening + clustering.
