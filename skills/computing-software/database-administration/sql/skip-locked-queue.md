---
id: computing-software.database-administration.sql.skip-locked-queue
name: skip-locked-queue
category: computing-software
field: database-administration
product: sql
tags: [sql, skip-locked-queue]
level: advanced
status: docs-checked
description: "Build a safe work queue with FOR UPDATE SKIP LOCKED."
sources: ["https://www.postgresql.org/docs/current/sql-select.html", "https://www.sqlite.org/lang_transaction.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SELECT FOR UPDATE SKIP LOCKED job queues

- `WITH j AS (SELECT id FROM jobs WHERE state = 'new' ORDER BY id LIMIT 10 FOR UPDATE SKIP LOCKED) UPDATE jobs SET state = 'running' FROM j WHERE jobs.id = j.id RETURNING jobs.*;`
- With SKIP LOCKED any selected rows that cannot be immediately locked are skipped; PostgreSQL documents this as suitable for multiple consumers of a queue-like table, though it gives an inconsistent view of the data.
- Reclaim stuck jobs with a lease timeout.
- SQLite: `BEGIN IMMEDIATE` starts a write transaction immediately and may fail with SQLITE_BUSY if another write transaction is active.
- Self-check: two concurrent workers never receive the same job id.

## Checked

2026-11-02. Confirmed: FOR UPDATE ... SKIP LOCKED behaviour and queue use (PostgreSQL SELECT page); BEGIN IMMEDIATE (SQLite transaction page). Removed: version and other-engine claims, the index requirement, the SQLite no-row-locks claim.
Method: documentation only; no commands were run.
