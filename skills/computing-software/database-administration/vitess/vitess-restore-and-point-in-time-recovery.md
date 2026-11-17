---
id: computing-software.database-administration.vitess.vitess-restore-and-point-in-time-recovery
name: vitess-restore-and-point-in-time-recovery
category: computing-software
field: database-administration
product: vitess
tags: [restore, point-in-time-recovery, pitr, restore-from-backup, bootstrap, incremental-backup, vtctldclient]
level: advanced
status: docs-checked
description: "Restore Vitess tablets: auto-restore on startup, bootstrapping flags, manual RestoreFromBackup, and restoring to a timestamp or GTID position from a full plus incremental chain."
sources:
  - https://vitess.io/docs/25.0/user-guides/operating-vitess/backup-and-restore/bootstrap-and-restore/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Auto restore: if vttablet starts with `--restore-from-backup` it is seeded from backup storage; without it the tablet starts empty like a new shard. Restores always use the engine that made the backup. If `--restore-to-timestamp` or `--restore-to-pos` is also given, it is a point-in-time recovery: the tablet picks a full backup plus incrementals, ends up in `DRAINED` type and does not begin replicating. Otherwise it restores the latest full backup, or with `--restore-from-backup-ts` the latest at or before that time. If no backup exists the tablet starts empty, unless `--wait-for-backup-interval` is above zero, in which case it keeps polling for one.
```sh
vttablet ... --backup-storage-implementation=file \
             --file-backup-storage-root=/nfs/XXX \
             --restore-from-backup
```
Bootstrapping a new tablet is the same but also set `--init-keyspace <keyspace>`, `--init-shard <shard>` and `--init-tablet-type replica|rdonly`; after the restore it restarts replication to catch up.

Manual restore shuts down the tablet's MySQL and wipes its data:
```shell
vtctldclient --server=<vtctld_host>:<vtctld_port> RestoreFromBackup <tablet-alias>
```
If the backup used `--include-binlogs`, the source's binary logs are restored too.

Point in time (assumes backups cover the target; the restore builds a path of one full backup then zero or more incrementals):
- Timestamp (v18 and later), RFC3339, applies events up to but excluding it at 1 second granularity: `vtctldclient RestoreFromBackup --restore-to-timestamp "2023-06-15T09:49:50Z" zone1-0000000100`
- Position, up to and including the exact GTID: `vtctldclient RestoreFromBackup --restore-to-pos "MySQL56/0d7aaca6-1666-11ee-aeaf-0a43f95f28a3:1-60" zone1-0000000102`
- `--dry-run` with either flag checks whether a restore path exists without restoring or changing the tablet; it exits with an error if there is no valid path: `vtctldclient RestoreFromBackup --dry-run --restore-to-timestamp "2023-06-15T09:49:50Z" zone1-0000000100`

## Checked

2026-11-04. Auto restore, bootstrap flags, manual restore and both PITR forms and the dry-run flag confirmed on the Bootstrap and Restore page.

Method: documentation only; no commands were run.
