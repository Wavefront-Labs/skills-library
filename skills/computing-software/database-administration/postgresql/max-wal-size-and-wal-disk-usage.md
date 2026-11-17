---
id: computing-software.database-administration.postgresql.max-wal-size-and-wal-disk-usage
name: max-wal-size-and-wal-disk-usage
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, wal-configuration, postgres-checkpoints, max-wal-size, min-wal-size, wal-disk-usage, checkpoint-warning]
level: practitioner
status: verified
description: "Size max_wal_size and min_wal_size from measured WAL rate so checkpoints are time-driven, and predict how much disk pg_wal really needs."
sources:
  - https://www.postgresql.org/docs/current/wal-configuration.html
  - https://www.postgresql.org/docs/current/runtime-config-wal.html#RUNTIME-CONFIG-WAL-CHECKPOINTS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# max_wal_size, min_wal_size and WAL disk usage

## What they control
- `max_wal_size` (default 1GB): soft limit of WAL generated between checkpoints before a
  checkpoint is **forced**. Not a hard cap on pg_wal size.
- `min_wal_size` (default 80MB): below this, old segments are recycled for reuse rather than
  removed, smoothing bursts.
- `checkpoint_timeout` (default 5min): time-based trigger.

Goal: checkpoints should almost always be triggered by **time**, not size. Size-forced
checkpoints are frequent, cause I/O storms, and inflate WAL through extra full-page writes.

## Measure
```sql
-- PG17+: pg_stat_checkpointer; older: pg_stat_bgwriter.checkpoints_timed/req
SELECT num_timed, num_requested FROM pg_stat_checkpointer;
```
If `num_requested` is a significant share, raise max_wal_size. The log also says it:
`LOG: checkpoints are occurring too frequently (23 seconds apart)` with
`HINT: Consider increasing the configuration parameter "max_wal_size"` (needs
`checkpoint_warning`, default 30s).

WAL rate:
```sql
SELECT pg_current_wal_lsn();          -- note value, wait 10 minutes, repeat
SELECT pg_size_pretty(pg_wal_lsn_diff('<lsn2>', '<lsn1>'));
-- or: SELECT wal_bytes FROM pg_stat_wal;  (cumulative, PG14+)
```

## Sizing (rule of thumb, not from the docs)
`max_wal_size` ~ WAL generated per `checkpoint_timeout` x 1.5 to 2 (because with
`checkpoint_completion_target = 0.9` the spread checkpoint overlaps the next cycle).
Example: 3 GB per 15 min with `checkpoint_timeout = 15min` -> `max_wal_size = 6GB`.
```sql
ALTER SYSTEM SET checkpoint_timeout = '15min';
ALTER SYSTEM SET max_wal_size = '6GB';
ALTER SYSTEM SET min_wal_size = '1GB';
SELECT pg_reload_conf();          -- all reloadable
```

## How big pg_wal actually gets
Roughly `max_wal_size` + `wal_keep_size` + WAL retained by **replication slots** + WAL not yet
archived (a rule of thumb). Slots (default `max_slot_wal_keep_size = -1`) and a failing archiver are unbounded:
the docs warn that pg_wal keeps filling until archiving works, and a full pg_wal volume ends in a PANIC shutdown. Size the volume for the sum plus headroom for bursts such as
index builds and bulk loads.

## Trade-offs
- Larger values mean longer **crash recovery** (more WAL to replay since the last
  checkpoint); usually tolerable, but measure recovery time if RTO is tight.
- Longer checkpoint intervals reduce full-page writes (the first change to a page after each checkpoint logs the whole page; docs, "WAL Configuration"), which can cut WAL volume.

## Verify
After a day, `num_requested` is a small fraction of `num_timed`, no "too frequently" log
lines, and pg_wal stays well inside its volume.

## Checked
- PostgreSQL 18.6: defaults from `pg_settings`: `max_wal_size` 1024 MB, `min_wal_size` 80 MB, `checkpoint_timeout` 300 s, `checkpoint_warning` 30 s, `checkpoint_completion_target` 0.9, `max_slot_wal_keep_size` -1, `wal_keep_size` 0; all of max_wal_size, min_wal_size, checkpoint_timeout have context `sighup`; the `ALTER SYSTEM` block with 15min / 6GB / 1GB applied on reload with nothing pending restart. `SELECT num_timed, num_requested FROM pg_stat_checkpointer` and `SELECT wal_bytes FROM pg_stat_wal` ran. With `max_wal_size = 32MB`, `checkpoint_warning = 300s` and a bulk insert plus update, the log showed `checkpoints are occurring too frequently (0 seconds apart)` with `HINT: Consider increasing the configuration parameter "max_wal_size".` and `num_requested` rose to 16.
- PostgreSQL 16.15: `SELECT checkpoints_timed, checkpoints_req FROM pg_stat_bgwriter` runs there (columns moved to `pg_stat_checkpointer` in 17).
- Docs (wal-configuration, runtime-config-wal, continuous-archiving): checkpoint triggers and defaults, `min_wal_size` recycling, full-page-write note, `checkpoint_warning` wording and default, pg_wal fills while archiving fails and a full volume causes a PANIC shutdown. The 1.5-2x sizing factor is labelled as a rule of thumb.
