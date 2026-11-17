---
id: computing-software.database-administration.mysql.xtrabackup-incremental-backups
name: xtrabackup-incremental-backups
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, xtrabackup, xtrabackup-incremental, physical-backup, apply-log-only, backup-restore]
level: practitioner
status: docs-checked
description: "Take and restore Percona XtraBackup incremental chains: base and incrementals by LSN, prepare with --apply-log-only in order, then copy back."
sources:
  - https://docs.percona.com/percona-xtrabackup/8.4/create-incremental-backup.html
  - https://docs.percona.com/percona-xtrabackup/8.4/prepare-incremental-backup.html
  - https://docs.percona.com/percona-xtrabackup/8.4/restore-a-backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XtraBackup incremental backups

Incrementals copy only InnoDB pages whose LSN is newer than the previous backup's
`to_lsn` (recorded in `xtrabackup_checkpoints`). Use a XtraBackup major version matching the
server (8.0 for MySQL 8.0, 8.4 for 8.4).

## Take the chain
```bash
# Sunday full
xtrabackup --backup --user=bkp --password=... --target-dir=/backups/full
# Monday incremental, based on full
xtrabackup --backup --user=bkp --password=... \
  --target-dir=/backups/inc1 --incremental-basedir=/backups/full
# Tuesday incremental, based on Monday
xtrabackup --backup --user=bkp --password=... \
  --target-dir=/backups/inc2 --incremental-basedir=/backups/inc1
cat /backups/inc2/xtrabackup_checkpoints     # backup_type = incremental, from_lsn, to_lsn
```
Alternative: `--incremental-lsn=<lsn>` when the previous backup directory is not local
(streamed to object storage). On big datasets, avoid scanning every page for changed LSNs by
using MySQL page tracking: `INSTALL COMPONENT "file://component_mysqlbackup";` on the server,
then add `--page-tracking` to the full and incremental backups.

Backup user privileges: `BACKUP_ADMIN, PROCESS, RELOAD, LOCK TABLES, REPLICATION CLIENT,
SELECT ON performance_schema.*` (plus `SELECT` on `performance_schema.keyring_component_status` if keyring).

## Prepare (order is everything)
```bash
xtrabackup --prepare --apply-log-only --target-dir=/backups/full
xtrabackup --prepare --apply-log-only --target-dir=/backups/full --incremental-dir=/backups/inc1
xtrabackup --prepare                  --target-dir=/backups/full --incremental-dir=/backups/inc2   # last one: no --apply-log-only
```
`--apply-log-only` skips the rollback of uncommitted transactions so the next incremental can
be applied. If you forget it on an intermediate step, later incrementals cannot be applied:
start over from copies. Prepare **modifies** the base directory: work on a copy if you want
to keep the chain reusable.

## Restore
```bash
systemctl stop mysqld
mv /var/lib/mysql /var/lib/mysql.old
xtrabackup --copy-back --target-dir=/backups/full      # or --move-back
chown -R mysql:mysql /var/lib/mysql
systemctl start mysqld
```
Then apply binary logs from the position in `xtrabackup_binlog_info` for point-in-time recovery.

## Gotchas
- Incrementals track InnoDB pages only; other engines' files are copied whole every time (as with MyRocks).
- Any break in the chain (lost inc1) makes later ones useless; keep checksums and test.
- Compressed/encrypted backups (`--compress`, `--encrypt`) need `--decompress` / `--decrypt`
  before prepare.
- Restore needs a compatible server version.

## Verify
After prepare, `xtrabackup_checkpoints` shows `backup_type = full-prepared` with `to_lsn`
equal to the last incremental; a restored test instance starts and row counts match source.

## Checked

2026-10-31: confirmed incremental LSN mechanics and the xtrabackup_checkpoints contents, --incremental-lsn, page tracking (INSTALL COMPONENT "file://component_mysqlbackup", --page-tracking on full and incremental backups, MySQL page tracking functions), the documented backup-user grants (BACKUP_ADMIN, PROCESS, RELOAD, LOCK TABLES, REPLICATION CLIENT plus SELECT on performance_schema tables), prepare with --apply-log-only ordering, --copy-back/--move-back with the datadir required empty and the server shut down, xtrabackup_binlog_info, --compress (zst output) with --decompress, --encrypt/--decrypt, --use-memory and --parallel on Percona XtraBackup 8.4 documentation pages. Removed the unconfirmed 8.0.27+ version note and the innodb_page_size restore requirement.
Method: documentation only; no commands were run.
