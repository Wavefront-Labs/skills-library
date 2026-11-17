---
id: computing-software.database-administration.postgresql.asynchronous-commit
name: asynchronous-commit
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, wal-configuration, asynchronous-commit, synchronous-commit-off, wal-writer-delay, commit-latency, durability-tradeoff, bulk-load]
level: advanced
status: verified
description: "Use synchronous_commit=off per transaction or role to cut PostgreSQL commit latency where losing the last few hundred ms of commits on crash is acceptable."
sources:
  - https://www.postgresql.org/docs/current/wal-async-commit.html
  - https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Asynchronous commit

**Goal:** high-rate, low-value writes (metrics, sessions, clicks) stop waiting on
an fsync per commit, while money-moving transactions stay fully durable.

## What it does
With `synchronous_commit = off`, COMMIT returns as soon as the commit record is
in WAL buffers; the WAL writer flushes it within `wal_writer_delay` (default
200ms, worst case about 3x that). A crash loses those last commits, but the
database stays **consistent** (unlike `fsync = off`): it is as if those
transactions never happened.

## Scope it narrowly
```sql
-- per transaction
BEGIN; SET LOCAL synchronous_commit = off; INSERT INTO page_views ...; COMMIT;
-- per role
ALTER ROLE metrics_writer SET synchronous_commit = off;
-- per database
ALTER DATABASE telemetry SET synchronous_commit = off;
```
Leave the cluster default `on`. Mixed transactions are fine: WAL is flushed in order, so a later
synchronous commit also flushes all earlier async ones (checked: after a synchronous commit
`pg_current_wal_flush_lsn()` equals the insert LSN).

## When it helps
Small, frequent single-row commits on storage with slow fsync (measure your own
flush latency, e.g. with `pg_test_fsync`). Batching many rows per transaction gives similar
gains with no durability trade-off; try that first.
Benchmark: `pgbench -c 32 -j 8 -T 60` with and without
`PGOPTIONS='-c synchronous_commit=off'`.

## Gotchas
- With synchronous replication, `off` also skips waiting for the standby; use
  `local` to keep local durability but skip only the standby wait. `commit_delay` is ignored
  during an asynchronous commit.
- Clients told "committed" may act on data that then disappears after a crash
  (e.g. sent a confirmation email). Only use where that is acceptable.
- `commit_delay`/`commit_siblings` (group commit) are a different, rarely useful knob.
- Settings scope: `ALTER ROLE ... SET` applies at the role's next login; `ALTER DATABASE ... SET` to new sessions in that database; `SET LOCAL` to one transaction.

## Verify
`SHOW synchronous_commit;` in the target role's session; commit latency in
`pg_stat_statements` (mean_exec_time for COMMIT) or app metrics drops; cluster
default still `on`.

## Checked
PostgreSQL 17.6: `wal_writer_delay` default 200ms; `ALTER ROLE`/`ALTER DATABASE ... SET synchronous_commit=off` took effect for new sessions of that role/database only; `SET LOCAL` and `local` accepted, invalid values list `local, remote_write, remote_apply, on, off`. Docs (wal-async-commit, runtime-config-wal): risk window is at most three times `wal_writer_delay`, `commit_delay` ignored for async commits, `off` does not risk corruption. The pgbench figures were not measured here: treat the speed-up as workload dependent.
