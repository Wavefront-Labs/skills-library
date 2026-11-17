---
id: computing-software.database-administration.mysql.binary-log-expiry-and-purging
name: binary-log-expiry-and-purging
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, mysql-server-logs, binlog, binlog-expire-logs-seconds, purge-binary-logs, disk-full, binlog-retention, replica-safety]
level: practitioner
status: verified
description: "Control MySQL binary log disk usage with binlog_expire_logs_seconds and safe PURGE BINARY LOGS, without purging logs a replica or PITR backup still needs."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/replication-options-binary-log.html#sysvar_binlog_expire_logs_seconds
  - https://dev.mysql.com/doc/refman/8.4/en/purge-binary-logs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary log expiry and purging

**Goal:** binlogs never fill the disk, yet every replica and the PITR chain still
has the files it needs.

## Automatic expiry
```ini
[mysqld]
binlog_expire_logs_seconds = 604800     # 7 days (8.0 default 2592000 = 30 days)
max_binlog_size = 1G
```
Expiry runs whenever the binlog rotates (size reached or
`FLUSH BINARY LOGS`): on 9.7.4, with `binlog_expire_logs_seconds=1`, a `FLUSH BINARY LOGS` after a 2 second wait removed all older files and kept the previous current file. The default is 2592000 (30 days, checked). `expire_logs_days` no longer exists (`Unknown system variable` on 9.7.4), and `binlog_expire_logs_auto_purge = OFF` disables automatic purging and overrides the seconds setting (8.4 manual). Check MariaDB's own variable names in its docs before copying this to MariaDB (not run here).

Choose retention >= (longest replica downtime you want to survive) and >= the
interval between full backups + safety margin, if you use binlogs for PITR.

## Manual purge when the disk is filling
1. Find what replicas still need. On each replica:
   ```sql
   SHOW REPLICA STATUS\G     -- Source_Log_File = file being read (shown as `binlog.000008` on 9.7.4)
   ```
2. On the source, list files:
   ```sql
   SHOW BINARY LOGS;
   ```
3. Purge up to (not including) the oldest file any replica still reads, and
   make sure your binlog backup (e.g. `mysqlbinlog --read-from-remote-server
   --raw --stop-never`) has copied them:
   ```sql
   PURGE BINARY LOGS TO 'binlog.000412';
   PURGE BINARY LOGS BEFORE NOW() - INTERVAL 3 DAY;
   ```
Per the PURGE BINARY LOGS manual page, the statement is safe while replicas replicate: it keeps the file an active replica is reading (and later ones), deletes earlier ones and issues a warning. It does **not** protect a disconnected replica: on 9.7.4, after `STOP REPLICA IO_THREAD` on the replica, `PURGE BINARY LOGS TO 'binlog.000010'` removed files 7 to 9 that the replica still needed. Both `PURGE BINARY LOGS TO '<file>'` and `PURGE BINARY LOGS BEFORE NOW() - INTERVAL 3 DAY` ran as written (the second purged nothing because every file was newer).

## Never
- Delete binlog files from the filesystem by hand: `binlog.index` (one `.\binlog.00000N` line per file, seen in the data dir) still lists them. Use `PURGE BINARY LOGS`, which updates the index. (Hand-deletion was not tried here.)
- `RESET BINARY LOGS AND GTIDS` (`RESET MASTER` before 8.4; it ran on 9.7.4) on a source with
  replicas: wipes all binlogs and GTID history.

## Gotchas
- A transaction is written to one file, so a large transaction can exceed `max_binlog_size` (manual: the size is only checked before writing a group of transactions).
- `binlog_error_action` defaults to `ABORT_SERVER` (checked): a binlog write failure such as a full disk shuts mysqld down, so alert on free space before that.

## Verify
`SHOW BINARY LOGS;` oldest file date matches retention; replicas show
`Replica_IO_Running: Yes` after the purge. A replica whose next file was purged stops with `Last_IO_Errno: 13114`, "Got fatal error 1236 from source ... Cannot replicate because the source purged required binary logs" (reproduced on 9.7.4) and must be re-provisioned from a backup.
