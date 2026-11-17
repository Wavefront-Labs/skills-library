---
id: computing-software.database-administration.mysql.mysqldump-single-transaction-consistent-backups
name: mysqldump-single-transaction-consistent-backups
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, mysqldump, single-transaction, consistent-backup, source-data, logical-backup, routines-triggers-events, gtid-purged]
level: practitioner
status: verified
description: "Take a consistent hot logical MySQL backup with mysqldump --single-transaction, record binlog/GTID position, and avoid the DDL and MyISAM traps."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html
  - https://dev.mysql.com/doc/refman/8.4/en/using-mysqldump.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consistent logical backups with mysqldump --single-transaction

**Goal:** a dump that is a consistent point-in-time copy of InnoDB data, taken while the app keeps writing, usable to seed replicas and for PITR.

## The command
```bash
mysqldump --single-transaction --source-data=2 --routines --triggers --events \
  --hex-blob --default-character-set=utf8mb4 --set-gtid-purged=AUTO \
  --all-databases | zstd -T0 > full-$(date +%F).sql.zst
```
(`--source-data` is 8.0.26+ (the 8.0.26 release notes list `master-data` getting the alias `source-data`); older: `--master-data=2`, which still works on 9.7.4 but prints `WARNING: --master-data is deprecated`. On 9.7.4 this command wrote `-- CHANGE REPLICATION SOURCE TO SOURCE_LOG_FILE='binlog.000004', SOURCE_LOG_POS=12325;` and `SET @@GLOBAL.GTID_PURGED=...`, and `--hex-blob` wrote `0x00FF` for a BLOB; `zstd` was not available here, so a plain `gzip` was used for the compressed copy.)

| Option | Why |
|---|---|
| `--single-transaction` | `START TRANSACTION WITH CONSISTENT SNAPSHOT` at REPEATABLE READ: InnoDB data consistent with no table locks |
| `--source-data=2` | Writes the binlog file/position as a comment; briefly takes `FLUSH TABLES WITH READ LOCK` to get it (the manual: the lock is released as soon as the coordinates are read) |
| `--routines --events` | Not dumped by default (triggers are) |
| `--set-gtid-purged` | Writes `SET @@GLOBAL.gtid_purged` for GTID replica seeding; use `OFF` when restoring into an existing GTID server you do not want to reset |
| `--hex-blob` | Binary-safe |

## Traps
- **Only InnoDB is consistent** (documented: `--single-transaction` only works for transactional tables). MyISAM tables in the dump are not; use `--lock-all-tables` if any exist (blocks writes). The manual also says `--single-transaction` and `--lock-tables` are mutually exclusive.
- **DDL during the dump**: the manual says no other connection should run `ALTER TABLE`, `CREATE TABLE`, `DROP TABLE`, `RENAME TABLE` or `TRUNCATE TABLE` because a consistent read is not isolated from them, so the dumped contents can be wrong or the SELECT can fail. Freeze schema changes during backups.
- `--source-data` FTWRL waits behind long-running queries and then blocks everything (manual: "the MySQL server may get stalled until those statements finish"); schedule away from long reports.
- Single-threaded: big databases take hours to dump and longer to restore (index builds). Past ~100 GB use mysqlsh dump utilities or XtraBackup.
- The `mysql` system schema in `--all-databases` restores users over the target; for cross-version moves dump users with `SHOW CREATE USER`/`mysqlsh util.dumpInstance` instead (the mysqlsh part was not run here). A restricted-privilege dump account on 9.7.4 failed on the `column_masking_policy` table and needed `--no-tablespaces` (or `PROCESS`).

## Restore
```bash
zstd -dc full-2026-10-16.sql.zst | mysql -u root -p
```
Speed up (not timed here): `SET GLOBAL innodb_flush_log_at_trx_commit=2; SET GLOBAL sync_binlog=0;` during the load on a non-replicating target (revert after: `sync_binlog=1` and `innodb_flush_log_at_trx_commit=1` are the durable settings per the manual). Replaying `full.sql` into an empty second server with `GTID_PURGED` in the dump needs that server's `gtid_executed` to be empty (use `RESET BINARY LOGS AND GTIDS` first on a scratch server).

## Verify
Restore into a scratch server weekly, compare row counts / `CHECKSUM TABLE` for key tables, and confirm the position comment exists: `zstd -dc dump.sql.zst | head -40 | grep -E 'CHANGE (MASTER|REPLICATION SOURCE)|GTID_PURGED'`.
