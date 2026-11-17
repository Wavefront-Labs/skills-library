---
id: computing-software.database-administration.time-series-databases.timescale-memory-parallel-workers
name: timescale-memory-parallel-workers
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-tuning, timescale-memory-parallel-workers, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Use parallel query and size memory for aggregations over many chunks."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parallelism and memory

**Goal:** Use parallel query and size memory for aggregations over many chunks.

## Steps
- `max_parallel_workers` controls how many parallel workers PostgreSQL may use for larger queries; the docs say it defaults to the number of CPUs available, and `timescaledb-tune` changes it with `--cpus` (or `TS_TUNE_NUM_CPUS` in Docker). Smaller queries may not trigger parallel workers.
- `max_worker_processes` is the pool for both background and parallel workers and must be at least `timescaledb.max_background_workers` plus `max_parallel_workers`.
- `timescaledb.max_background_workers` should be the number of databases plus the concurrent background workers you want (one scheduler worker per database); `timescaledb-tune` sets it to 16 by default (`--max-bg-workers`).
- Continuous aggregate refresh and compression jobs run as background workers, so count them.
- Each chunk a query touches needs a lock. Raise `max_locks_per_transaction` (default typically 64; changing it needs a restart). Docs formula: `max_locks_per_transaction = 2 * num_chunks / max_connections`, where `num_chunks` is the most chunks you expect in a hypertable.
- Use `EXPLAIN (ANALYZE, BUFFERS)` to see shared-buffer hits.

**Gotcha:** A query over thousands of chunks with the default `max_locks_per_transaction` fails with `out of shared memory` and the hint to increase `max_locks_per_transaction`.

## Verify
- `EXPLAIN` shows parallel nodes on large scans.
- Wide-range queries complete without lock-table errors.

## Checked

Checked 2026-11-03 against the timescale/docs repository: self-hosted/configuration/configuration and about-configuration. Removed: the `max_parallel_workers_per_gather` 2 to 4 advice, ChunkAppend and parallel append claims, the `timescaledb.max_open_chunks_per_insert` GUC (not found in the docs) and the example value of 256.

Method: documentation only; no commands were run.
