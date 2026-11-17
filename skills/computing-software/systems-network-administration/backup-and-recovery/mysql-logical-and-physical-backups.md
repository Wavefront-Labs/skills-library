---
id: computing-software.systems-network-administration.backup-and-recovery.mysql-logical-and-physical-backups
name: mysql-logical-and-physical-backups
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [mysqldump, xtrabackup, mariabackup, binlog, point-in-time-recovery, database-backup, mysql]
level: advanced
status: docs-checked
description: "Back up MySQL 8.4: mysqldump logical dumps with binlog coordinates, Percona XtraBackup full and incremental physical backups with prepare, and binlog point-in-time recovery."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html
  - https://docs.percona.com/percona-xtrabackup/8.4/xtrabackup-option-reference.html
  - https://dev.mysql.com/doc/refman/8.4/en/point-in-time-recovery.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MySQL logical and physical backups

**Goal:** a restorable MySQL backup at the right speed, plus binary logs for point-in-time recovery.

## Logical (mysqldump)
```bash
mysqldump --single-transaction --routines --triggers --events --source-data=2 \
  --all-databases | zstd > /backup/mysql-$(date +%F).sql.zst
```
- `--single-transaction` issues a `BEGIN` before dumping data; without it mysqldump needs `LOCK TABLES`. Read the manual's section on this option for its consistency limits with non-transactional tables.
- `--source-data=2` writes the `CHANGE REPLICATION SOURCE TO` statement (binary log file and position) as an SQL comment for PITR; value 1, the default if none is given, writes it as a live statement that takes effect on reload. `--master-data` is a deprecated alias in the 8.4 manual.

## Physical (Percona XtraBackup for MySQL)
```bash
xtrabackup --backup --target-dir=/backup/full-20261015 --user=bkp --password=...
xtrabackup --backup --target-dir=/backup/inc-20261016 --incremental-basedir=/backup/full-20261015
# restore
xtrabackup --prepare --apply-log-only --target-dir=/backup/full-20261015
xtrabackup --prepare --target-dir=/backup/full-20261015 --incremental-dir=/backup/inc-20261016
systemctl stop mysql && xtrabackup --copy-back --target-dir=/backup/full-20261015
chown -R mysql:mysql /var/lib/mysql && systemctl start mysql
```
`--prepare` performs recovery on a backup made with `--backup`; `--apply-log-only` is essential for incremental backups. By default a backup aborts if the source server's version is higher than the XtraBackup version (`--no-server-version-check` overrides this and may cause issues), so use an XtraBackup release that supports your server version.

## Point-in-time recovery with binlogs
Binary logging is on by default in MySQL 8.4; back up binlogs off-host continuously (e.g. `mysqlbinlog --read-from-remote-server --raw --stop-never`, which needs the `REPLICATION SLAVE` privilege). After restoring the base backup, replay by position:
```bash
mysqlbinlog --start-position=<from backup> --stop-position=<before bad event> binlog.000123 binlog.000124 | mysql
```
The manual advises using `--start-datetime`/`--stop-datetime` only to locate event positions, not to select the range to apply, because events can be missed. See the binlog point-in-time recovery skill for the full procedure.

## Gotchas
- Binlog retention (`binlog_expire_logs_seconds`, default 30 days in 8.4) must exceed the gap between base backups.

## Verify
Restore to a scratch server weekly and replay binlogs to a chosen position, then check the data.

## Checked

Checked 2026-10-27 against the MySQL 8.4 Reference Manual (mysqldump, mysqlbinlog, point-in-time recovery by positions, binary log options) and the Percona XtraBackup 8.4 option reference. Confirmed: `--source-data` values and `--master-data` as a deprecated alias, `--single-transaction` issuing `BEGIN` and `LOCK TABLES` otherwise, XtraBackup `--backup`, `--prepare`, `--apply-log-only`, `--incremental-basedir`, `--incremental-dir`, `--copy-back`, `--target-dir`, `--user`, `--password`, the default server-version check, binary logging on by default, the 30 day default binlog expiry, and the position-based replay advice. MariaDB, mariabackup and mydumper claims were removed because they were not checked.

Method: documentation only; no commands were run.
