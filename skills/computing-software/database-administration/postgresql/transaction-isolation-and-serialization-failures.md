---
id: computing-software.database-administration.postgresql.transaction-isolation-and-serialization-failures
name: transaction-isolation-and-serialization-failures
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, mvcc, locking, transaction-isolation, serialization-failure, serializable-isolation, repeatable-read, read-committed, sqlstate-40001, retry-loop]
level: advanced
status: verified
description: "Choose PostgreSQL isolation levels (READ COMMITTED, REPEATABLE READ, SERIALIZABLE/SSI), understand the anomalies each allows, and retry 40001 serialization failures correctly."
sources:
  - https://www.postgresql.org/docs/current/transaction-iso.html
  - https://wiki.postgresql.org/wiki/SSI
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Isolation levels and serialization failures

**Goal:** concurrent transactions cannot produce results no serial order could,
where it matters, and the app handles the resulting retries.

## Levels in PostgreSQL
| Level | Snapshot | Allows | Errors you must retry |
|---|---|---|---|
| READ COMMITTED (default) | per statement | non-repeatable reads, lost updates (read-then-write), write skew | none (but logic bugs) |
| REPEATABLE READ | per transaction | write skew | 40001 on concurrent update of the same row |
| SERIALIZABLE (SSI) | per transaction + predicate tracking | nothing | 40001 when a dangerous pattern is detected |
READ UNCOMMITTED behaves as READ COMMITTED (`SHOW transaction_isolation` still prints `read uncommitted`).

## Classic bugs at READ COMMITTED
- **Lost update**: two sessions read balance 100, both write 100-10. Fix: atomic
  `UPDATE acct SET bal = bal - 10`, or `SELECT ... FOR UPDATE`, or higher isolation.
- **Write skew**: "at least one doctor on call": two transactions each check that
  another doctor is on call, both go off call. Only SERIALIZABLE (or explicit
  locking of the checked rows/ a constraint) prevents it.

## Using SERIALIZABLE
```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT count(*) FROM oncall WHERE shift_id = 7 AND on_call;
UPDATE oncall SET on_call = false WHERE doctor_id = 3 AND shift_id = 7;
COMMIT;   -- may fail: ERROR 40001 could not serialize access due to read/write dependencies among transactions
```
Rules for SSI to work well:
- **Every** transaction involved must run SERIALIZABLE.
- Retry the whole transaction on SQLSTATE `40001` (and `40P01` deadlock), with
  backoff, re-reading data; never just re-issue the failed statement.
- Keep transactions short; declare read-only ones `READ ONLY` (fewer false positives,
  `DEFERRABLE` for long reports on a safe snapshot).
- Indexes reduce false positives (predicate locks become page/tuple level instead of relation level).
- Monitor `pg_stat_database.xact_rollback` and app retry metrics.

## Gotchas
- ORMs may hide the 40001 as a generic error: map it to retry.
- Default level can be set per role/database: `ALTER ROLE app SET default_transaction_isolation = 'serializable';`
- Hot standbys do not support SERIALIZABLE: an attempt to set it there raises an error (PG docs, hot-standby). Only updating transactions need retries at REPEATABLE READ; read-only ones never see serialization conflicts there.

## Verify
Run the write-skew test in two sessions: at SERIALIZABLE one commit fails with
40001; the app's retry wrapper succeeds on the second attempt.

## Checked
PostgreSQL 17.6, two psycopg connections on a two-doctor on-call table: at READ COMMITTED and REPEATABLE READ both transactions committed and nobody was left on call (write skew); at SERIALIZABLE the second commit failed with SQLSTATE 40001 `could not serialize access due to read/write dependencies among transactions` and one doctor stayed on call; two REPEATABLE READ sessions updating the same row gave 40001 `could not serialize access due to concurrent update`; `default_transaction_isolation` is `read committed`. Docs (transaction-iso, hot-standby): READ UNCOMMITTED maps to READ COMMITTED, predicate locking, no SERIALIZABLE on hot standby. DEFERRABLE only has an effect on SERIALIZABLE READ ONLY transactions (docs: sql-set-transaction).
