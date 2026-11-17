---
id: computing-software.database-administration.sql.serialization-failure-retry
name: serialization-failure-retry
category: computing-software
field: database-administration
product: sql
tags: [sql, serialization-failure-retry]
level: advanced
status: docs-checked
description: "Run SERIALIZABLE transactions with retry on serialization failures."
sources: ["https://www.postgresql.org/docs/current/transaction-iso.html", "https://www.postgresql.org/docs/current/mvcc-serialization-failure-handling.html", "https://www.postgresql.org/docs/current/sql-set-transaction.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serializable isolation and retry loops

- `BEGIN ISOLATION LEVEL SERIALIZABLE;` Serializable behaves like Repeatable Read plus monitoring for read/write dependencies that could not match any serial order. A conflict raises SQLSTATE 40001 (serialization_failure), which the manual says to retry unconditionally. Deadlocks (40P01, deadlock_detected) are also advisable to retry.
- Retry the complete transaction, including the logic that decides which SQL and values to use; PostgreSQL offers no automatic retry. A retry may itself fail, so loop with a cap (backoff is common practice, not from the manual). Unique-violation (23505) and exclusion-violation (23P01) errors can sometimes be retried, but may be persistent, so take more care.
- Do not depend on results read in a transaction that later aborted.
- Predicate locks used by Serializable do not block and cannot cause deadlocks. Only updating transactions need retries at Repeatable Read; read-only transactions never hit serialization conflicts there.
- `SERIALIZABLE, READ ONLY, DEFERRABLE` may block while acquiring its snapshot, then runs without the normal serializable overhead and cannot be cancelled by a serialization failure; suited to long reports or backups. DEFERRABLE has no effect without both other properties.
- READ COMMITTED (the default) lets two successive SELECTs see different data (non-repeatable reads). REPEATABLE READ in PostgreSQL is snapshot isolation; its snapshot is taken at the first non-transaction-control statement and a concurrent update raises "could not serialize access due to concurrent update".
- Self-check: run two concurrent conflicting transactions and confirm one retries.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual pages transaction-iso.html, mvcc-serialization-failure-handling.html and sql-set-transaction.html; the draft's write-skew statement for READ COMMITTED was dropped because the page describes that anomaly only in the Serializable example.
