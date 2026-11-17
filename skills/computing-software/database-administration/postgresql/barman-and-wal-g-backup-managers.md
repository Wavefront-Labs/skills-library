---
id: computing-software.database-administration.postgresql.barman-and-wal-g-backup-managers
name: barman-and-wal-g-backup-managers
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, barman-backup-server, wal-g-backup-push, barman, wal-g, backup-retention, pitr, object-storage]
level: practitioner
status: gated
description: "Run PostgreSQL backups with Barman (dedicated backup server) or WAL-G (object storage): setup, WAL archiving, retention, restore and checks."
sources:
  - https://docs.pgbarman.org/
  - https://github.com/wal-g/wal-g/blob/master/docs/PostgreSQL.md
  - https://www.postgresql.org/docs/current/continuous-archiving.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Barman and WAL-G backup managers

| | Barman | WAL-G |
|---|---|---|
| Model | central backup server pulls from many PG servers | agent on the DB host pushes to object storage |
| Storage | local disk on backup server (optional cloud via barman-cloud) | S3/GCS/Azure/Swift, compressed + encrypted |
| Best for | on-prem fleets with a backup host | cloud, Kubernetes, many small clusters |

## Barman (streaming setup)
```ini
# /etc/barman.d/pg1.conf
[pg1]
description = "Main DB"
conninfo = host=pg1 user=barman dbname=postgres
streaming_conninfo = host=pg1 user=streaming_barman
backup_method = postgres
streaming_archiver = on
slot_name = barman
create_slot = auto
retention_policy = RECOVERY WINDOW OF 14 DAYS
```
```bash
barman check pg1                 # every line must be OK before trusting it
barman switch-wal --force --archive pg1
barman backup pg1
barman list-backups pg1
barman recover pg1 latest <RESTORE_DIR> --target-time "2026-10-18 09:00:00" --remote-ssh-command "ssh postgres@pg1-new"
barman cron                      # run every minute from cron: receive-wal, retention
```
Watch the replication slot: if Barman stops, the slot retains WAL on the primary until its disk fills (set `max_slot_wal_keep_size`).

## WAL-G
```bash
# environment (e.g. /etc/wal-g.env, loaded by the postgres user)
WALG_S3_PREFIX=s3://<BUCKET>/pg1
AWS_REGION=<REGION>
WALG_COMPRESSION_METHOD=zstd
WALG_LIBSODIUM_KEY_PATH=<KEY_FILE>        # client-side encryption
PGHOST=/var/run/postgresql
```
```ini
# postgresql.conf
archive_mode = on
archive_command = 'envdir /etc/wal-g.d wal-g wal-push %p'
restore_command = 'envdir /etc/wal-g.d wal-g wal-fetch %f %p'
```
```bash
wal-g backup-push <DATA_DIR>                 # full; set WALG_DELTA_MAX_STEPS for delta backups
wal-g backup-list --detail
wal-g delete retain FULL 7 --confirm         # keep 7 full backups and their WAL
wal-g backup-fetch <RESTORE_DIR> LATEST      # then recovery.signal + restore_command
wal-g wal-verify integrity timeline          # gaps in archived WAL
```

## Either tool: non-negotiables
- Monitor archive success (`pg_stat_archiver.failed_count`, `last_archived_time`) and backup age; alert if the newest full backup is older than the schedule.
- Restore-test on a schedule into a scratch host; a backup never restored is a hope.
- Keep encryption keys and object-storage credentials outside the backup they protect.

## Gotchas
- WAL-G `wal-push` failures make `archive_command` fail; pg_wal grows until fixed. Fix credentials/permissions fast.
- Barman with `rsync` backup method needs SSH both ways; `postgres` method (pg_basebackup) is simpler.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; Barman docs page unreadable (empty stub); WAL-G and PostgreSQL pages fetched but Barman options not checked. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
