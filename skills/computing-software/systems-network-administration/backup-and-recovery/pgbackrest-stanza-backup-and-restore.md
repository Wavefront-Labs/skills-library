---
id: computing-software.systems-network-administration.backup-and-recovery.pgbackrest-stanza-backup-and-restore
name: pgbackrest-stanza-backup-and-restore
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [pgbackrest-stanza, pgbackrest, postgresql, point-in-time-recovery, database-backup, wal-archiving]
level: advanced
status: docs-checked
description: "Back up PostgreSQL with pgBackRest: stanza config, WAL archive_command, full/diff/incr backups, retention, S3 repos with encryption, delta and PITR restores, and checks."
sources:
  - https://pgbackrest.org/user-guide.html
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pgBackRest

## Config (`/etc/pgbackrest/pgbackrest.conf`)
```ini
[global]
repo1-type=s3
repo1-s3-bucket=pg-backups
repo1-s3-endpoint=s3.eu-west-1.amazonaws.com
repo1-s3-region=eu-west-1
repo1-path=/pgbackrest
repo1-retention-full=4
repo1-retention-diff=7
repo1-cipher-type=aes-256-cbc
repo1-cipher-pass=<long-random-secret>
process-max=4
compress-type=zst
start-fast=y

[main]
pg1-path=/var/lib/postgresql/16/main
```
Credentials via `repo1-s3-key`/`-secret` or instance role (`repo1-s3-key-type=auto`).
A second repo (`repo2-*`, e.g. local disk or another region) gives two copies. `compress-type` accepts `none`, `bz2`, `gz`, `lz4` and `zst` (lz4 and zst are not available on all platforms); `repo1-cipher-type` is `none` (default) or `aes-256-cbc`, and encryption is always client-side. `repo1-s3-key-type` takes `shared`, `auto`, `web-id`, `pod-id` or `process`.

## PostgreSQL settings
```
archive_mode = on
archive_command = 'pgbackrest --stanza=main archive-push %p'
wal_level = replica
```
Restart PostgreSQL, then:
```sh
sudo -u postgres pgbackrest --stanza=main stanza-create
sudo -u postgres pgbackrest --stanza=main check        # verifies archiving end-to-end
```

## Backups
```sh
pgbackrest --stanza=main --type=full backup
pgbackrest --stanza=main --type=diff backup
pgbackrest --stanza=main --type=incr backup
pgbackrest info --stanza=main                          # backups, WAL range, sizes
```
Schedule (cron/systemd): weekly full, daily diff, hourly incr as needed. Retention expires
backups and their WAL automatically (`expire` runs after backup). Backups can run from a
standby (`backup-standby=y`) to offload the primary.

## Restore
```sh
systemctl stop postgresql
# fast in-place restore reusing unchanged files
sudo -u postgres pgbackrest --stanza=main --delta restore
# point in time
sudo -u postgres pgbackrest --stanza=main --delta --type=time "--target=2026-10-18 10:06:30+00" --target-action=promote restore
systemctl start postgresql
```
Restore to another host/path with `--pg1-path`. `--type` also accepts `lsn` (PostgreSQL 10+), `xid`, `name`, `immediate`, `default`, `preserve`, `standby` and `none`; avoid `none` because the timeline is not incremented. `--target-action` is `pause`, `promote` or `shutdown`. If the target is before the latest backup and the type is not `time` or `lsn`, select the backup with `--set`.

## Gotchas
- `archive_command` failures fill `pg_wal` and can stop the database: monitor
  `pg_stat_archiver.failed_count` and disk usage.
- Losing `repo1-cipher-pass` makes backups unrecoverable: escrow it.
- Version upgrades (major PG) need `stanza-upgrade` after pg_upgrade.

## Verify
`pgbackrest check` passes; `info` shows recent backups and continuous WAL; monthly PITR
restore to a scratch host succeeds and data matches the target time.

## Checked

Checked 2026-10-27 against the pgBackRest documentation sources in pgbackrest/pgbackrest (doc/xml/reference.xml and doc/xml/user-guide.xml; latest release 2.60.0). Confirmed: `compress-type` values, `repo-cipher-type` values and client-side encryption, `repo-s3-key-type` values, `backup-standby`, `start-fast`, automatic `expire` after a successful backup, `stanza-create`, `stanza-upgrade` and `check` commands, restore `--type` and `--target-action` values, `--target` and `--set` semantics, the `archive_command` form with `archive-push`, and the warning against `type=none`. Removed the unconfirmed `max_wal_senders` setting.

Method: documentation only; no commands were run.
