---
id: computing-software.database-administration.postgresql.pg-stat-io-and-checkpointer-statistics
name: pg-stat-io-and-checkpointer-statistics
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-monitoring, pg-stat-io, pg-stat-bgwriter, pg-stat-checkpointer, checkpoints, buffers-backend, shared-buffers, io-statistics]
level: practitioner
status: verified
description: "Read pg_stat_io, pg_stat_bgwriter and pg_stat_checkpointer to see who does PostgreSQL I/O, whether checkpoints are forced, and if shared_buffers is too small."
sources:
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-IO-VIEW
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-CHECKPOINTER-VIEW
  - https://www.postgresql.org/docs/current/wal-configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pg_stat_io and checkpointer statistics

**Goal:** know whether reads are served from cache, who is writing dirty buffers, and whether checkpoints happen on schedule or are forced by WAL volume.

## Checkpoints (17+: pg_stat_checkpointer; 16 and older: pg_stat_bgwriter)
```sql
-- 17+
SELECT num_timed, num_requested, write_time, sync_time, buffers_written, stats_reset FROM pg_stat_checkpointer;
-- <=16
SELECT checkpoints_timed, checkpoints_req, buffers_checkpoint, buffers_clean, buffers_backend, maxwritten_clean
FROM pg_stat_bgwriter;
```
- `num_requested` (`checkpoints_req`) a large share of the total: checkpoints are triggered by `max_wal_size`, not `checkpoint_timeout`. Raise `max_wal_size` until most are timed.
- `maxwritten_clean` climbing: bgwriter hits `bgwriter_lru_maxpages`; raise it.
- `buffers_backend` high (<=16): backends evict dirty pages themselves, stalling queries; more `shared_buffers` / bgwriter aggressiveness.

Also set `log_checkpoints = on` (default on since 15): each line shows write/sync time and the trigger (`time` vs `wal`).

## pg_stat_io (16+)
One row per backend_type x object x context.
```sql
SELECT backend_type, object, context, reads, writes, extends, hits, evictions, fsyncs
FROM pg_stat_io WHERE reads + writes + coalesce(fsyncs,0) > 0 ORDER BY reads + writes DESC;
```
- Cache hit ratio per backend type: `hits / (hits + reads)` for `client backend`, context `normal`.
- `client backend` with large `writes` in context `normal`: backends writing dirty buffers (same signal as `buffers_backend`).
- `fsyncs` by `client backend` are unexpected (backends normally leave fsync to the checkpointer); expect NULL/0. Docs: fsyncs are only tracked in context `normal`.
- Context `bulkread` / `vacuum` use ring buffers by design, so low hit ratios there are normal.

## Resetting for a clean measurement window
```sql
SELECT pg_stat_reset_shared('io');            -- 16+
SELECT pg_stat_reset_shared('checkpointer');  -- 17+ ('bgwriter' for <=16)
```
Record the time; compute rates from deltas over a known interval rather than totals since boot.

## Gotchas
- PG18 adds byte and timing columns to pg_stat_io (`read_bytes`, `write_bytes`, ...) and drops `op_bytes`; the queries here still run.
- Reads counted in pg_stat_io may be satisfied by the OS page cache; it measures PostgreSQL buffer misses, not physical disk reads.
- Column names moved from pg_stat_bgwriter to pg_stat_checkpointer in 17; monitoring queries must branch on `server_version_num`.

## Verify
After raising `max_wal_size`, the requested/timed ratio falls over the next day and checkpoint log lines show `checkpoint starting: time`.

## Checked
- PostgreSQL 18.6: `pg_stat_checkpointer` columns (`num_timed`, `num_requested`, `write_time`, `sync_time`, `buffers_written`, `stats_reset`, plus `num_done`, `restartpoints_*`, `slru_written`) and the `pg_stat_io` query ran (columns `reads`, `writes`, `extends`, `hits`, `evictions`, `fsyncs` exist; 18 adds `read_bytes`, `write_bytes`, `extend_bytes`, `read_time` etc.); `pg_stat_reset_shared('io')`, `('checkpointer')` and `('bgwriter')` all ran; `pg_stat_bgwriter` in 18 has only `buffers_clean`, `maxwritten_clean`, `buffers_alloc`, `stats_reset`. The logs showed `checkpoint starting: wal` for size-triggered checkpoints and `shutdown immediate` for the shutdown one.
- PostgreSQL 16.15: `SELECT checkpoints_timed, checkpoints_req, buffers_checkpoint, buffers_clean, buffers_backend, maxwritten_clean FROM pg_stat_bgwriter` ran; `pg_stat_io` and `pg_stat_reset_shared('io')` and `('bgwriter')` ran.
- Docs: pg_stat_io page (fsyncs only in context normal), runtime-config-resource (`bgwriter_lru_maxpages` caps writes per round); PG15 notes flip `log_checkpoints` to on. The old `fsync request queue overflowed` explanation was removed because it is not in the docs.
