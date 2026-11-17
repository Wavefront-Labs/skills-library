---
id: computing-software.data-engineering.databricks.copy-into-idempotent-loads
name: copy-into-idempotent-loads
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-copy-into, copy-into, idempotent-load, batch-ingestion, mergeschema, sql-warehouse, file-ingestion]
level: practitioner
status: docs-checked
description: "Load files into Delta with COPY INTO: idempotent file tracking, schemaless tables, mergeSchema, validation, force reloads, Auto Loader trade-offs."
sources:
  - https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/copy-into/
  - https://docs.databricks.com/aws/en/sql/language-manual/delta-copy-into
  - https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/copy-into/tutorial-dbsql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# COPY INTO idempotent loads (Databricks)

**Goal:** a re-runnable SQL statement that loads each new file once, from a SQL warehouse or job, with no streaming checkpoint to manage.

## 1. Basic load
```sql
CREATE TABLE IF NOT EXISTS prod.bronze.invoices;      -- schemaless placeholder; schema comes from first load

COPY INTO prod.bronze.invoices
FROM '/Volumes/prod/landing/invoices/'
FILEFORMAT = CSV
PATTERN = '2026/10/*/*.csv'
FORMAT_OPTIONS ('mergeSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');
```
- Idempotent: the target Delta table's log records which files were loaded; rerunning skips them.
- `FORMAT_OPTIONS mergeSchema` merges schemas across source files; `COPY_OPTIONS mergeSchema` evolves the target table.
- `FILES = ('a.csv','b.csv')` loads an explicit list (up to 1000 files).
- Transform during load with `FROM (SELECT expression_list FROM <source>)`; aggregations are allowed only as global aggregates (no GROUP BY). Concurrent COPY INTO calls on the same table must use distinct sets of files, and one call with many files is usually faster than many calls with one file each.

## 2. Validate before loading
```sql
COPY INTO prod.bronze.invoices FROM '/Volumes/prod/landing/invoices/'
FILEFORMAT = JSON VALIDATE 15 ROWS;        -- or VALIDATE ALL (the default); nothing is written
```

## 3. Reloads and corrections
- Already-loaded files are skipped even if they were modified since. Reload deliberately with `COPY_OPTIONS ('force' = 'true')` (default false) — this disables idempotency and can duplicate rows; delete the affected rows first or load into a staging table and MERGE.
- Credentials: reading through a Unity Catalog external location or volume needs no inline credential; `WITH (CREDENTIAL ...)` is only needed when the path is not in an external location.

## 4. COPY INTO vs Auto Loader
| | COPY INTO | Auto Loader |
|---|---|---|
| Interface | SQL statement (warehouse friendly) | Structured Streaming |
| File tracking | idempotent by default, skips loaded files | checkpoint |
| Scale | Databricks recommends Auto Loader for directories with a very large number of files | designed for large directories; notification mode |
| Schema evolution | mergeSchema | evolution modes, rescued data, hints |
| Best for | ad hoc / scheduled SQL loads, small-medium volumes | continuous or large-scale ingestion |
For SQL users who need more scalable and robust file ingestion, Databricks recommends streaming tables over COPY INTO.

## Verify
- [ ] Running the same COPY INTO twice inserts 0 rows the second time.
- [ ] `VALIDATE` run on a new feed before the first real load.
- [ ] Any `force` reload was preceded by deleting or staging the affected rows.

## Checked

2026-11-09. Confirmed on the COPY INTO SQL reference and the Get started with COPY INTO page: idempotent and retryable, skips loaded files even if modified, schemaless placeholder table with mergeSchema in COPY_OPTIONS (Runtime 11.3 LTS and above), FILES limit of 1000, PATTERN, VALIDATE with ROWS, force default false, mergeSchema default false, concurrent-call guidance, Auto Loader recommended for very large directories, streaming tables recommended for SQL users. Removed: output column names, SELECT cast and _metadata example, scale figures, RocksDB, and the streaming-table syntax (not on the pages read).

Method: documentation only; no commands were run.

