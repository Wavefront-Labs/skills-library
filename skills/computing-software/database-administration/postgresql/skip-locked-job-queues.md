---
id: computing-software.database-administration.postgresql.skip-locked-job-queues
name: skip-locked-job-queues
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, mvcc, locking, skip-locked, job-queue-table, select-for-update, row-level-locks, queue-bloat, nowait]
level: advanced
status: verified
description: "Build a reliable job queue in PostgreSQL with SELECT ... FOR UPDATE SKIP LOCKED, and keep it fast under load (partial index, batch claiming, bloat and vacuum)."
sources:
  - https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE
  - https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-ROWS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SKIP LOCKED job queues

**Goal:** many workers pull jobs concurrently, each job is processed once, and
no worker waits on another's lock.

## Schema
```sql
CREATE TABLE jobs (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  queue text NOT NULL, payload jsonb NOT NULL,
  run_at timestamptz NOT NULL DEFAULT now(),
  attempts int NOT NULL DEFAULT 0,
  locked_until timestamptz, done_at timestamptz);
CREATE INDEX jobs_ready ON jobs (queue, run_at) WHERE done_at IS NULL;   -- partial: stays small
```

## Claim and process
```sql
-- in a short transaction: claim up to 10
WITH c AS (
  SELECT id FROM jobs
  WHERE queue = 'email' AND done_at IS NULL AND run_at <= now()
    AND (locked_until IS NULL OR locked_until < now())
  ORDER BY run_at
  LIMIT 10
  FOR UPDATE SKIP LOCKED)
UPDATE jobs j SET locked_until = now() + interval '5 minutes', attempts = attempts + 1
FROM c WHERE j.id = c.id
RETURNING j.id, j.payload;
-- COMMIT, do the work outside the transaction, then:
UPDATE jobs SET done_at = now() WHERE id = ANY($1);
```
`SKIP LOCKED` ignores rows other transactions have locked instead of waiting.
The lease column (`locked_until`) makes crashed workers' jobs reappear without
holding a transaction open during the work. Alternative for short jobs: keep the
transaction open, process, `DELETE` the row, commit (simplest exactly-once, but long
transactions hurt vacuum).

## Keep it healthy
- Completed rows: delete or move them (partition by day and drop old partitions);
  a queue table full of dead tuples makes every claim scan garbage.
- Tune autovacuum for the table: `ALTER TABLE jobs SET (autovacuum_vacuum_scale_factor = 0.01, autovacuum_vacuum_cost_delay = 0);`
- `NOWAIT` instead of SKIP LOCKED raises an error immediately when locked; for
  "lock this specific row or fail fast" cases.
- LISTEN/NOTIFY can wake workers instead of polling.

## Gotchas
- SKIP LOCKED gives an inconsistent view by design: fine for queues, wrong for reports.
- Ordering is best effort (skipped rows are newer/older); don't rely on strict FIFO.
- Max attempts: move jobs with `attempts > 10` to a dead-letter state.

## Verify
Run N workers against 100k jobs: each id processed once (unique constraint on a
results table catches duplicates), no `Lock` waits in `pg_stat_activity.wait_event_type`.

## Checked
Run on PostgreSQL 17.6 (Windows build, two to eight real sessions via psycopg 3.3) on Windows: 8 worker threads claimed and finished 5000 jobs in batches of 10 with the skill's claim query: 5000 distinct rows in the results table (no duplicate processing), no row claimed twice, `attempts` 1 for every job, and no `Lock` wait events seen in 10 ms samples of `pg_stat_activity`; `FOR UPDATE SKIP LOCKED` skipped rows locked by another transaction (rows 1 and 2 held, query returned 3 and 4) and `NOWAIT` raised 55P03 `could not obtain lock on row in relation "jobs"`; the lease column hid leased jobs and made them claimable again after expiry; the partial index was far smaller than the table (57 kB versus 744 kB) and the claim query used it; `ALTER TABLE ... SET (autovacuum_vacuum_scale_factor = 0.01, autovacuum_vacuum_cost_delay = 0)` is accepted. Not run: LISTEN/NOTIFY wake-ups, partitioned queue tables, bloat growth over time, strict FIFO ordering under contention, Linux.
