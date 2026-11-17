---
id: computing-software.database-administration.cockroachdb.import-into
name: import-into
category: computing-software
field: database-administration
product: cockroachdb
tags: [import-into, bulk-load, csv, avro, table-offline, detached]
level: practitioner
status: docs-checked
description: "Bulk load CSV, Avro, Parquet or delimited data into an existing CockroachDB table with IMPORT INTO, and plan for the table going offline and foreign keys being invalidated."
sources:
  - https://www.cockroachlabs.com/docs/stable/import-into
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: ingest large files into an existing table quickly, knowing the side effects first.

Statement shape (from the import performance page):
```sql
IMPORT INTO customers (id, name)
CSV DATA ('<cloud-storage-url-to-customers.csv>');
```
Put files on cloud storage reachable from every node by the same location; nodes read the files in parallel.

Considerations stated on the page:
- The target table goes offline for the whole job and returns online only when the job succeeds. Queries against it fail meanwhile.
- It is blocking; add the `DETACHED` option to run asynchronously and watch the job with `SHOW JOBS`.
- It invalidates all foreign keys on the target table. Re-validate with `ALTER TABLE ... VALIDATE CONSTRAINT`.
- Insert-only: it cannot update rows, and imported rows must not conflict with the primary key or any `UNIQUE` constraint. No `SELECT` or `WHERE` subset; use `INSERT` for that.
- Any changefeed on the target table fails.
- Cannot be used during a rolling upgrade.
- Works with `REGIONAL BY ROW` tables, computed columns and some `DEFAULT` expressions: user-defined types, constant expressions (`random()`, `gen_random_uuid()`, `unique_rowid()`, `nextval()`) and transaction-timestamp functions (`now()`, `current_timestamp()`, `statement_timestamp()` and similar).
- At job start it snapshots the user-defined types the table references, including `crdb_internal_region` in multi-region clusters.

Check the job with `SHOW JOBS`; the table stays offline until it succeeds.

## Checked

2026-11-03. Confirmed against the IMPORT INTO page and the import performance page: formats, offline table, `DETACHED`, foreign key invalidation, insert-only, changefeed failure, rolling upgrade limit, supported DEFAULT expressions, type snapshot. Removed: invented validation and row-count verification.
Method: documentation only; no commands were run.
