---
id: computing-software.systems-network-administration.linux.mysql-and-postgresql-slow-query-logging
name: mysql-and-postgresql-slow-query-logging
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, slow-query-log, long-query-time, log-min-duration-statement, pg-stat-statements, pt-query-digest, auto-explain]
level: practitioner
status: draft
description: "Turn on and use slow query logging in MySQL/MariaDB and PostgreSQL: thresholds, auto_explain, pg_stat_statements and digesting logs with pt-query-digest."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/slow-query-log.html
  - https://www.postgresql.org/docs/current/runtime-config-logging.html
  - https://www.postgresql.org/docs/current/pgstatstatements.html
  - https://docs.percona.com/percona-toolkit/pt-query-digest.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Slow query logging

## MySQL / MariaDB
```sql
SET GLOBAL slow_query_log = ON;
SET GLOBAL long_query_time = 0.5;                  -- seconds, applies to new connections
SET GLOBAL log_queries_not_using_indexes = ON;     -- noisy; pair with throttle below
SET GLOBAL log_throttle_queries_not_using_indexes = 60;
SHOW VARIABLES LIKE 'slow_query_log_file';
```
Persist in `my.cnf` under `[mysqld]`: `slow_query_log=1`, `slow_query_log_file=/var/log/mysql/slow.log`, `long_query_time=0.5`, `min_examined_row_limit=1000`. MySQL 8 can also `SET PERSIST`.
Digest:
```bash
pt-query-digest /var/log/mysql/slow.log > digest.txt     # ranks by total time, shows fingerprint, p95, rows examined
mysqldumpslow -s t -t 10 /var/log/mysql/slow.log        # built-in, cruder
```
Look at `Rows_examined` vs `Rows_sent`: a ratio of thousands means a missing index; then `EXPLAIN ANALYZE <query>`.

## PostgreSQL
```
# postgresql.conf
log_min_duration_statement = 500ms        # logs statement + duration
log_line_prefix = '%m [%p] %q%u@%d '      # timestamp, pid, user, db
log_lock_waits = on                        # waits longer than deadlock_timeout
log_temp_files = 0                         # sorts/hashes spilling to disk
shared_preload_libraries = 'pg_stat_statements,auto_explain'
auto_explain.log_min_duration = 2s
auto_explain.log_analyze = on              # real timings; small overhead on every query
```
`log_min_duration_statement` reloads with `SELECT pg_reload_conf();`; `shared_preload_libraries` needs a restart. Per-database or per-role thresholds: `ALTER ROLE reporting SET log_min_duration_statement = '5s';`.

pg_stat_statements aggregates without log parsing:
```sql
CREATE EXTENSION pg_stat_statements;
SELECT calls, round(total_exec_time) AS ms, round(mean_exec_time,1) AS mean, rows, query
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;
SELECT pg_stat_statements_reset();   -- start a fresh measurement window
```
pgBadger turns log files into HTML reports (`pgbadger /var/log/postgresql/*.log`); it needs the log_line_prefix it documents.

## Practice
- Rank by **total** time (calls x mean), not the single slowest query; a 20 ms query called 1M times matters more.
- Threshold 0 (log everything) briefly for a sampling window only; disk and I/O cost is real.
- Logs contain literal values (PII, tokens): restrict file permissions and retention.

## Verify
- [ ] `SELECT pg_sleep(1);` or `SELECT SLEEP(1);` appears in the slow log.
- [ ] Top 10 by total time identified and each has an EXPLAIN plan reviewed.
