---
id: computing-software.database-administration.cockroachdb.query-performance-best-practices
name: query-performance-best-practices
category: computing-software
field: database-administration
product: cockroachdb
tags: [performance-best-practices, multi-row-dml, unique-ids, disallow-full-table-scans, bulk-insert]
level: practitioner
status: docs-checked
description: "Apply CockroachDB SQL performance practices: multi-row DML, TRUNCATE and batch deletes, unique ID choices, AS OF SYSTEM TIME, full-scan guards and row limits."
sources:
  - https://www.cockroachlabs.com/docs/stable/performance-best-practices-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: shape workloads so a distributed SQL cluster scales instead of contending.

DML and bulk work:
- Prefer one multi-row `INSERT`, `UPSERT` or `DELETE` over many single-row statements; find a good batch size experimentally (10, 100, 1000 rows). Very large multi-row inserts become long transactions; if you see `40001` with `transaction deadline exceeded`, split them. `IMPORT INTO` loads CSV into an existing table.
- Use `UPSERT` rather than `INSERT ... ON CONFLICT` on tables with no secondary indexes.
- `TRUNCATE` beats `DELETE` for emptying a table. For large partial deletes, delete in iterative batches; for expiring data use row-level TTL.
- Column families help when frequently updated columns share a row with rarely updated ones.

Unique IDs (best to worst performance): multi-column primary keys (needs design, for example `(username, post_timestamp)` where the leading column is well distributed); ID functions (`gen_random_uuid()` gives a `UUID`, `uuid_v4()` gives `BYTES`, `unique_rowid()` gives an `INT`); `INSERT ... RETURNING` with a sequence-like value (slower, more contention). Monotonic `INT` or `SERIAL` keys create read and write hotspots; use hash-sharded indexes if sequential keys are unavoidable.

Guardrails:
- `AS OF SYSTEM TIME` lets long analytical reads avoid conflicts with writers, at the cost of stale data.
- Session setting `disallow_full_table_scans` blocks plans that fully scan tables larger than `large_full_scan_rows`; index hints can prevent full scans.
- `transaction_rows_read_err` and `transaction_rows_written_err` fail transactions that touch too many rows, e.g. `ALTER ROLE ALL SET transaction_rows_read_err = 1000;`.

Contention occurs when concurrent transactions hit the same index key values and at least one holds a write intent or exclusive locking read (`SELECT ... FOR UPDATE`). Symptoms: query delays, automatic retries, client-visible retry errors, hotspots.

## Checked

2026-11-03. Confirmed against the performance best practices page: multi-row DML and batch sizes, `40001` with `transaction deadline exceeded`, UPSERT versus INSERT ON CONFLICT, TRUNCATE, unique ID options and their order, hotspots, `disallow_full_table_scans`, `large_full_scan_rows`, row-limit settings, contention. Removed: invented DB Console verification.
Method: documentation only; no commands were run.
