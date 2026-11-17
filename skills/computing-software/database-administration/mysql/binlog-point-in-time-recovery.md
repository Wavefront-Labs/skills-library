---
id: computing-software.database-administration.mysql.binlog-point-in-time-recovery
name: binlog-point-in-time-recovery
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, mysqlbinlog-pitr, point-in-time-recovery, mysqlbinlog, binlog, stop-datetime, exclude-gtids, accidental-delete]
level: practitioner
status: verified
description: "Recover MySQL to just before a bad DROP/DELETE: restore the last full backup, then replay binlogs with mysqlbinlog up to a position, datetime or GTID."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/point-in-time-recovery.html
  - https://dev.mysql.com/doc/refman/8.4/en/point-in-time-recovery-positions.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysqlbinlog.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Point-in-time recovery from the binary log

**Goal:** undo `DROP TABLE orders` at 14:07:12 by rebuilding the server state as of 14:07:11.

## 0. Stop the damage
Stop writes (app off / `SET GLOBAL super_read_only = ON`). Copy the binlogs somewhere safe (`SHOW BINARY LOGS;`, files in datadir) before anything purges them.

## 1. Find the bad event
```bash
mysqlbinlog --base64-output=decode-rows -vv --start-datetime="2026-10-16 14:00:00" binlog.000231 | grep -n -B5 -i 'drop table'
```
Note the `SET @@SESSION.GTID_NEXT= 'uuid:N'` line and the position of the **GTID event that starts the DROP transaction**: it is the `# at <pos>` line above the `GTID` event (equal to the previous transaction's last `end_log_pos`; `1109` in a 9.7.4 test, where the `DROP TABLE` query event itself was at `1186`). Use the GTID event position, not the query event's, as the stop position, so the transaction is excluded whole.

## 2. Restore the base backup to a NEW server (or the same, after moving the datadir aside)
From mysqldump: the dump's `CHANGE REPLICATION SOURCE TO ... SOURCE_LOG_FILE='binlog.000229', SOURCE_LOG_POS=157` comment is the start point. From XtraBackup: `xtrabackup_binlog_info`.

## 3. Replay up to the bad event
Position-based:
```bash
mysqlbinlog --start-position=157 binlog.000229 binlog.000230 > replay.sql
mysqlbinlog --stop-position=<pos of the GTID event that starts the DROP transaction> binlog.000231 >> replay.sql
mysql -u root -p < replay.sql
```
GTID-based (skip only the bad transaction, keep everything after it):
```bash
mysqlbinlog --skip-gtids=false --exclude-gtids='3E11FA47-71CA-11E1-9E33-C80AA9429562:9811' \
  binlog.000229 binlog.000230 binlog.000231 binlog.000232 | mysql -u root -p
```
The restored server's `gtid_executed` (from the backup) makes already-applied GTIDs skip automatically, but only for transactions whose default database exists on the target: in a test, replaying an older file that began with `use `shop``, with no `shop` database on the target, failed with `ERROR 1049 Unknown database` even though that GTID was already executed. Start from the binlog file named in the dump's `CHANGE REPLICATION SOURCE TO` comment, not from older files.

Both routes were run on 9.7.4 (dump with `--source-data=2 --set-gtid-purged=ON`, replay into a second server): the position route with `--start-position=198 --stop-position=1109` restored the 4 rows in `orders` and the earlier rows of the neighbouring table; the GTID route with `--exclude-gtids` for the DROP's GTID applied the later inserts too (`gtid_executed` ended as `...:1-220:222`, the gap being the excluded DROP).

## Rules
- Pipe all files in ONE mysqlbinlog invocation: temporary tables and multi-file transactions break if split across separate mysql runs.
- `--stop-datetime` is second-granular and stops at the first event whose timestamp is equal to or later than the value, so events stamped with exactly that second are NOT replayed (manual); it is relative to the local time zone of the machine running mysqlbinlog. Prefer positions/GTIDs.
- Disable binlogging of the replay on the target if it must not replicate: `mysqlbinlog ... | mysql --init-command="SET sql_log_bin=0"` (`--init-command` set `@@session.sql_log_bin` to 0 in a test; without `SUPER`, `SYSTEM_VARIABLES_ADMIN` or `SESSION_VARIABLES_ADMIN` the restore account gets error 1227).
- Binlog retention (`binlog_expire_logs_seconds`) must exceed the backup interval, or PITR has a gap.

## Recover just one table
Restore and replay on a scratch server, then `mysqldump` that table back into production.

## Verify
The dropped table exists with the row count it had at 14:07, and rows written after the incident (GTID route) are present.
