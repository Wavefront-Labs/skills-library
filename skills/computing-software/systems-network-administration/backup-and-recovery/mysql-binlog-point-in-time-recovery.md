---
id: computing-software.systems-network-administration.backup-and-recovery.mysql-binlog-point-in-time-recovery
name: mysql-binlog-point-in-time-recovery
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [binlog-pitr, mysql, mariadb, point-in-time-recovery, mysqlbinlog, database-backup]
level: advanced
status: docs-checked
description: "Recover MySQL 8.4 to a point in time from binary logs: binlog settings, backup position, streaming binlogs off-host, and replaying up to just before a bad statement."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/point-in-time-recovery-positions.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysqlbinlog.html
  - https://dev.mysql.com/doc/refman/8.4/en/replication-options-binary-log.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MySQL binlog point-in-time recovery

**Goal:** restore to the second before someone ran `DELETE FROM orders` without a `WHERE`.

## Prerequisites (my.cnf)
```
log_bin = /var/lib/mysql-binlog/binlog
binlog_expire_logs_seconds = 1209600     # >= interval between full backups + margin
```
In MySQL 8.4 binary logging is on by default (except in a data directory initialised manually with `--initialize`), `binlog_format` defaults to `ROW` (the variable is deprecated), and `binlog_expire_logs_seconds` defaults to 2592000 (30 days). Replication topologies need a unique nonzero `server_id` on each server.

## Full backup that records its position
```sh
mysqldump --single-transaction --source-data=2 --routines --events --all-databases | gzip > full.sql.gz
# --master-data is a deprecated alias for --source-data in the 8.4 manual.
```
With value 2 the `CHANGE REPLICATION SOURCE TO` statement (with the binary log file name and position) is written as an SQL comment, informative only; with value 1 (the default if no value is given) it is not a comment and takes effect on reload.

## Keep binlogs off the server
```sh
mysqlbinlog --read-from-remote-server --host=db01 --user=binlog_ro --raw --stop-never \
  --result-file=/backup/binlogs/ binlog.000123
```
`--read-from-remote-server` needs an account with the `REPLICATION SLAVE` privilege; `--raw` writes one output file per log file read, and `--stop-never` keeps the connection open after the last file. Losing the server should not lose the logs since the last full.

## Find the bad event
```sh
mysqlbinlog --base64-output=DECODE-ROWS -v --start-datetime="2026-10-17 14:00:00" binlog.000124 | less
# note the "# at <pos>" before the bad transaction, e.g. 98765
```

## Recover
```sh
gunzip < full.sql.gz | mysql                     # on a recovery instance
mysqlbinlog --start-position=4567 binlog.000123 binlog.000124 --stop-position=98765 | mysql
# skip the bad transaction and continue if needed:
mysqlbinlog --start-position=<pos after bad trx> binlog.000124 binlog.000125 | mysql
```
With GTIDs, `--exclude-gtids='uuid:1234'` omits the transaction groups in the given GTID set from the output.

## Gotchas
- `--start-position` applies to the first log file named and `--stop-position` to the last; positions are per file.
- Pipe all the log files you need through a single `mysql` session (`mysqlbinlog binlog.000123 binlog.000124 | mysql`): the server drops temporary tables when a session ends, so a later file that uses a temporary table created in an earlier one fails if replayed separately.
- The manual advises using `--start-datetime` and `--stop-datetime` only to find positions, not to select the range to apply, because events can be missed; use positions.
- Recover to a separate instance first, then copy back the affected rows if only one table was hit.

## Verify
Quarterly drill: restore full + binlogs to a timestamp on a test host and compare row counts with the expected values at that time.

## Checked

Checked 2026-10-27 against the MySQL 8.4 Reference Manual pages for point-in-time recovery by positions, mysqlbinlog, binary log server options and mysqldump. Confirmed: `--source-data` values 1 and 2 and `--master-data` as a deprecated alias, binary logging on by default, `binlog_format` default ROW (deprecated), `binlog_expire_logs_seconds` default 2592000, the mysqlbinlog options `--read-from-remote-server`, `--raw`, `--stop-never`, `--result-file`, `--base64-output=DECODE-ROWS`, `--verbose`, `--start-position`, `--stop-position`, `--exclude-gtids`, the single-session rule for temporary tables, and the manual's advice to use datetime options only to locate positions. MariaDB option names differ and were not checked. Removed the unconfirmed `sync_binlog` setting, the XtraBackup file name and version-specific `--master-data` remark.

Method: documentation only; no commands were run.
