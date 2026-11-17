---
id: computing-software.data-engineering.snowflake.external-tables
name: external-tables
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, external-tables, data-lake-query, partition-columns, auto-refresh, metadata-filename, delta-external-table, query-in-place]
level: practitioner
status: docs-checked
description: "Query data lake files from Snowflake with external tables: VALUE and virtual columns, partitions from paths, auto-refresh, performance limits, and when Iceberg is better."
sources:
  - https://docs.snowflake.com/en/user-guide/tables-external-intro
  - https://docs.snowflake.com/en/sql-reference/sql/create-external-table
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External tables

**Goal:** query Parquet/CSV/JSON files in S3/GCS/Azure from Snowflake without loading them, with partition pruning.

## Create
```sql
create or replace external table raw.ext_clicks (
    event_date date as to_date(split_part(metadata$filename, '/', 3), 'YYYY-MM-DD'),   -- from path .../clicks/2026-10-15/...
    user_id varchar as (value:user_id::varchar),
    url varchar as (value:url::varchar),
    ts timestamp_ntz as (value:ts::timestamp_ntz)
)
partition by (event_date)
location = @raw.landing.lake_stage/clicks/
file_format = (type = parquet)
auto_refresh = true;
```
- Every external table has a `VALUE` VARIANT column with the row; typed columns are virtual expressions over it.
- Partition columns must be derived from `metadata$filename` (the path); filters on them prune files.
- `auto_refresh = true` registers new files from cloud storage event notifications; otherwise run `alter external table raw.ext_clicks refresh;`.

## Performance reality
- Not supported for external tables: clustering keys, cloning, XML data and Time Travel. Fine for occasional queries, exploration, and staging into native tables.
- For heavily queried lake data: materialized views over external tables (Enterprise Edition), or Iceberg tables.
- Delta Lake: `TABLE_FORMAT = DELTA` is a CREATE EXTERNAL TABLE option; check the external tables pages for its current status and Snowflake's Iceberg alternatives.

## Verify
- [ ] Query with a partition filter scans only matching files (profile: partitions scanned).
- [ ] New files appear in query results after the notification (check `information_schema.external_table_files`).

## Checked

2026-10-28: reviewed against the Snowflake documentation fetched this batch.

Confirmed: VALUE VARIANT column and METADATA$FILENAME virtual columns, AUTO_REFRESH, TABLE_FORMAT = DELTA option, unsupported features (clustering keys, cloning, XML, Time Travel), materialized views over external tables need Enterprise, information_schema.EXTERNAL_TABLE_FILES (create-external-table and tables-external-intro pages).

Removed or corrected: the 'now steers to Iceberg' claim, notification-channel and serverless-cost wording, and the 'full performance' claim (not on the pages read).

Method: documentation only; no commands were run.
