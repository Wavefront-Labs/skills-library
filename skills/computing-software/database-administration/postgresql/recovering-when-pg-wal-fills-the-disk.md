---
id: computing-software.database-administration.postgresql.recovering-when-pg-wal-fills-the-disk
name: recovering-when-pg-wal-fills-the-disk
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, wal-configuration, pg-wal-full, disk-full, replication-slots, archive-command, incident-response]
level: advanced
status: docs-checked
description: "Handle pg_wal filling the disk: find why WAL is retained (slot, failing archiver, wal_keep_size), free space safely, and never delete WAL files by hand."
sources:
  - https://www.postgresql.org/docs/current/wal-configuration.html
  - https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-MAX-SLOT-WAL-KEEP-SIZE
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ARCHIVER-VIEW
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recovering when pg_wal fills the disk

When the WAL volume is full the server cannot write WAL and stops; it will not restart until there is room.

## Rule zero
Do **not** delete files from `pg_wal` by hand; segments are removed or recycled by the server at checkpoints. Do not reach for `pg_resetwal` as a first step.

## Step 1: get a little space back without touching pg_wal
- Delete unrelated files on the same filesystem (old logs in `log/`, core dumps, backups
  someone left there).
- Grow the volume if your platform allows it.
- If pg_wal is a symlink to its own volume, that volume is what needs room.

## Step 2: find why WAL is retained (server running)
```sql
-- replication slots holding WAL
SELECT slot_name, slot_type, active, wal_status,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained
FROM pg_replication_slots ORDER BY restart_lsn;
-- archiver failing?
SELECT archived_count, failed_count, last_failed_wal, last_failed_time, last_archived_time
FROM pg_stat_archiver;
SHOW wal_keep_size; SHOW max_wal_size;
```
| Cause | Fix |
|---|---|
| inactive slot (dead standby, abandoned CDC/Debezium) | `SELECT pg_drop_replication_slot('name');` after confirming the consumer is gone; the consumer must be re-seeded |
| `archive_command` failing (bucket permissions, full archive disk) | fix the command; the archiver catches up and old segments are recycled at later checkpoints |
| huge `wal_keep_size` | lower it |
| long-running bulk load generating WAL faster than checkpoints recycle | wait for checkpoint, or `CHECKPOINT;` |

After fixing, run `CHECKPOINT;` and watch `pg_wal`: after a checkpoint, older segments can be recycled or removed, but with archiving they must be archived first.

## Step 3: prevent recurrence
- `max_slot_wal_keep_size = '<size>'` caps how much WAL replication slots may retain at checkpoint time (default -1 = unlimited); a standby whose slot falls further behind may no longer be able to continue replication (watch `wal_status` in `pg_replication_slots`).
- Alert on: pg_wal volume usage, `failed_count` increasing, slot retained bytes, inactive slots.
- Put pg_wal on a volume sized for `max_wal_size` + slot cap + headroom.
- An `archive_command` that returns 0 without archiving hides failures; test it.

## Verify
Server running, `pg_stat_archiver.failed_count` not increasing, pg_wal
size stable after a few checkpoints, standbys/CDC consumers reconnected or rebuilt.

## Checked

2026-10-28. Confirmed against PostgreSQL docs (version 18): WAL configuration (segments recycled or removed after a checkpoint, must be archived first, WAL accumulates when archive_command fails or a slot is stuck), max_slot_wal_keep_size (default -1 unlimited), pg_stat_archiver columns, pg_replication_slots.wal_status. Removed unconfirmed: the PANIC message text, pg_resetwal and unrecoverable-cluster claim, .ready counting, PG13+ tag, numeric alert thresholds, space-needed estimate, xfs_growfs/resize2fs.

Method: documentation only; no commands were run.
