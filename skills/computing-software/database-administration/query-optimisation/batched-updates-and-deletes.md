---
id: computing-software.database-administration.query-optimisation.batched-updates-and-deletes
name: batched-updates-and-deletes
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, sql, query-anti-patterns, batched-deletes, batched-updates, data-purge, replication-lag, lock-escalation, keyset-batching]
level: practitioner
status: draft
description: "Delete or update millions of rows without long locks, log/WAL explosions or replica lag: keyset-driven batches, pacing, per-engine syntax, and when to swap or drop partitions instead."
sources:
  - https://use-the-index-luke.com/sql/dml/delete
  - https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide#lock-escalation
  - https://dev.mysql.com/doc/refman/8.4/en/delete.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Batched updates and deletes

**Goal:** purge 200M old rows from a live table while normal traffic and replicas
stay unaffected.

## Why one big statement hurts
`DELETE FROM events WHERE created_at < '2025-01-01'` in one transaction:
holds locks on every row for its whole duration, generates one huge WAL/binlog/log
burst (replicas lag; SQL Server log can't truncate), may escalate to a table lock
(SQL Server at ~5000 locks), and a failure rolls back everything (as slowly as it ran).

## Pattern: small keyset-driven batches, committed separately
```sql
-- PostgreSQL (loop in app/script; each statement its own transaction)
WITH b AS (SELECT id FROM events WHERE created_at < '2025-01-01' ORDER BY id LIMIT 5000)
DELETE FROM events e USING b WHERE e.id = b.id;

-- MySQL
DELETE FROM events WHERE created_at < '2025-01-01' ORDER BY id LIMIT 5000;

-- SQL Server
DELETE TOP (4000) FROM dbo.events WHERE created_at < '2025-01-01';   -- < 5000 to avoid escalation
```
Repeat until 0 rows affected. Needs an index on the filter (`created_at`) or each
batch scans the table. For updates, iterate over PK ranges:
`UPDATE ... WHERE id > :last AND id <= :last + 10000 AND <condition>` so each
batch starts where the previous ended (no rescanning finished ranges).

## Pacing
- Sleep between batches (e.g. 100-500 ms), and back off when replica lag or
  `Threads_running`/active sessions exceed a threshold.
- Run off-peak; tools: `pt-archiver` (MySQL) does this with throttling.
- PostgreSQL: dead tuples accumulate; let autovacuum keep up (or VACUUM between chunks for very large purges).

## Better: avoid DELETE entirely
- Partitioned by time → `DROP`/`DETACH` the old partition: instant, no row-level work.
- Keeping a small fraction → copy the keepers to a new table, swap names, drop the old (needs a write freeze or sync).

## Gotchas
- Batch size: big enough to amortise overhead, small enough to finish in < ~1 s.
- Triggers and cascading FKs multiply per-row work; account for them.

## Verify
Monitor during the run: replica lag stays under threshold, no lock waits for app
queries, transaction log/WAL rate acceptable; final count of matching rows = 0.
