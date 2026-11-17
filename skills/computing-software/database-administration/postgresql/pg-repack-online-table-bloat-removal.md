---
id: computing-software.database-administration.postgresql.pg-repack-online-table-bloat-removal
name: pg-repack-online-table-bloat-removal
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, vacuum, pg-repack, table-bloat, vacuum-full-alternative, online-rewrite, pg-squeeze]
level: advanced
status: docs-checked
description: "Remove PostgreSQL table bloat without the long ACCESS EXCLUSIVE lock of VACUUM FULL using pg_repack: prerequisites, run options, lock behaviour and cleanup after failures."
sources:
  - https://reorg.github.io/pg_repack/
  - https://www.postgresql.org/docs/current/routine-vacuuming.html#VACUUM-FOR-SPACE-RECOVERY
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pg_repack: online bloat removal

**Goal:** shrink a table that VACUUM cannot shrink (dead space spread through
the file) while the application keeps reading and writing.

## When you need it
Plain VACUUM marks dead space reusable but rarely returns it to the OS.
After a mass delete, a table may stay much larger than its live data, hurting
sequential scans and cache efficiency. pg_repack offers an online `VACUUM FULL` and an
online `CLUSTER`, holding `ACCESS EXCLUSIVE` only briefly.

Check first:
```sql
SELECT n_live_tup, n_dead_tup FROM pg_stat_user_tables WHERE relname='events';
SELECT pg_size_pretty(pg_total_relation_size('events'));
```

## Setup
Install pg_repack, then per database: `CREATE EXTENSION pg_repack;`. The client binary version must match
the extension version (otherwise it errors). Requirements: the table has a PRIMARY KEY or a UNIQUE index on NOT NULL
columns; free disk about twice the size of the tables and indexes being repacked; superuser or table and index
owner (owners need `--no-superuser-check`, `-k` on platforms that run it without superuser).
Temp tables cannot be repacked and GiST indexes cannot be used to cluster.

## Run
```bash
pg_repack -h db -d appdb -t public.events --jobs 4 --wait-timeout 60 --no-kill-backend
pg_repack -d appdb -t public.events --only-indexes      # rebuild indexes only
pg_repack -d appdb -t public.events -o created_at        # online CLUSTER by those columns
pg_repack -d appdb --dry-run -t public.events
pg_repack -d appdb -t public.events --no-order           # online VACUUM FULL
```
How it works: creates a log table and a trigger capturing INSERT/UPDATE/DELETE, copies the rows
into a new table, builds indexes, applies the log, swaps the tables (including indexes and toast tables) and drops
the original. It holds `ACCESS EXCLUSIVE` only briefly during setup and the final swap; otherwise
`SHARE UPDATE EXCLUSIVE`, so reads and writes continue. `--wait-timeout` (default 60 seconds) is how long it waits for
those two locks; after that it cancels conflicting queries (and terminates remaining backends after twice the timeout)
unless `--no-kill-backend` is set, which skips the table instead. `--jobs` parallelizes index builds for
full-table repacks only.

## Failure cleanup
After a fatal error, clean up by dropping and recreating the extension in that database
(`DROP EXTENSION pg_repack CASCADE;` then `CREATE EXTENSION pg_repack;`). Symptoms of leftovers: a warning that
the table already has a trigger called `repack_trigger`, or an invalid temporary index that you remove with `DROP INDEX`
before retrying.

## Gotchas
- DDL on the target table is not possible while pg_repack runs (it holds `SHARE UPDATE EXCLUSIVE`); on versions up to 1.1.8 it could fail or corrupt data.
- Write-heavy tables may struggle to catch up: `--switch-threshold` switches tables when that many tuples remain in the log table.
- Two concurrent pg_repack runs on one table can deadlock.

## Verify
Table size reduced to roughly live data size; `\d events` shows no leftover
`repack_trigger`; application error rate unchanged during the run.

## Checked

2026-10-31. Confirmed against the pg_repack documentation: requirements (primary key or NOT NULL unique index, about twice the disk, superuser or owner with `--no-superuser-check`), options (`--jobs`, `--wait-timeout` default 60, `--no-kill-backend`, `--only-indexes`, `--order-by`, `--no-order`, `--dry-run`, `--switch-threshold`), locking and the full-table algorithm, restrictions, cleanup by dropping and recreating the extension, and the error messages. Removed unconfirmed: size multiples, WAL and replica-lag claims, pg_squeeze comparison, `rds_superuser`, `repack.log_<oid>` naming, pgstattuple usage.

Method: documentation only; no commands were run.
