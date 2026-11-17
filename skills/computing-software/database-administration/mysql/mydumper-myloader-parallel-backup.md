---
id: computing-software.database-administration.mysql.mydumper-myloader-parallel-backup
name: mydumper-myloader-parallel-backup
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mydumper-myloader, mydumper, myloader, parallel-logical-backup, consistent-backup, mysql-backup]
level: practitioner
status: docs-checked
description: "Take fast parallel consistent logical backups of MySQL with mydumper and restore them with myloader: threads, chunking, compression and consistency options."
sources:
  - https://github.com/mydumper/mydumper
  - https://mydumper.github.io/mydumper/docs/html/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parallel logical backup with mydumper / myloader

mysqldump is single-threaded. mydumper dumps tables (and chunks of big tables) in parallel with one consistent snapshot; myloader restores in parallel. Practical for logical backups up to a few TB.

## Backup
```bash
mydumper --host db1 --user backup --ask-password \
  --outputdir /backup/shop-$(date +%F) \
  --database shop \
  --threads 8 \
  --rows 500000 \
  --compress --compress-protocol \
  --routines --events --triggers \
  --verbose 3 --logfile /backup/mydumper.log
```
`--rows` chunks big tables by primary-key ranges so several threads share one table.
Output: one schema file and one or more data files per table (`shop.orders.00000.sql.gz` with the default gzip compression; zstd is available), plus `metadata` with binlog file/position and GTID set at snapshot time — needed to start a replica or PITR from this backup.

## Consistency
mydumper synchronises all dump threads to one point in time with a global lock (`FLUSH TABLES WITH READ LOCK` by default; `--sync-thread-lock-mode` offers LOCK_ALL, NO_LOCK, SAFE_NO_LOCK and GTID alternatives), sends DDL locks (`LOCK INSTANCE FOR BACKUP`/`BACKUP STAGE START`) where supported, and uses Percona backup locks unless disabled with `--no-backup-locks`. Long-running queries block that lock and stall the server: check `SHOW PROCESSLIST` before nightly runs, or let mydumper kill/wait long queries (`--long-query-guard`, default 60 s, and `--kill-long-queries`).

## Restore
```bash
myloader --host db2 --user restore --ask-password \
  --directory /backup/shop-2026-10-18 \
  --threads 8 \
  --drop-table \
  --database shop_restored \
  --verbose 3
```
`--database` here restores into a different schema name.
myloader creates tables, loads data in parallel, then builds secondary indexes (with options to defer them), and finally loads triggers/routines.

## Speed tips
- Restore into a server with `innodb_flush_log_at_trx_commit = 2` and a larger `innodb_redo_log_capacity`; for disposable restores only, disable redo logging (`ALTER INSTANCE DISABLE INNODB REDO_LOG`, 8.0.21+) and re-enable it afterwards.
- Thread count around CPU cores on the target; I/O bound beyond that.

## Verify
- `metadata` file present and contains binlog/GTID positions.
- Restore test: row counts per table vs source (`SELECT table_name, table_rows` is approximate; use `COUNT(*)` on key tables) and `CHECKSUM TABLE` on small tables.

## Gotchas
- Tables without a primary key cannot be chunked by rows; one thread dumps them whole.
- Consistency and locking option names have changed between mydumper releases; read `mydumper --help` for the installed version before copying flags from older guides.

## Checked

2026-10-31: confirmed mydumper options -a/--ask-password, -o/--outputdir, -t/--threads, -r/--rows, -c/--compress (gzip default, zstd optional), -C/--compress-protocol, -R/--routines, -E/--events, -G/--triggers, -L/--logfile, -l/--long-query-guard (default 60 s) and -K/--kill-long-queries, and myloader options -d/--directory, -B/--database, -t/--threads (default 4), -v/--verbose, -o/--drop-table (modes FAIL/NONE/DROP/TRUNCATE/DELETE, default FAIL, bare flag = DROP) and --optimize-keys (index creation staged after import) on the mydumper usage docs; lock modes (FTWRL default via --sync-thread-lock-mode, DDL locks with LOCK INSTANCE FOR BACKUP/BACKUP STAGE START, --no-backup-locks) on the locks page; the metadata file with binlog position and GTID set and the database.table.chunk.sql file naming on the files page; ALTER INSTANCE {ENABLE|DISABLE} INNODB REDO_LOG introduced in MySQL 8.0.21 on the MySQL release notes. Replaced --overwrite-tables with the current --drop-table flag and the .zst example with the default gzip extension.
Method: documentation only; no commands were run.
