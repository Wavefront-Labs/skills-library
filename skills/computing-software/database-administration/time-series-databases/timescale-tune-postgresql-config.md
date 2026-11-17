---
id: computing-software.database-administration.time-series-databases.timescale-tune-postgresql-config
name: timescale-tune-postgresql-config
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-tuning, timescale-tune-postgresql-config, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Set PostgreSQL parameters sensibly for a Timescale workload."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# timescaledb-tune and config

**Goal:** Set PostgreSQL parameters sensibly for a Timescale workload.

## Steps
- `timescaledb-tune` reads `postgresql.conf` and proposes settings from the machine's memory, CPU count and PostgreSQL version, writing a backup first; changes take effect on the next restart. It is packaged with the binary releases (including Docker).
- Non-interactive: `timescaledb-tune --quiet --yes --dry-run >> /path/to/postgresql.conf` appends the suggestions to the file.
- It tunes memory settings (`shared_buffers`, `effective_cache_size`, `work_mem`, `maintenance_work_mem`; PgTune values for a data-warehouse DB type are the manual route), worker settings and `shared_preload_libraries = 'timescaledb'`.
- Workers: `timescaledb.max_background_workers` is the number of databases plus concurrent background workers (the tool sets 16; override with `--max-bg-workers`), `max_parallel_workers` defaults to the CPU count (`--cpus`), and `max_worker_processes` must be at least their sum.
- Ingest: `synchronous_commit = 'off'` raises write throughput but a crash can lose recent committed transactions; the docs actively discourage changing `fsync`. Insert in batches or use `COPY` / `timescaledb-parallel-copy`.
- Locks: raise `max_locks_per_transaction` (default typically 64; restart needed) using `2 * num_chunks / max_connections`.

**Gotcha:** `work_mem` applies per sort or hash node, so a generous value times parallel queries can exhaust RAM.

## Verify
- `SHOW` for each parameter returns the intended value.
- Ingest throughput improves in a load test.

## Checked

Checked 2026-11-03 against the timescale/docs repository: self-hosted/configuration/configuration and about-configuration, self-hosted/backup-and-restore/logical-backup (parallel copy). Removed: the percentage rules for `shared_buffers`/`effective_cache_size`, `wal_buffers`, `max_wal_size` and `checkpoint_timeout` sizes, and `random_page_cost = 1.1`, none of which these pages state; the PostgreSQL docs root source was not used for them. The `work_mem` per-node gotcha is PostgreSQL behaviour not covered in these pages and is kept as general guidance.

Method: documentation only; no commands were run.
