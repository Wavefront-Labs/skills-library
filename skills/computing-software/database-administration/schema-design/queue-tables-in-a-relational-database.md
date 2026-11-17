---
id: computing-software.database-administration.schema-design.queue-tables-in-a-relational-database
name: queue-tables-in-a-relational-database
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, schema-patterns, queue-table, skip-locked, job-queue, outbox-pattern, bloat]
level: advanced
status: verified
description: "Design a job or outbox queue table that scales: SKIP LOCKED claiming, visibility timeouts, partial indexes, retries and dead letters, and keeping bloat under control."
sources:
  - https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html
  - https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-table
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue tables in a relational database

A queue in the same database as your data gives transactional enqueue (job created only if the
business transaction commits) without another system. It works well up to thousands of jobs per
second if designed carefully.

## Schema
```sql
CREATE TABLE jobs (
  id           bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  queue        text        NOT NULL,
  payload      jsonb       NOT NULL,
  status       text        NOT NULL DEFAULT 'ready',   -- ready | running | done | dead
  run_at       timestamptz NOT NULL DEFAULT now(),
  attempts     int         NOT NULL DEFAULT 0,
  locked_until timestamptz,
  last_error   text,
  created_at   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX jobs_ready ON jobs (queue, run_at) WHERE status = 'ready';   -- small, hot index
```

## Claiming without contention
```sql
WITH next AS (
  SELECT id FROM jobs
  WHERE queue = 'email' AND status = 'ready' AND run_at <= now()
  ORDER BY run_at
  LIMIT 10
  FOR UPDATE SKIP LOCKED
)
UPDATE jobs j SET status = 'running', attempts = attempts + 1,
                  locked_until = now() + interval '5 minutes'
FROM next WHERE j.id = next.id
RETURNING j.*;
```
`SKIP LOCKED` lets concurrent workers grab different rows instead of queueing on the same ones
(PostgreSQL 9.5+ per its release notes; the claim query was run on 18 and claimed 10 of 15 rows. Other engines have equivalents, such as SQL Server's `READPAST` hint: check their docs).

## Completion, retries, dead letters
- Success: `UPDATE jobs SET status = 'done' WHERE id = $1` (or DELETE / move to history).
- Failure: `status = 'ready', run_at = now() + backoff(attempts), last_error = ...`; after N
  attempts `status = 'dead'` for manual inspection.
- Reaper for crashed workers: `UPDATE jobs SET status = 'ready' WHERE status = 'running' AND locked_until < now();`
- Handlers must be idempotent: a job can run twice after a timeout.

## Keeping it healthy
- Completed rows bloat the table and index: delete or archive done jobs promptly, ideally by
  **partition** (daily partitions dropped in bulk) for high volume.
- Per-table autovacuum tuning (`autovacuum_vacuum_scale_factor = 0.01` or lower) on PostgreSQL.
- Long-running transactions elsewhere prevent cleanup of dead rows: the queue gets slower.
- Watch queue depth and oldest ready job age as SLOs.

## Outbox variant
Write `outbox` rows in the business transaction; a relay reads them in order and publishes to a
broker (or CDC with Debezium reads the table/WAL). Guarantees "publish if and only if committed".

## When to move to a broker
Fan-out to many consumers, very high throughput, or long retention/replay: use Kafka/RabbitMQ/
SQS, possibly fed by the outbox.

## Verify
Run N workers concurrently in a test: no job is processed by two workers at once, throughput
scales with workers, and the ready index stays small.
