---
id: computing-software.database-administration.postgresql.group-commit-commit-delay
name: group-commit-commit-delay
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, commit-delay, commit-siblings, wal-buffers, group-commit, wal-performance, pg-test-fsync]
level: practitioner
status: docs-checked
description: "Tune PostgreSQL group commit with commit_delay, commit_siblings and wal_buffers for many small concurrent transactions, measured with pg_test_fsync and pgbench."
sources:
  - https://www.postgresql.org/docs/current/wal-configuration.html
  - https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-COMMIT-DELAY
  - https://www.postgresql.org/docs/current/pgtestfsync.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Group commit (commit_delay / commit_siblings / wal_buffers)

Every durable commit waits for a WAL flush (fsync). With many concurrent short transactions on storage with slow fsync, letting one flush cover several commits raises throughput.

## Settings
| GUC | Default | Effect |
|---|---|---|
| `commit_delay` | 0 (µs) | the backend about to flush waits this long so other commits can join the same flush |
| `commit_siblings` | 5 | only delay if at least this many other transactions are active |
| `wal_buffers` | -1 (= 1/32 of shared_buffers, at least 64kB and at most one WAL segment, typically 16MB) | WAL held in memory before it is written; a few MB can help busy servers with many clients |

`commit_delay` can be changed at runtime by superusers and users granted the appropriate SET privilege; `wal_buffers` needs a restart. No delay is performed if `fsync` is off, and `commit_delay` is ignored during an asynchronous commit.

## Procedure
1. Measure flush latency:
   ```bash
   pg_test_fsync -f <PG_WAL_DIR>/fsync.test     # look at "fdatasync" ops/sec for 8kB writes
   ```
   Docs guidance: start `commit_delay` at about half the single 8kB write flush time reported.
2. Baseline with your workload or pgbench at realistic concurrency:
   ```bash
   pgbench -i -s 100 bench && pgbench -c 64 -j 8 -T 120 -N bench
   ```
3. `ALTER SYSTEM SET commit_delay = 200; SELECT pg_reload_conf();` and rerun. Compare TPS and latency; try a few values.
4. Keep it only if TPS rises without unacceptable latency. A value that is too high can raise latency enough to reduce total throughput. The docs say benefits can appear even on fast storage such as SSDs, but must be tested against a representative workload; use a higher `commit_siblings` on fast media and a smaller one on high-latency media.

## Signs WAL flushing is the bottleneck
- Wait events `LWLock:WALWrite`, `IO:WALSync` dominate active sessions.
- WAL write and sync counts and times in `pg_stat_io` for object `wal` (timings need `track_wal_io_timing = on`); in PostgreSQL 18 the old `pg_stat_wal` write and sync columns are no longer there.
- `wal_buffers_full` in `pg_stat_wal` rising: wal_buffers too small.

## Alternatives that trade durability
- `synchronous_commit = off` for specific transactions/roles: no flush wait at all; up to `3 x wal_writer_delay` of committed transactions lost on crash (no corruption). Often a better tool for bulk/low-value writes.
- Batch commits in the application (many rows per transaction) beats any server tuning.

## Gotchas
- `commit_delay` adds latency to every eligible commit even when no one joins the group.
- `fsync = off` is not a tuning knob: it risks corruption on crash.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): `commit_delay` (default 0, microseconds, delay only if at least `commit_siblings` other transactions are active, none with fsync off, SET privilege), `commit_siblings` (default 5), `wal_buffers` (default -1, 1/32 of shared_buffers, 64kB minimum, one WAL segment maximum), WAL configuration chapter (start `commit_delay` at about half the single 8kB flush time reported by pg_test_fsync; too high a value can reduce throughput; `synchronous_commit = off` risk window is three times `wal_writer_delay`), pgbench options (`-i`, `-s`, `-c`, `-j`, `-T`, `-N`), wait event names `WALWrite` and `WAL_SYNC` and the `pg_stat_io` `wal` object with `track_wal_io_timing`. Corrected: the `pg_stat_wal` sync counters and timings are gone in 18 (the `pg_stat_io` wal object is PostgreSQL 18, not 17); removed the unsupported 64MB wal_buffers advice and the NVMe remark.
Method: documentation only; no commands were run.
