---
id: computing-software.database-administration.mysql.innodb-configuration-and-tuning
name: innodb-configuration-and-tuning
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, percona-server, innodb, my-cnf, innodb-buffer-pool-size, innodb-redo-log-capacity, innodb-log-file-size, innodb-flush-log-at-trx-commit, sync-binlog, innodb-flush-method, o-direct, innodb-io-capacity, slow-query-log, long-query-time, pt-query-digest, performance-schema, sys-schema, statement-analysis, mysqltuner, performance-tuning, durability, redo-log]
level: advanced
status: docs-checked
description: "Size the InnoDB buffer pool and redo log (innodb_redo_log_capacity vs innodb_log_file_size), set flush/durability options, and find slow SQL with the slow log and sys schema."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-configuration.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-redo-log.html
  - https://dev.mysql.com/doc/refman/8.4/en/slow-query-log.html
  - https://dev.mysql.com/doc/refman/8.4/en/sys-schema.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InnoDB configuration and tuning — buffer pool, redo, durability, then the queries

**Goal:** give InnoDB the memory and redo capacity it needs, choose durability
settings deliberately, and find the statements that consume the server.

## 1. Baseline `my.cnf` for a dedicated server
```ini
[mysqld]
innodb_buffer_pool_size        = 24G     # ~60-75% of RAM on a dedicated box
innodb_buffer_pool_instances   = 8       # splits a large pool to reduce mutex contention
innodb_redo_log_capacity       = 4G      # MySQL 8.0.30+ (default 100MB)
innodb_flush_log_at_trx_commit = 1
sync_binlog                    = 1
innodb_flush_method            = O_DIRECT  # Linux; avoids double buffering
innodb_io_capacity             = 2000    # SSD; raise for NVMe
innodb_io_capacity_max         = 4000
innodb_file_per_table          = ON
max_connections                = 500     # each thread has per-session buffers
```
MySQL 8.0+ has `innodb_dedicated_server = ON`, which auto-sizes the buffer pool (from
RAM) and the redo log capacity (from CPU count). Fine for a VM that only runs MySQL;
do not use it on shared hosts. The buffer pool also resizes online
(`SET GLOBAL innodb_buffer_pool_size = ...`) in chunks of
`innodb_buffer_pool_chunk_size × instances` (chunk default 128M).

Check the buffer pool is big enough: the miss ratio
`Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests` (from
`SHOW GLOBAL STATUS`) should be well under 1%; also watch `Innodb_buffer_pool_wait_free`
(should stay 0).

## 2. Redo log sizing (version matters)
| Version | Setting | Change needs |
|---|---|---|
| MySQL ≤ 8.0.29 | `innodb_log_file_size` (× `innodb_log_files_in_group`; both deprecated from 8.0.30) | restart |
| MySQL 8.0.30+ | `innodb_redo_log_capacity` (total) | `SET GLOBAL`, online |

Rule of thumb: enough redo for 1–2 hours of peak writes, measured rather than guessed.
On 8.0.30+:
```sql
SELECT VARIABLE_VALUE FROM performance_schema.global_status
 WHERE VARIABLE_NAME = 'Innodb_redo_log_current_lsn';  -- sample twice, 60s apart
```
LSN delta per minute × 60–120 = target capacity. Too-small redo shows up as stalls
from aggressive (sync) flushing. MariaDB has its own redo log handling; check its
documentation.

## 3. Durability trade-off
`innodb_flush_log_at_trx_commit=1` + `sync_binlog=1` is fully durable and the only
safe choice for primaries you will fail over. `=2` survives a mysqld crash but loses up
to ~1s on OS crash/power loss: acceptable on a rebuildable replica, not on a primary.
Never "fix" write latency this way without writing down the data-loss window.

## 4. Find the expensive statements
Slow log:
```sql
SET GLOBAL slow_query_log = ON;
SET GLOBAL long_query_time = 0.5;          -- seconds, fractional OK
SET GLOBAL log_queries_not_using_indexes = OFF;  -- noisy; enable briefly
```
Digest it with `pt-query-digest <slow.log>` (Percona Toolkit). It ranks by total time,
which is what matters.

Without file access, use `performance_schema` (on by default) via the `sys` schema:
```sql
SELECT query, exec_count, total_latency, avg_latency, rows_examined_avg
FROM sys.statement_analysis ORDER BY total_latency DESC LIMIT 20;
SELECT * FROM sys.statements_with_full_table_scans LIMIT 20;
SELECT * FROM sys.schema_unused_indexes;
SELECT * FROM sys.schema_redundant_indexes;
```
`rows_examined` far above rows sent means a missing or unused index. Follow up with
`EXPLAIN ANALYZE` on the worst ones; see
computing-software.database-administration.query-optimisation.reading-execution-plans.

## 5. Gotchas
- `query_cache` is gone in MySQL 8.0; MariaDB still has it but leave it off on
  write-heavy workloads (a global mutex).
- Per-session buffers (`sort_buffer_size`, `join_buffer_size`) are allocated per
  connection; raising them globally to "speed up sorts" is a common OOM cause. Defaults
  are usually right.
- Large `ALTER TABLE`: prefer `ALGORITHM=INSTANT`/`INPLACE` where supported, or
  `gh-ost`/`pt-online-schema-change`.
- MariaDB has diverged from MySQL 8.4 (redo log handling, `sys`/performance_schema
  defaults). Check the MariaDB documentation; do not copy MySQL 8.4 config blindly.
- Transparent huge pages and swap: disable THP, set `vm.swappiness=1`.

## Verify
- [ ] `SELECT @@innodb_buffer_pool_size/1024/1024/1024;` matches the plan.
- [ ] Buffer pool miss ratio < 1% at peak and `Innodb_buffer_pool_wait_free` = 0.
- [ ] Redo capacity covers at least an hour of measured peak LSN growth.
- [ ] Durability settings are 1/1 on every server that can become primary.
- [ ] Slow log or `sys.statement_analysis` top-20 reviewed and the worst queries explained.

## Checked

2026-10-31: confirmed innodb_redo_log_capacity (introduced in MySQL 8.0.30 per the 8.0.30 release notes, default 104857600 bytes, superseding the deprecated innodb_log_file_size/innodb_log_files_in_group), online buffer pool resizing in 128M chunks, innodb_dedicated_server auto-sizing (buffer pool 0.5/0.75 of RAM, redo capacity from CPU count) and its dedicated-host-only warning, the sys views statement_analysis (with rows_examined_avg), statements_with_full_table_scans, schema_unused_indexes, schema_redundant_indexes and metrics, and the slow log variables (long_query_time default 10, microsecond resolution) on dev.mysql.com 8.4 pages. Removed the MariaDB specifics (the cited MariaDB page moved) and unconfirmed version/default notes.
Method: documentation only; no commands were run.
