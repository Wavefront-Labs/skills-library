---
id: computing-software.database-administration.mysql.backup-and-restore-with-xtrabackup
name: backup-and-restore-with-xtrabackup
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, percona-xtrabackup, mysqldump, mydumper, hot-backup, incremental-backup, restore, innodb, backup-strategy]
level: advanced
status: docs-checked
description: "Take consistent hot InnoDB backups with Percona XtraBackup (full and incremental), and know when mysqldump or mydumper is the better tool instead."
sources:
  - https://docs.percona.com/percona-xtrabackup/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MySQL backups: XtraBackup, mysqldump, and mydumper — picking and running the right one

**Goal:** back up a live production InnoDB instance without blocking writes for the
backup's duration, and restore it correctly, including to a point in time.

## 1. Why not just mysqldump for anything beyond small databases
`mysqldump` is logical (SQL statements) — correct, portable across versions, but
slow to restore (replays every INSERT). For a consistent snapshot of InnoDB tables
use `--single-transaction`: it takes a REPEATABLE READ consistent snapshot without
blocking applications, but only InnoDB is consistent (MyISAM or MEMORY tables can
still change state), and it is mutually exclusive with `--lock-tables` (enabled by
default via `--opt`; override with `--skip-lock-tables`). A single-threaded
dump/restore of a large database can take many hours each way. Use it for: small
databases, schema/data export for migration, selective table dumps, or cross-version
upgrades where binary compatibility isn't guaranteed.
**mydumper/myloader** parallelizes the same logical approach and is meaningfully
faster for multi-GB databases — reach for it before XtraBackup if a logical (not
raw file) format is required.

## 2. XtraBackup: physical hot backup
Copies InnoDB data files directly while tracking the redo log, so it captures a
consistent point without requiring a global lock for the bulk of the copy:
```bash
xtrabackup --backup --target-dir=/backup/full-$(date +%F) \
  --user=root --password=... --parallel=4
xtrabackup --prepare --target-dir=/backup/full-2026-10-15
```
`--backup` copies files and replays redo entries generated during the copy;
`--prepare` applies them so the directory is restore-ready (a non-prepared backup
is not yet consistent). A brief `FLUSH TABLES WITH READ LOCK` (or backup locks,
which XtraBackup uses where the server supports them) is taken near the end, before
non-InnoDB files are copied and the binlog position recorded — not for the whole
backup. This is the entire reason XtraBackup exists over a filesystem snapshot
plus dump.

## 3. Incrementals
```bash
xtrabackup --backup --target-dir=/backup/inc1 \
  --incremental-basedir=/backup/full-2026-10-15
```
Restore order matters: prepare the full backup first with `--apply-log-only` (skip
final rollback so later increments can still apply), then prepare each incremental
in sequence with `--incremental-dir`, only doing the final full prepare (rollback)
on the very last one. Getting `--apply-log-only` wrong on an intermediate step is
the most common XtraBackup restore mistake — it leaves the chain unable to accept
further increments.

## 4. Restoring
```bash
# stop mysqld, empty datadir, then:
xtrabackup --copy-back --target-dir=/backup/full-2026-10-15
chown -R mysql:mysql /var/lib/mysql
# start mysqld
```
`--copy-back` refuses to overwrite a non-empty datadir (safety) — use
`--move-back` only when you don't need the backup directory afterward (it's
destructive to the source backup files).

## 5. Point-in-time recovery on top of a physical backup
XtraBackup restores to the exact moment the backup was taken. To go further
forward, note the binlog file/position captured in `xtrabackup_binlog_info` inside
the backup directory, restore the backup, then replay binlogs from that position
forward with `mysqlbinlog` piped into `mysql` (see the GTID/binlog skill for the
replay mechanics) up to just before the mistake.

## 6. Verifying backups actually work
A backup that was never restored is a hope, not a backup. Periodically restore to
a scratch instance and run `CHECK TABLE` / a row-count or checksum comparison
against production. Confirm `--prepare` completed without
`[ERROR] InnoDB: ... corrupt` in its log — a backup taken during heavy DDL can
occasionally need `--prepare` re-run with more memory (`--use-memory`) if it OOMs
mid-apply.

## Verify
- [ ] Full backups prepare cleanly (`--prepare` ends with "completed OK").
- [ ] Incremental chain was tested end-to-end on a scratch restore, not just taken.
- [ ] `xtrabackup_binlog_info` position is recorded and binlogs are retained past it.
- [ ] A scheduled restore drill has run in the last quarter and passed a data check.
- [ ] mysqldump/mydumper is used only where a logical, version-portable export is actually needed.

## Checked

2026-10-31: confirmed mysqldump --single-transaction semantics (REPEATABLE READ consistent snapshot, no blocking for InnoDB, non-transactional tables not consistent, mutual exclusion with --lock-tables, --skip-lock-tables as the --opt override) on the mysqldump reference; xtrabackup --backup/--prepare, --copy-back/--move-back with the datadir required empty, the FLUSH TABLES WITH READ LOCK stage (backup locks preferred where supported), xtrabackup_binlog_info (binary log coordinates for point-in-time recovery), --use-memory, --parallel and the Galera/PXC restore notes on Percona XtraBackup 8.4 pages. Dropped the unconfirmable 500 GB figure and reworded the locking description.
Method: documentation only; no commands were run.
