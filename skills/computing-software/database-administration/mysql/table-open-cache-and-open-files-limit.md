---
id: computing-software.database-administration.mysql.table-open-cache-and-open-files-limit
name: table-open-cache-and-open-files-limit
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, table-open-cache, open-files-limit, table-definition-cache, opened-tables, file-descriptors, mysql-tuning]
level: practitioner
status: docs-checked
description: "Size MySQL table_open_cache, table_definition_cache and open_files_limit from Opened_tables rates, and fix 'Too many open files' errors."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/table-cache.html
  - https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html#sysvar_table_open_cache
  - https://dev.mysql.com/doc/refman/8.4/en/not-enough-file-handles.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table open cache and open_files_limit

## How it works
- `table_open_cache` (default 4000): number of open table handles across all sessions. Each concurrent use of a table needs its own handle: 200 connections joining 5 tables need up to 1000.
- `table_open_cache_instances` (default 16): cache is partitioned to reduce mutex contention.
- `table_definition_cache`: cached table definitions (.frm-less dictionary objects), default autosized; should be >= number of tables actively used.
- `open_files_limit`: file descriptors mysqld requests from the OS; bounded by the process limit (`LimitNOFILE` under systemd).

## Is it too small?
```sql
SHOW GLOBAL STATUS LIKE 'Open%table%';
-- Open_tables: currently open (near table_open_cache = full)
-- Opened_tables: cumulative opens; the RATE matters
SHOW GLOBAL STATUS LIKE 'Table_open_cache_%';
-- Table_open_cache_misses / _overflows rising fast = too small
SELECT @@table_open_cache, @@table_definition_cache, @@open_files_limit;
```
Rule of thumb: `Opened_tables` increasing by more than a few per second under steady load, or `Table_open_cache_overflows` growing, means raise the cache.

## Sizing
```ini
[mysqld]
table_open_cache = 8000
table_definition_cache = 4000       # >= tables in use (SELECT COUNT(*) FROM information_schema.tables)
open_files_limit = 65535
```
`SET PERSIST table_open_cache = 8000;` works online. mysqld lowers the effective `table_open_cache` when `open_files_limit` is too small (effective value = MAX((open_files_limit - 10 - max_connections) / 2, 400)); check the error log at startup.

## "Too many open files" (errno 24)
1. Check the real process limit: `cat /proc/$(pidof mysqld)/limits | grep 'open files'`.
2. Raise it with a systemd override (`LimitNOFILE=65535`), restart.
3. Confirm `SELECT @@open_files_limit;` reflects it.
InnoDB file-per-table with tens of thousands of tables also needs `innodb_open_files` big enough.

## Gotchas
- Huge caches (hundreds of thousands) waste memory and slow `FLUSH TABLES`.

## Checked

2026-10-31: confirmed table_open_cache default 4000 with the effective-value formula above, table_open_cache_instances default 16, table_definition_cache default -1 (autosized, MIN(400 + table_open_cache / 2, 2000)) and its role for InnoDB tablespaces with innodb_open_files, the 200-connections-x-N-tables sizing guidance and Opened_tables/Open_tables monitoring on the table-cache page, and open_files_limit (10 + max_connections + table_open_cache * 2, capped by ulimit or systemd LimitNOFILE) plus the errno 24 'Too many open files' error on the not-enough-file-handles page, all on dev.mysql.com 8.4. Removed the exact 'Changed limits' log message wording (not found in the cited pages).
Method: documentation only; no commands were run.
- Many-thousand-table schemas (one schema per tenant) are the usual reason; fixing the design beats endless cache growth.
