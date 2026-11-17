---
id: computing-software.database-administration.mysql.metadata-locks-blocking-ddl
name: metadata-locks-blocking-ddl
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, online-schema-change, metadata-lock, waiting-for-table-metadata-lock, lock-wait-timeout, mdl, sys-schema-table-lock-waits, idle-transaction]
level: advanced
status: docs-checked
description: "Diagnose 'Waiting for table metadata lock' pile-ups in MySQL, find the idle transaction holding the MDL, and run DDL with lock_wait_timeout so it never stalls traffic."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/metadata-locking.html
  - https://dev.mysql.com/doc/refman/8.4/en/sys-schema-table-lock-waits.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metadata locks blocking DDL

**Goal:** a quick `ALTER TABLE` never turns into an outage because it queued
behind a forgotten transaction.

## The pile-up
1. Session A ran `SELECT ... FROM orders` inside a transaction and is idle (not
   committed). It holds a shared metadata lock (MDL) on `orders` until COMMIT.
2. Session B runs `ALTER TABLE orders ...` and needs an exclusive MDL: waits.
3. Every new query on `orders` queues **behind B** (`Waiting for table metadata
   lock` in the processlist). The table is effectively down.

## Find the blocker
```sql
SELECT * FROM sys.schema_table_lock_waits\G
-- columns: waiting_query, blocking_pid, blocking_thread_id, sql_kill_blocking_connection
SELECT object_name, lock_type, lock_status, owner_thread_id
FROM performance_schema.metadata_locks WHERE object_name = 'orders';
SELECT trx_mysql_thread_id, trx_started, trx_state, trx_query
FROM information_schema.innodb_trx ORDER BY trx_started;   -- the old idle one
```
The `wait/lock/metadata/sql/mdl` instrument must be enabled (default ON in 8.0).
Then `KILL <blocking_pid>;` or kill the DDL (cancels the queue instantly).

## Prevent
In every DDL session (and migration tool):
```sql
SET SESSION lock_wait_timeout = 5;    -- default is 31536000 seconds (1 year)!
ALTER TABLE orders ADD COLUMN ..., ALGORITHM=INSTANT;
```
On timeout, retry with backoff instead
of waiting. Also: kill idle-in-transaction sessions (`wait_timeout`,
application fixes), and avoid running DDL while long reports or backups run.

## Checked

2026-11-01. Confirmed against MySQL 8.4 manual pages metadata-locking, sys-schema-table-lock-waits (columns incl. blocking_pid, sql_kill_blocking_connection), performance-schema-metadata-locks-table, information-schema-innodb-trx-table, innodb-online-ddl-operations, server-system-variables (lock_wait_timeout range 1 to 31536000, default 31536000). Removed unconfirmed error number and mysqldump claim.

Method: documentation only; no commands were run.

## Gotchas
- Even INSTANT DDL needs the exclusive MDL briefly; "instant" does not mean "lock-free".
- `FLUSH TABLES WITH READ LOCK` (some backup tools) also waits behind long queries and blocks everything.
- Replicas apply DDL in the SQL thread; a long reporting query on a replica
  blocks replication there in the same way.

## Verify
During a test ALTER with an open transaction in another session, the ALTER fails
after 5 s with a lock wait timeout error and other queries on the table keep running.
