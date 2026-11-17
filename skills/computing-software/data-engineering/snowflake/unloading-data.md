---
id: computing-software.data-engineering.snowflake.unloading-data
name: unloading-data
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, unload-data, copy-into-location, partition-by, max-file-size, single-file, header, parquet-export, data-export, overwrite]
level: practitioner
status: docs-checked
description: "Export data from Snowflake with COPY INTO @stage: Parquet/CSV formats, PARTITION BY paths, MAX_FILE_SIZE and SINGLE, headers, overwrite behaviour, and secure delivery to partners."
sources:
  - https://docs.snowflake.com/en/sql-reference/sql/copy-into-location
  - https://docs.snowflake.com/en/user-guide/data-unload-considerations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unloading data (COPY INTO location)

**Goal:** produce well-structured export files in cloud storage for downstream systems, partners or archives.

## Parquet export, partitioned
```sql
copy into @exports.partner_stage/orders/
from (select order_id, customer_id, amount, ordered_at, to_date(ordered_at) as order_date
      from analytics.fct_orders where ordered_at >= dateadd(day, -1, current_date))
partition by ('order_date=' || to_varchar(order_date, 'YYYY-MM-DD'))
file_format = (type = parquet)
header = true                       -- keeps real column names in Parquet
max_file_size = 268435456           -- ~256 MB target per file
overwrite = false;
```
- `partition by` expression builds Hive-style subfolders.
- Unloads run in parallel and write multiple files; each file name gets a unique suffix such as `data_0_1_0`.
- `header = true` includes the table column headings in the output files.

## CSV for legacy consumers
```sql
copy into @exports.partner_stage/daily/orders_2026-10-15.csv.gz
from analytics.fct_orders_daily
file_format = (type = csv compression = gzip field_optionally_enclosed_by = '"' null_if = ())
header = true single = true max_file_size = 5368709120;    -- single file up to 5 GB
```
`single = true` writes one file at the potential cost of performance; the maximum file size is 5 GB on S3, GCS and Azure stages. Prefer multiple files unless the consumer truly needs one.

## Overwrite and idempotency
- `overwrite = true` replaces existing files with matching names; files from previous runs with different names remain and give duplicates. Unload to a run-specific path (`.../run_id=<id>/`) and publish a manifest or `_SUCCESS` marker for consumers.
- Unloads are not transactional with respect to readers: consumers may see partial output; markers solve this.
- `include_query_id = true` adds the query id to file names for uniqueness.

## Delivery options
- Partner-owned bucket via a storage integration with write permission to that prefix only.
- If the partner also uses Snowflake: **secure data sharing** instead of files (no copies).

## Verify
- [ ] File count/size per partition reasonable; row count of exported data equals the source query count (COPY result row count).
- [ ] Consumer reads the `_SUCCESS`-marked folder only.

## Checked

2026-10-28: reviewed against the Snowflake documentation fetched this batch.

Confirmed: COPY INTO <location> syntax (PARTITION BY, HEADER, OVERWRITE, SINGLE, MAX_FILE_SIZE, INCLUDE_QUERY_ID), 16 MB default and 5 GB maximum file size, unique file-name suffix such as data_0_1_0, duplicates when names differ between runs (copy-into-location and data-unload-considerations pages).

Removed or corrected: the data_<n>_<n>_<n>.snappy.parquet name pattern, the _COL_0 claim, the 'deletes same prefix' wording, the encryption bullet and the stage-count verify query.

Method: documentation only; no commands were run.
