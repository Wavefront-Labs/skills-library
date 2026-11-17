---
id: computing-software.systems-network-administration.backup-and-recovery.postgresql-base-backup-and-pitr
name: postgresql-base-backup-and-pitr
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [database-backup, pg-basebackup, point-in-time-recovery, pitr, wal-archiving, pgbackrest, postgresql, recovery-target-time]
level: advanced
status: docs-checked
description: "Back up PostgreSQL for point-in-time recovery: WAL archiving, pg_basebackup or pgBackRest, restoring to a target time with recovery.signal, and verifying the chain."
sources:
  - https://www.postgresql.org/docs/current/continuous-archiving.html
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostgreSQL base backups and point-in-time recovery

**Goal:** restore a PostgreSQL cluster to any moment (e.g. one minute before a bad
`DELETE`), not just to last night's dump.

## Pieces
- **Base backup:** a physical copy of the data directory taken online.
- **WAL archive:** every completed WAL segment copied somewhere safe. Base backup + WAL
  replay = any point after the base backup.
- `pg_dump` is logical (per database, portable, no PITR); use it in addition, not instead.

## Configure WAL archiving
```ini
# postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'test ! -f "/backup/wal/%f" && cp "%p" "/backup/wal/%f"'   # form from the PostgreSQL manual; prefer pgBackRest
archive_timeout = 60          # force a segment switch at least every 60 s (bounds RPO)
```
Restart is needed for `archive_mode`. Monitor `pg_stat_archiver` (failed_count, last_failed_wal):
a failing archive_command makes `pg_wal` fill the disk, and the manual warns that if the file system holding `pg_wal` fills up PostgreSQL does a PANIC shutdown. The manual says an `archive_timeout` of a minute or so is reasonable; much shorter values bloat the archive.

## Base backup
```sh
pg_basebackup -h db01 -U replicator -D /backup/base/$(date +%F) -Ft -z -Xs -P --checkpoint=fast
```
Production setups usually use **pgBackRest** (or Barman/WAL-G): parallel, compressed,
encrypted, full/diff/incr, retention, repo on S3, `archive-push`/`archive-get`, and
`pgbackrest verify`:
```sh
pgbackrest --stanza=main --type=full backup
pgbackrest --stanza=main info
```

## Restore to a point in time (manual method)
1. Stop PostgreSQL; move the old data directory aside.
2. Extract the base backup into the data directory.
3. In `postgresql.conf` (PG 12+):
   `restore_command = 'cp "/backup/wal/%f" "%p"'`
   `recovery_target_time = '2026-10-16 14:02:00+00'`
   `recovery_target_action = 'promote'`
4. `touch $PGDATA/recovery.signal`; start PostgreSQL; it replays WAL to the target, then
   promotes. pgBackRest: `pgbackrest --stanza=main --type=time --target="2026-10-16 14:02:00+00" restore`.

## Gotchas
- A base backup without the WAL from its start to its end is useless; `-Xs` streams it.
- Restoring creates a new timeline; archive keeps both; later restores must pick the
  right one (`recovery_target_timeline`).
- Back up config files (`postgresql.conf`, `pg_hba.conf`) separately if outside PGDATA.

## Verify
Monthly: restore to a scratch host at a chosen timestamp and compare a known row count or
checksum; `pg_stat_archiver.failed_count` stays 0; newest archived WAL is under a minute old.

## Checked

Checked 2026-10-27 against the PostgreSQL documentation sources on the postgres/postgres master branch (doc/src/sgml/backup.sgml, ref/pg_basebackup.sgml, config.sgml) and the pgBackRest reference (pgbackrest/pgbackrest, release 2.60.0). Confirmed: the `archive_command` and `restore_command` forms, `archive_timeout` guidance, `archive_mode` and `wal_level` requirements, `recovery.signal`, the PANIC shutdown when the WAL file system fills, `pg_basebackup` `-Ft`, `--gzip`, `-X stream` as the default WAL method, and the pgBackRest `restore --type=time --target` form.

Method: documentation only; no commands were run.
