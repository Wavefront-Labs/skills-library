---
id: computing-software.database-administration.postgresql.locking-deadlocks-and-long-transactions
name: locking-deadlocks-and-long-transactions
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, locking, deadlock, pg_locks, pg_stat_activity, idle-in-transaction, lock-timeout, advisory-locks, blocking-queries, mvcc, exclusive-lock]
level: advanced
status: verified
description: "Find and kill blocking lock chains and deadlocks in Postgres, and stop long-running or idle-in-transaction sessions from stalling the system."
sources:
  - https://www.postgresql.org/docs/current/explicit-locking.html
  - https://www.postgresql.org/docs/current/view-pg-locks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostgreSQL locking, deadlocks, and long transactions

**Goal:** go from "the app is hanging" to the exact blocking query in under a
minute, and know which lock each DDL/DML statement actually takes so you stop
causing the problem.

## 1. Find who is blocking whom
```sql
SELECT blocked.pid AS blocked_pid, blocked.query AS blocked_query,
       blocking.pid AS blocking_pid, blocking.query AS blocking_query,
       now() - blocking.query_start AS blocking_duration
FROM pg_stat_activity blocked
CROSS JOIN LATERAL unnest(pg_blocking_pids(blocked.pid)) AS b(pid)
JOIN pg_stat_activity blocking ON blocking.pid = b.pid;
```
Do not hand-join `pg_locks` on `locktype`, `database` and `relation` alone: for `transactionid` locks (row-lock waits) those columns are all NULL, so every waiter matches every holder (tested: with one holder and two waiters the join reported the first waiter as blocked by the second waiter as well). `pg_blocking_pids(pid)` gives the correct answer, including a second waiter queued behind the first (it waits on a `tuple` lock and lists the first waiter). The built-in function is used on each waiting backend in
`pg_stat_activity`. A long chain (A blocks B blocks C) needs walking — the head of
the chain is the only one worth killing.

## 2. Kill or cancel
- `SELECT pg_cancel_backend(pid)` — cancels the running statement, keeps the
  session and transaction open. Often not enough if the session is just sitting
  idle-in-transaction holding a lock.
- `SELECT pg_terminate_backend(pid)` — drops the whole connection, rolling back its
  transaction. This is what actually releases the lock in most "stuck" cases.
- Prefer fixing the root cause (a forgotten `COMMIT`/`ROLLBACK` in app code, a
  connection pool leaking transactions) over habitually terminating sessions.

## 3. Deadlocks vs. plain lock waits
A deadlock (two transactions each waiting on a lock the other holds) is detected
automatically by Postgres's deadlock detector (`deadlock_timeout`, default 1s) and
one side is aborted with `ERROR: deadlock detected`, logged with both queries and
lock types. A plain lock wait is not an error — it just waits, potentially forever,
until `statement_timeout`/`lock_timeout` fires or someone intervenes. Set
`lock_timeout` (e.g. 5s) for interactive/app queries so a blocked statement fails
fast and retries instead of queuing indefinitely behind a long transaction.

## 4. Which DDL takes which lock
This is the part people get burned by in production:
- `ALTER TABLE ... ADD COLUMN` with no default is fast and takes `ACCESS EXCLUSIVE` only briefly
  (no rewrite: checked by `relfilenode`).
- `ALTER TABLE ... ADD COLUMN ... DEFAULT <constant or stable expression>` since PG11 is a
  metadata-only change, cheap (`DEFAULT 5` and `DEFAULT now()` did not rewrite). A volatile
  default such as `DEFAULT random()` rewrites the whole table under the lock.
- `CREATE INDEX` takes `SHARE` lock, blocking writes to the table for its full
  duration — on a large table that is unacceptable. Always use
  `CREATE INDEX CONCURRENTLY` in production (note: cannot run inside a transaction
  block, and a failed concurrent build leaves an invalid index that must be dropped).
- `ALTER TABLE ... SET NOT NULL` scans the whole table under `ACCESS EXCLUSIVE`; add
  `CHECK (col IS NOT NULL) NOT VALID`, then `VALIDATE CONSTRAINT` (takes `SHARE UPDATE EXCLUSIVE`,
  so reads and writes continue; checked for CHECK and FOREIGN KEY constraints), then `SET NOT NULL`
  (PG12+ skips the scan; the server logged that existing constraints prove it).
- `VACUUM FULL` takes `ACCESS EXCLUSIVE` on the table. Plain `REINDEX TABLE` takes `SHARE` on the table (writes block, reads continue) and `ACCESS EXCLUSIVE` on the index it rebuilds (so queries using that index block). Use
  `REINDEX CONCURRENTLY` (PG12+) or `pg_repack` instead on live tables.

## 5. Advisory locks
Application-level locks (`pg_advisory_lock(key)`) that don't correspond to any
table, useful for serializing a job (e.g. "only one cron instance runs this") across
processes. Session-level locks persist until explicitly unlocked or the session
ends; `pg_try_advisory_lock` is the non-blocking variant for "skip if already
running" patterns. Forgetting to release one (e.g. on an exception path) wedges the
next run — always unlock in a `finally`/exception handler.

## Verify
- [ ] Can produce the blocking-chain query above and name the head blocker in under a minute.
- [ ] `lock_timeout` is set for interactive app roles, not left at 0 (infinite).
- [ ] Any `CREATE INDEX` or `REINDEX` on a production table used the `CONCURRENTLY` variant.
- [ ] No advisory lock acquisition path is missing a corresponding unlock on the error path.
- [ ] Deadlock log entries (if any) were read for the actual query pair, not just alerted on.

## Checked
Run on PostgreSQL 17.6 (Windows build, two to eight real sessions via psycopg 3.3) on Windows: the blocking-chain queries (the old hand join gave wrong pairs, the replacement and the `pg_blocking_pids` tree gave correct ones), `pg_cancel_backend` on an idle-in-transaction holder (returned true, waiter stayed blocked) versus `pg_terminate_backend` (waiter proceeded, holder session gone); a two-session deadlock (`ERROR: deadlock detected` after `deadlock_timeout` 1 s, the waiting side aborted, DETAIL naming both processes in the log); `lock_timeout` giving SQLSTATE 55P03 `canceling statement due to lock timeout`; a queued `ALTER TABLE` making a later `SELECT` wait; `LOCK ... NOWAIT`; `CREATE INDEX CONCURRENTLY` inside a transaction (`cannot run inside a transaction block`); a failed unique concurrent build leaving an invalid index; advisory locks (`pg_try_advisory_lock`, released when the session ends); rewrite checks by `relfilenode`. Not run: pg_repack, Linux (PostgreSQL behaviour here is not OS-specific apart from file and process handling).
