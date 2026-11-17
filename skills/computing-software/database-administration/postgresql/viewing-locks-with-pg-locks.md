---
id: computing-software.database-administration.postgresql.viewing-locks-with-pg-locks
name: viewing-locks-with-pg-locks
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, pg-stat-activity, pg-locks, pg-blocking-pids, blocking, lock-waits, troubleshooting]
level: practitioner
status: verified
description: "Find who is blocking whom in PostgreSQL with pg_blocking_pids and pg_locks, read lock modes on relations, and end the root blocker safely."
sources:
  - https://www.postgresql.org/docs/current/view-pg-locks.html
  - https://www.postgresql.org/docs/current/functions-info.html#FUNCTIONS-INFO-SESSION
  - https://www.postgresql.org/docs/current/explicit-locking.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Viewing locks with pg_locks and pg_blocking_pids

## Fast answer: blocking tree
```sql
SELECT a.pid, pg_blocking_pids(a.pid) AS blocked_by, a.usename, a.state,
       a.wait_event_type, a.wait_event, now() - a.xact_start AS xact_age,
       left(a.query, 80) AS query
FROM pg_stat_activity a
WHERE cardinality(pg_blocking_pids(a.pid)) > 0
   OR a.pid IN (SELECT unnest(pg_blocking_pids(pid)) FROM pg_stat_activity)
ORDER BY xact_age DESC NULLS LAST;
```
The **root blocker** is the pid that appears in `blocked_by` but is not itself blocked. It is
often `idle in transaction`: a session that ran an UPDATE or DDL and never committed.

## Which object and mode
```sql
SELECT l.pid, l.locktype, l.relation::regclass, l.mode, l.granted, l.waitstart
FROM pg_locks l
WHERE l.relation IS NOT NULL AND l.database = (SELECT oid FROM pg_database WHERE datname = current_database())
ORDER BY l.relation, l.granted DESC;
```
- `granted = false` rows are waiters; `waitstart` (PG14+) says since when.
- `locktype = transactionid` waits mean a **row lock** conflict: the waiter waits for the
  holder's transaction to end (mode `ShareLock`, `waitstart` set; checked). A further waiter on the same row shows `locktype = tuple` and lists the first waiter in `pg_blocking_pids`.
- `AccessExclusiveLock` waiting on a busy table (from `ALTER TABLE`, `DROP`, `TRUNCATE`,
  `VACUUM FULL`) queues **every later reader** behind it. That is the classic "one migration
  froze the site" pattern.

## Ending it
```sql
SELECT pg_cancel_backend(12345);     -- cancel current query; transaction stays open if idle
SELECT pg_terminate_backend(12345);  -- end session; its transaction rolls back
```
Idle-in-transaction blockers need terminate; cancel does nothing for them. Confirm with the
application owner when the blocker is a batch job mid-way (rollback of a huge transaction
can take as long as it ran).

## Prevention
- `idle_in_transaction_session_timeout = '5min'` (per role for apps).
- `SET lock_timeout = '3s'` before DDL in migrations, with retry.
- `log_lock_waits = on` so waits over `deadlock_timeout` are logged with the holder pid.

## Gotchas
- `pg_blocking_pids()` is not free on very busy systems (it takes lock manager locks);
  don't run it every second from monitoring.
- Advisory locks appear as `locktype = advisory` with the key in `classid/objid`.
- Prepared transactions hold locks with no session: check `pg_prepared_xacts`.

## Verify
After terminating the root blocker, re-run the tree query: no rows with non-empty
`blocked_by`.

## Checked
Run on PostgreSQL 17.6 (Windows build, two to eight real sessions via psycopg 3.3) on Windows: the blocking-tree query (root blocker was the idle-in-transaction session; after terminating it the next waiter became the holder, so re-run until empty), `granted = false` rows with `waitstart` populated, `transactionid` and `tuple` waits, cancel versus terminate on an idle-in-transaction holder, advisory lock rows (`classid` 0, `objid` the key, `objsubid` 1 for the single-bigint form), a prepared transaction keeping a RowExclusiveLock with `pid` NULL and blocking an UPDATE (listed in `pg_prepared_xacts`), `log_lock_waits` producing `still waiting for ShareLock on transaction N after 1011 ms` and `acquired ... after ...` lines, `idle_in_transaction_session_timeout` closing the idle session. Not run: the cost of `pg_blocking_pids` under load.
