---
id: computing-software.data-engineering.snowflake.transforming-data-during-copy
name: transforming-data-during-copy
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, copy-into, copy-transformations, metadata-filename, column-reordering, variant, loading-data, snowpipe]
level: practitioner
status: docs-checked
description: "Use COPY INTO with a SELECT over the stage to reorder, cast, flatten and add file metadata columns during load, and know the transformation limits."
sources:
  - https://docs.snowflake.com/en/user-guide/data-load-transform
  - https://docs.snowflake.com/en/user-guide/querying-metadata
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transforming data during COPY

**Goal:** load files into a typed table in one step, adding lineage columns, without a separate staging table.

## Pattern
```sql
copy into raw.orders (order_id, customer_id, amount, ordered_at, src_file, src_row, loaded_at)
from (
  select
    $1:order_id::number,
    $1:customer:id::varchar,
    $1:amount::number(18,2),
    to_timestamp_ntz($1:ts::varchar, 'YYYY-MM-DD"T"HH24:MI:SS'),
    metadata$filename,
    metadata$file_row_number,
    metadata$start_scan_time
  from @raw.landing/orders/
)
file_format = (type = json strip_outer_array = true)
pattern = '.*orders_.*[.]json[.]gz'
on_error = abort_statement;
```
For CSV, refer to columns positionally (`t.$1, t.$3`) with an alias: `from @stage t`.

## Metadata columns
`metadata$filename`, `metadata$file_row_number`, `metadata$file_content_key`, `metadata$file_last_modified`, `metadata$start_scan_time`. They can only be queried by name (not via `SELECT *`). Persist filename + row number for dedup and debugging. For the load time, Snowflake recommends `metadata$start_scan_time` over a `CURRENT_TIMESTAMP` column default.

## Supported in COPY transformations
- Column reordering, omission, casts, `to_timestamp`/`to_date`, `concat`, `substr`, `nullif`, `trim`, `case`, `parse_json`, `uuid_string`, a sequence `NEXTVAL`, or omitting an `AUTOINCREMENT` column. Only a subset of functions is supported (the docs list them); scalar SQL UDFs have limited error handling.
## Not supported
- `WHERE` filters, `ORDER BY`, `LIMIT`, `FETCH`, `TOP`, `GROUP BY`, joins and `FLATTEN`; `DISTINCT` is not fully supported.
- `MATCH_BY_COLUMN_NAME` together with a transformation SELECT (error: match_by_column_name is not supported with copy transform).
- `VALIDATION_MODE` cannot be combined with transformations.
For those, load raw into a VARIANT landing table and transform with SQL/streams/dynamic tables.

## Parquet/Avro/ORC alternative
```sql
copy into raw.events
from @raw.landing/events/
file_format = (type = parquet)
match_by_column_name = case_insensitive;
```
`MATCH_BY_COLUMN_NAME` maps by name without writing a SELECT, and is often simpler than a transformation for columnar files. Add `INCLUDE_METADATA = (src_file = metadata$filename)` to capture metadata alongside it (it works only with `MATCH_BY_COLUMN_NAME`, and the target column must already exist).

## Snowpipe
Pipes accept the same `copy into ... from (select ...)` statement, so transformations work for continuous loading too.

## Gotchas
- With `on_error = continue`, rows with errors are skipped; the gap between `ROWS_PARSED` and `ROWS_LOADED` counts them. `VALIDATE` fails for a COPY that used a SELECT transformation, and ignores the SELECT list, so read `first_error_message` in `copy_history` instead.
- Load metadata is per table and expires after 64 days; `force = true` reloads every matched file and can duplicate data.

## Verify
- [ ] `select count(*), count(distinct src_file) from raw.orders where loaded_at > ...` matches files in the stage listing.
- [ ] `copy_history` shows status `Loaded` with expected row counts and zero errors.

## Checked
2026-11-09. Confirmed against Snowflake docs "Transform data during a load", "Query metadata for staged files", the COPY INTO <table> reference (INCLUDE_METADATA, MATCH_BY_COLUMN_NAME, ON_ERROR, FORCE) and the VALIDATE and COPY_HISTORY function pages: the supported/unsupported transformation list, the five metadata columns, VALIDATE failing on transformed loads, Snowpipe support, the 64-day load metadata. Removed: CURRENT_TIMESTAMP, window functions and case-sensitivity of paths (not in the pages), the file-rename reload claim, and the validate() suggestion.
Method: documentation only; no commands were run.
