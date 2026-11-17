---
id: computing-software.database-administration.sql.sql-row-locking-and-queues
name: sql-row-locking-and-queues
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-for-update, skip-locked, select-for-update, advisory-locks, job-queue]
level: advanced
status: docs-checked
description: "Lock rows with SELECT FOR UPDATE and SKIP LOCKED in PostgreSQL to build safe work queues and avoid lost updates."
sources: ["https://www.postgresql.org/docs/current/sql-select.html", "https://www.postgresql.org/docs/current/explicit-locking.html", "https://www.postgresql.org/docs/current/transaction-iso.html", "https://www.postgresql.org/docs/current/runtime-config-client.html", "https://www.postgresql.org/docs/current/view-pg-locks.html", "https://www.postgresql.org/docs/current/functions-info.html", "https://www.postgresql.org/docs/current/functions-admin.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Row locking (PostgreSQL)

- The locking clause is `FOR { UPDATE | NO KEY UPDATE | SHARE | KEY SHARE } [ OF table ] [ NOWAIT | SKIP LOCKED ]`. It locks the rows the query returns, requires `UPDATE` privilege on the table, and cannot be used with `GROUP BY`, `HAVING`, `DISTINCT`, `WINDOW`, `UNION` / `INTERSECT` / `EXCEPT` or aggregation. With `LIMIT`, locking stops once enough rows have been returned (rows skipped by `OFFSET` are still locked).
- Avoid deadlocks by taking locks on multiple objects in a consistent order, and take the most restrictive mode needed first. PostgreSQL detects deadlocks and aborts one transaction; handle that by retrying. Without a deadlock, a lock request waits indefinitely, so never hold transactions open across user input.
- Queue pattern: `WITH next AS (SELECT id FROM jobs WHERE status = 'queued' ORDER BY id LIMIT 1 FOR UPDATE SKIP LOCKED) UPDATE jobs SET status = 'running' FROM next WHERE jobs.id = next.id RETURNING jobs.*;`. `SKIP LOCKED` skips rows that cannot be locked immediately; the manual says this gives an inconsistent view of the data, unsuitable for general-purpose work but fine for several consumers of a queue-like table. `NOWAIT` raises an error instead of waiting. Both apply only to row locks; the table-level `ROW SHARE` lock is still taken normally.
- The locking clause does not reach `WITH` queries referenced by the main query; put it inside the `WITH` query, as above.
- Lost-update prevention: under `READ COMMITTED`, `UPDATE`, `DELETE` and `SELECT FOR UPDATE` wait for a concurrent updater, then re-evaluate the `WHERE` clause against the new row version, so an atomic `UPDATE stock SET qty = qty - 1 WHERE id = ? AND qty > 0` (check rows affected) is safe. Alternatives: optimistic `UPDATE ... WHERE id = ? AND version = ?` with a rows-affected check, or pessimistic `FOR UPDATE`.
- Advisory locks are application-defined and not enforced by the system. `pg_advisory_xact_lock(key)` takes an exclusive lock held until the end of the transaction, with no explicit unlock; session-level locks survive a rollback and need an explicit unlock. Beware advisory-lock calls combined with `ORDER BY` / `LIMIT`, where evaluation order decides which locks are taken.
- `lock_timeout` aborts a statement that waits too long for a lock (it applies only to lock waits; setting it in `postgresql.conf` affects all sessions, which the manual advises against, so set it per session or role). `statement_timeout` bounds total time.
- Monitor with the `pg_locks` view (join `pid` to `pg_stat_activity`) and `pg_blocking_pids(pid)`, which returns the sessions blocking a given backend.

## Checked

2026-11-08. Confirmed against the PostgreSQL 18 pages "SELECT" (locking clause, NOWAIT, SKIP LOCKED, inconsistent view, WITH queries, LIMIT behaviour), "Explicit Locking" (deadlocks, consistent order, advisory locks), "Transaction Isolation" (READ COMMITTED WHERE re-evaluation), "Client Connection Defaults" (lock_timeout), "pg_locks", and the "System Information Functions" and "System Administration Functions" pages (`pg_blocking_pids`, `pg_advisory_xact_lock`). Removed as unconfirmed: MySQL 8, Oracle and SQL Server (`READPAST`) equivalents, the "PostgreSQL 9.5+" version note, and the `FOR SHARE` / `FOR KEY SHARE` strength ranking beyond naming them.
Method: documentation only; no commands were run.
