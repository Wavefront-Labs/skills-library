---
id: computing-software.database-administration.mysql.reading-binary-logs-with-mysqlbinlog
name: reading-binary-logs-with-mysqlbinlog
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-server-logs, binlog, mysqlbinlog, mysqlbinlog-decode, forensics, who-deleted]
level: practitioner
status: verified
description: "Decode MySQL binary logs with mysqlbinlog to find who changed what and when: row decoding, time and position filters, GTID ranges and remote reading."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/mysqlbinlog.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysqlbinlog-row-events.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading binary logs with mysqlbinlog

## Which file covers the time window
```sql
SHOW BINARY LOGS;                    -- names and sizes
SHOW BINLOG EVENTS IN 'binlog.000123' LIMIT 20;
```
File modification times (`ls -l --time-style=full-iso $datadir/binlog.*`) give rough ranges.

## Decode ROW events into readable pseudo-SQL
```bash
mysqlbinlog --base64-output=DECODE-ROWS -vv \
  --start-datetime='2026-10-18 09:00:00' --stop-datetime='2026-10-18 09:30:00' \
  /var/lib/mysql/binlog.000123 > /tmp/decoded.txt
```
Output shows `### DELETE FROM shop.orders ### WHERE ### @1=1001 ### @2='2026-10-01' ...`
with `@N` = column position (map with `SHOW CREATE TABLE`). `-vv` adds column types as comments (`@1=1 /* INT meta=0 nullable=0 is_null=0 */`);
`binlog_rows_query_log_events=ON` on the server includes the original SQL as a plain comment line, for example `# update orders set note='changed' where id=2` (no `Query:` label; 9.7.4). With `binlog_row_image=MINIMAL` the `WHERE` part shows only the primary key column and `SET` only the changed columns.

Find a culprit:
```bash
grep -n -B2 -A10 'DELETE FROM `shop`.`orders`' /tmp/decoded.txt | head -50
```
Each transaction header shows `SET TIMESTAMP=`, `server id`, `GTID_NEXT`, and the
`thread_id` (match to `performance_schema` history or the general log to get the user;
the binlog itself has no user name).

## Filters
| Option | Use |
|---|---|
| `--start-position / --stop-position` | exact event offsets (from `SHOW BINLOG EVENTS` or the decoded `# at N`) |
| `--start-datetime / --stop-datetime` | relative to the local time zone of the machine running mysqlbinlog (manual) |
| `--database=db` | one database only (last one wins), local files only; keyed to the default database set by `USE`, with different rules for statement and row formats (see the manual's --database entry) |
| `--include-gtids / --exclude-gtids` | GTID sets, e.g. skip one bad transaction during PITR |
| `--skip-gtids` | strip GTIDs from the output so it can be replayed on a server with its own GTIDs (the output kept only a trailing `GTID_NEXT= 'AUTOMATIC'` line instead of five `GTID_NEXT` settings) |
| `--read-from-remote-server -h src -u repl` | read from a running server instead of files (worked on 9.7.4: `mysqlbinlog --read-from-remote-server -h127.0.0.1 -P33061 -uroot binlog.000006`; add `--raw --result-file=<dir>/` to copy files) |

## Replaying (PITR)
```bash
mysqlbinlog --start-position=4567 --stop-position=98765 binlog.000123 binlog.000124 | mysql -u root -p
```
Pass **all** files in one invocation so temporary tables and session state carry across.
Never pipe a `--base64-output=DECODE-ROWS` output into mysql; it contains no executable row data (the row changes appear only as `### ...` comment lines).

## Gotchas
- Binlog encryption (`binlog_encryption=ON`) means you must read via
  `--read-from-remote-server`; mysqlbinlog cannot read encrypted files directly (manual; no keyring was set up here to run it).
- Compressed transaction payloads (8.0.20+) are decoded transparently: with `binlog_transaction_compression=ON` the rows still printed as `### INSERT` on 9.7.4.
- Use the mysqlbinlog that ships with the server version you are reading: the manual notes older mysqlbinlog versions do not even recognise an encrypted file as a binary log.

## Verify
For the time window in question, the decoded output contains the transaction (by GTID and
timestamp) you are looking for, and table/column mapping matches `SHOW CREATE TABLE`.
