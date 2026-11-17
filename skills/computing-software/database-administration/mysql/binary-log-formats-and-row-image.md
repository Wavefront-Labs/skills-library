---
id: computing-software.database-administration.mysql.binary-log-formats-and-row-image
name: binary-log-formats-and-row-image
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-server-logs, binlog, binlog-format, binlog-row-image, binlog-transaction-compression, replication]
level: practitioner
status: verified
description: "Choose MySQL binlog_format (ROW vs STATEMENT vs MIXED) and binlog_row_image, and control binlog size with compression and binlog_row_value_options."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/binary-log-formats.html
  - https://dev.mysql.com/doc/refman/8.4/en/replication-options-binary-log.html
  - https://dev.mysql.com/doc/refman/8.4/en/binary-log-transaction-compression.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary log formats and binlog_row_image

## binlog_format
| Format | Logs | Use |
|---|---|---|
| `ROW` (the default; `@@binlog_format` is `ROW` on 9.7.4) | changed row images | safe for all statements; required by gh-ost, Debezium/CDC, Group Replication |
| `STATEMENT` | SQL text | small binlogs for bulk UPDATEs, but non-deterministic statements (`UUID()`, `LIMIT` without ORDER BY, `NOW()` in some contexts, triggers) can diverge on replicas |
| `MIXED` | statement unless unsafe, then row | legacy compromise |
`binlog_format` is marked deprecated in the 8.4 manual (and still present, default ROW, on 9.7.4); keep ROW unless you
have a measured reason. Group Replication needs ROW (8.4 requirements page), gh-ost works on row-based logs (its docs) and the Debezium MySQL connector requires `binlog_format=ROW` and `binlog_row_image=FULL` (its docs).

## binlog_row_image
| Value | Before image | After image |
|---|---|---|
| `FULL` (default) | all columns | all columns |
| `MINIMAL` | PK (or all if no PK) | only changed columns |
| `NOBLOB` | like FULL but skips unchanged BLOB/TEXT | |
`MINIMAL` shrinks binlogs a lot on wide tables (on 9.7.4 an `UPDATE` of one column logged `WHERE @1=3` and `SET @2='min'` instead of all four columns before and after), but **CDC tools usually need FULL** (Debezium
requires it, see above), and tables without a primary key must log every column in the before image
anyway (documented; the PK-less case was not run here). Also used by `binlog_row_value_options = PARTIAL_JSON` to log only changed JSON paths.

## Size control
```sql
SET PERSIST binlog_transaction_compression = ON;          -- zstd per transaction (8.0.20+); default OFF
SET PERSIST binlog_transaction_compression_level_zstd = 3;
SET PERSIST max_binlog_size = 1073741824;                  -- rotation size (1GB max)
SET PERSIST binlog_expire_logs_seconds = 604800;           -- 7 days retention
```
Compressed payloads are replicated compressed (saves network) and are decompressed on apply (manual: decompressed by the applier, by `mysqlbinlog` replay and by `SHOW BINLOG EVENTS`). Compression level is 1 to 22, default 3. With it ON on 9.7.4, `mysqlbinlog -v` still printed the `### INSERT` rows.

## Other settings that matter
- `sync_binlog = 1` (default): fsync per commit group, required for crash safety with
  `innodb_flush_log_at_trx_commit = 1`.
- `binlog_rows_query_log_events = ON`: include the original SQL as a `Rows_query` event in ROW
  logs; `mysqlbinlog` prints it as a comment line `# <the statement>` (handy for auditing and `mysqlbinlog -vv`). Default is OFF.
- `log_replica_updates = ON` (default 8.0+) for chained replicas and failover candidates.
- `binlog_cache_size` / `Binlog_cache_disk_use` status: transactions spilling to disk.

## Gotchas
- The format cannot be changed inside a stored function or trigger, per session while that session has open temporary tables, and globally while any replication channel has open temporary tables or an applier thread is running (8.4 manual): stop replication first on a replica.
- A single `UPDATE` touching 10M rows in ROW format writes 10M row events: batch large DML.
- Tables without a primary key make replicas apply ROW events with full scans: add PKs
  (`sql_require_primary_key = ON` guards new tables).

## Verify
`SHOW BINARY LOGS;` sizes before/after, and `mysqlbinlog -vv --base64-output=DECODE-ROWS`
on a recent file shows the expected row images.
