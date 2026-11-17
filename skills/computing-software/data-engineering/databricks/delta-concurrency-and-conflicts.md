---
id: computing-software.data-engineering.databricks.delta-concurrency-and-conflicts
name: delta-concurrency-and-conflicts
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, delta-lake, concurrent-modification, concurrentappendexception, optimistic-concurrency, row-level-concurrency, isolation-level, write-conflicts]
level: advanced
status: docs-checked
description: "Resolve Delta Lake write conflicts (ConcurrentAppendException etc.): optimistic concurrency, row-level concurrency, disjoint MERGE predicates and safe retries."
sources:
  - https://docs.databricks.com/en/optimizations/isolation-level.html
  - https://docs.delta.io/latest/concurrency-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delta concurrency and write conflicts

**Goal:** multiple jobs writing the same Delta table (backfills + streaming + maintenance) do not fail each other.

## How Delta commits
Optimistic concurrency: each writer reads a snapshot, writes files, then tries to commit version N+1. If another commit landed in between, Delta checks whether the two conflict; if they do, the later writer gets an exception and its files are discarded.

## Conflict exceptions
Which operation pairs conflict depends on the isolation level (`WriteSerializable` is the default); see the isolation levels page for the matrix.

Exceptions:
- `ConcurrentAppendException`: files were added to the data your operation read (e.g. MERGE read partition X while another job appended to X).
- `ConcurrentDeleteReadException` / `ConcurrentDeleteDeleteException`: files you read/deleted were removed by another commit (e.g. OPTIMIZE compacted them).
- `MetadataChangedException`, `ProtocolChangedException`: schema/protocol changed concurrently.

## Fixes
1. **Make predicates disjoint and explicit.** A MERGE condition that includes the partition/clustering column lets Delta prove no overlap:
```sql
MERGE INTO sales t USING updates s
ON t.order_id = s.order_id AND t.order_date = s.order_date AND t.order_date >= '2026-10-10'
```
Without explicit predicates Delta cannot rule out overlap between concurrent writers.
2. **Row-level concurrency** (see the Databricks Row-level concurrency page for runtime and table requirements): conflicts are detected at row level. Deletion vectors are enabled with: `ALTER TABLE t SET TBLPROPERTIES ('delta.enableDeletionVectors' = true);`
3. **Schedule maintenance** (OPTIMIZE, VACUUM) away from heavy DML.
4. **Retry** idempotent operations with backoff on `ConcurrentAppendException`; MERGE/INSERT OVERWRITE with deterministic inputs are safe to retry.
5. **Isolation level:** `delta.isolationLevel = WriteSerializable` (default) allows more concurrency than `Serializable`; keep the default unless you need strict serializability.

## Streaming + batch on one table
Streaming appends rarely conflict with each other; a batch MERGE over recent partitions conflicts with streaming appends to those partitions. Route corrections into a separate table, or run the MERGE inside `foreachBatch` of the same stream.

## Diagnose
```sql
DESCRIBE HISTORY sales LIMIT 20;   -- operation, operationParameters (predicates)
```
Compare the failed job's predicates with those of the concurrent operations.

## Verify
- [ ] Concurrent test: backfill MERGE on old partitions and streaming append to today both succeed.
- [ ] No unexplained `Concurrent*Exception` in job run history over a week.

## Checked
2026-10-28. Confirmed against the Databricks isolation level page, the Delta Lake concurrency control page (ConcurrentAppendException, ConcurrentDeleteReadException, ConcurrentDeleteDeleteException, MetadataChangedException, ProtocolChangedException), the table properties page (isolationLevel values Serializable and WriteSerializable, default WriteSerializable; delta.enableDeletionVectors statement) and the table history page (DESCRIBE HISTORY, operationParameters). Removed: the conflict matrix cells, Runtime 14.2 and table-layout requirements for row-level concurrency, the predictive optimization claim and readVersion.
Method: documentation only; no commands were run.
