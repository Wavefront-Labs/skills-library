---
id: computing-software.database-administration.duckdb.duckdb-concurrency-and-persistence
name: duckdb-concurrency-and-persistence
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, concurrency, mvcc, read-only, in-memory, persistence, transaction-conflict]
level: practitioner
status: docs-checked
description: "DuckDB connection modes and concurrency rules: persistent vs :memory:, one writer process or many read-only, optimistic conflicts, multi-process write patterns."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/connect/concurrency.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/connect/overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right open mode and avoid write conflicts when several threads or processes touch one database.

Connecting: pass a file path (for example `my_database.duckdb`) for a persistent database; the file may be new or existing, with any extension (`.db`, `.duckdb`, sometimes `.ddb`). Pass `:memory:` or omit the path for in-memory mode, where all data is lost when the process ends. Both modes spill to disk for larger-than-memory work. Since v0.10 the storage format is backward compatible: newer versions read files from older ones.

Concurrency models (choose one):
1. One process reads and writes. Inside it, multiple writer threads work through MVCC plus optimistic concurrency control.
2. Many processes read, none write: open with `access_mode = 'READ_ONLY'`.
Cross-process writing is not supported automatically.

Inside one process:
- Appends never conflict, even on the same table.
- Threads can update different tables, or different subsets of one table, concurrently.
- Two threads editing (update or delete) the same row at once: the second fails with `Transaction conflict: cannot update a table that has been altered!`. Workaround: rerun the transaction.

If several processes must write to one file, build it in application logic:
- a cross-process mutex: lock, open read/write, run, close, unlock;
- or retry the connection when another process holds it, always closing after the query;
- or run multi-process transactions in MySQL, PostgreSQL or SQLite and query periodically from DuckDB through its mysql, postgres or sqlite extensions;
- or write Parquet/CSV files and read them with multi-file reads;
- or front DuckDB with a web server that serializes reads and writes.

Design note: DuckDB is optimized for bulk operations; many small transactions are not a design goal. Keeping one process lets it cache data, the catalog and function pointers across queries on a connection.

## Checked

2026-11-07. Read the Concurrency and Connect pages in full and confirmed the two concurrency options, MVCC with optimistic concurrency, append and update rules, the conflict error text and rerun workaround, the multi-process patterns, file extensions, `:memory:`, spilling, and backward compatibility since v0.10. Removed the Verify step, which the pages do not state.

Method: documentation only; no commands were run.
