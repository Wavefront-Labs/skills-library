---
id: computing-software.database-administration.postgresql.wal-level-and-wal-compression
name: wal-level-and-wal-compression
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, wal-configuration, wal-level, wal-compression, wal-volume, full-page-images, wal-buffers, pg-stat-wal]
level: advanced
status: verified
description: "Choose PostgreSQL wal_level (minimal/replica/logical) and enable wal_compression (lz4/zstd) to cut WAL volume, measured with pg_stat_wal before and after."
sources:
  - https://www.postgresql.org/docs/current/runtime-config-wal.html
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-WAL-VIEW
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wal_level and wal_compression

**Goal:** WAL carries exactly the detail your replication needs, compressed, so
archive storage and replication bandwidth stay down.

## wal_level (restart required)
| Level | Allows | Notes |
|---|---|---|
| `minimal` | Crash recovery only | Skips WAL for bulk ops in same-transaction-created tables (fast loads: `CREATE TABLE AS` of 200,000 rows wrote 130 kB of WAL at `minimal` and 22 MB at `replica`; a separate-transaction `INSERT` wrote 21 MB at both). No archiving, no replicas: `max_wal_senders` must be 0 (`WAL streaming ("max_wal_senders" > 0) requires "wal_level" to be "replica" or "logical"`) and `archive_mode` must be off (`WAL archival cannot be enabled when "wal_level" is "minimal"`) |
| `replica` (default) | Archiving, streaming replicas, pg_basebackup | The normal choice |
| `logical` | Adds info for logical decoding/replication | Slightly more WAL (a pgbench `-N` run wrote 1,238 bytes per transaction at `logical` against 1,122 at `replica`, about 10% more); logical slots need it (`logical decoding requires "wal_level" >= "logical"`) |
Switching to `logical` later needs a restart, so set it upfront on clusters that
may ever need CDC or logical upgrades.

## wal_compression (reload)
Compresses full-page images (the first change to a page after each checkpoint
writes the whole 8 KB page), usually most of WAL volume.
```conf
wal_compression = lz4      # PG15+: pglz | lz4 | zstd ; 'on' = pglz
```
lz4 and zstd work only if the build has them (the Windows 17.6 build did). Measured with `pgbench -N` (4 clients, 15 s, started right after a checkpoint so most pages need a full-page image): WAL per transaction was 1,642 bytes with `off`, 457 with `pglz` (-72%), 573 with `lz4` (-65%) and 348 with `zstd` (-79%), at 7,417, 7,283, 7,182 and 7,271 tps. Your reduction depends on how many full-page images you write.

## Measure
```sql
SELECT wal_records, wal_fpi, pg_size_pretty(wal_bytes) FROM pg_stat_wal;  -- reset with pg_stat_reset_shared('wal')
```
High `wal_fpi / wal_records` means full-page images dominate: compression and
longer checkpoint intervals (fewer FPIs per page) both help.
Per statement: `EXPLAIN (ANALYZE, WAL)` and `pg_stat_statements.wal_bytes`.

## Gotchas
- `wal_level = minimal` invalidates existing base backups for PITR; never on a
  cluster you archive.
- Compression trades CPU on the primary for I/O; check CPU headroom.
- Logical level with no consumers is harmless; an abandoned logical slot is not
  (it retains WAL).
- `wal_buffers` default (-1 = 1/32 of shared_buffers, between 64kB and one WAL segment, typically 16MB; 4MB with `shared_buffers = 128MB`) is usually fine; the docs say setting it to at least a few megabytes can help a busy server with many concurrent commits.

## Verify
`SHOW wal_level; SHOW wal_compression;` and compare `pg_stat_wal.wal_bytes` per
hour, or archive bytes per day, before and after.

## Checked
PostgreSQL 17.6 (EDB Windows build) in a scratch cluster: `wal_compression` accepted `off`, `pglz`, `lz4`, `zstd` via `ALTER SYSTEM` + reload; the figures above come from `pg_stat_wal.wal_bytes` after `pg_stat_reset_shared('wal')`; the `minimal` start failures, the bulk-load WAL sizes and the logical-slot error were reproduced; `SHOW wal_buffers` gave 4MB. `pg_stat_wal` columns `wal_records`, `wal_fpi`, `wal_bytes` exist and `EXPLAIN (ANALYZE, WAL)` printed `WAL: records=293 fpi=3 bytes=52474`. Docs (runtime-config-wal): methods `pglz`, `lz4`, `zstd`, `on` is a historical spelling of `pglz`, the `wal_buffers` rule, and switching to `minimal` makes previous base backups unusable for point-in-time recovery and standbys; logical-decoding docs: replication slots keep required WAL even with no consumer connected.
