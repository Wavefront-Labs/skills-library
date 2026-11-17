---
id: computing-software.database-administration.mysql.bulk-loading-innodb-load-data
name: bulk-loading-innodb-load-data
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, load-data-infile, bulk-loading, unique-checks, foreign-key-checks, innodb-bulk-load, mysql-import]
level: practitioner
status: docs-checked
description: "Load large data sets into InnoDB fast with LOAD DATA, sorted primary keys, deferred secondary indexes, unique_checks/foreign_key_checks off, and safe settings."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/optimizing-innodb-bulk-data-loading.html
  - https://dev.mysql.com/doc/refman/8.4/en/load-data.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysqlimport.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bulk data loading for InnoDB

## LOAD DATA
```sql
LOAD DATA INFILE '/var/lib/mysql-files/orders.csv'
INTO TABLE orders
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(order_id, customer_id, @created, total)
SET created_at = STR_TO_DATE(@created, '%Y-%m-%d %H:%i:%s');
```
- Server-side file must sit under `secure_file_priv`; `LOAD DATA LOCAL INFILE` reads from the client (needs `local_infile` on server and client).
- Much faster than single-row INSERTs. Second best: multi-row INSERT batches in explicit transactions.
- `SHOW WARNINGS` after loading: truncations and conversions appear there; with strict mode errors abort instead.

## Session settings for the load
```sql
SET SESSION unique_checks = 0;          -- skip secondary unique checks via change buffer (only if data is known unique)
SET SESSION foreign_key_checks = 0;     -- skip FK checks (only if data is known valid)
SET SESSION sql_log_bin = 0;            -- only if the target is not a source for replicas you need consistent
START TRANSACTION; LOAD DATA ...; COMMIT;
SET SESSION unique_checks = 1, foreign_key_checks = 1;
```
Turning checks off with bad data gives you an inconsistent table with no error. Validate afterwards.

## Table-level tricks
- Load in **primary key order**: sorted input appends to the clustered index instead of random page splits.
- For big tables: create the table with only the PK, load, then add secondary indexes in one `ALTER TABLE ... ADD INDEX a(...), ADD INDEX b(...)` (sorted index build is much faster than maintaining them row by row).
- Split huge files and run several LOAD DATA sessions in parallel on different tables.

## Server settings (temporary, for initial loads)
```sql
SET GLOBAL innodb_flush_log_at_trx_commit = 2;
ALTER INSTANCE DISABLE INNODB REDO_LOG;   -- ONLY for disposable/new instances: a crash means re-initialise
-- after the load:
ALTER INSTANCE ENABLE INNODB REDO_LOG;
SET GLOBAL innodb_flush_log_at_trx_commit = 1;
```
Bigger `innodb_buffer_pool_size` and `innodb_redo_log_capacity` help most.

## Verify
`SELECT COUNT(*)` vs source line count, check FKs for orphans if checks were off:
```sql
SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON c.id = o.customer_id WHERE c.id IS NULL;
```

## Gotchas
- One giant transaction for a very large load grows undo and makes rollback take hours; commit in chunks for incremental loads.
- Replicas replay LOAD DATA (row events with row-based binlog): plan for lag.
- `mysqlimport` is a command-line wrapper around LOAD DATA.

## Checked

2026-11-01. Confirmed against MySQL 8.4 manual pages optimizing-innodb-bulk-data-loading (unique_checks, foreign_key_checks, primary key order, secondary indexes after load, redo log), load-data (syntax, LOCAL, IGNORE, SET), load-data-local-security, server-system-variables. Removed unconfirmed speed ratio, batch size, version gate, MySQL Shell and mysqlimport thread claims.

Method: documentation only; no commands were run.
