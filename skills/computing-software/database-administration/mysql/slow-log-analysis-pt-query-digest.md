---
id: computing-software.database-administration.mysql.slow-log-analysis-pt-query-digest
name: slow-log-analysis-pt-query-digest
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, slow-log-analysis, mysqldumpslow, pt-query-digest, slow-query-log, long-query-time, query-performance]
level: practitioner
status: docs-checked
description: "Capture the MySQL slow query log with useful thresholds, then rank query fingerprints with pt-query-digest or mysqldumpslow to pick what to fix."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/slow-query-log.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysqldumpslow.html
  - https://docs.percona.com/percona-toolkit/pt-query-digest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Analysing the slow log with pt-query-digest and mysqldumpslow

## Capture
```sql
SET PERSIST slow_query_log = ON;
SET PERSIST slow_query_log_file = '/var/log/mysql/slow.log';
SET PERSIST long_query_time = 0.5;           -- seconds, fractional allowed
SET PERSIST log_slow_extra = ON;             -- 8.0.14+: extra fields (thread id, tmp tables, sorts, read counts)
SET PERSIST log_queries_not_using_indexes = OFF;   -- very noisy; enable briefly with log_throttle_queries_not_using_indexes
```
For a full workload picture, temporarily `long_query_time = 0` for 10-30 minutes at peak (watch disk), then restore. `long_query_time` applies to new sessions; pooled connections keep the old value until reconnect.

## pt-query-digest (Percona Toolkit)
```bash
pt-query-digest /var/log/mysql/slow.log > digest.txt
pt-query-digest --since '2026-10-18 09:00:00' --until '2026-10-18 10:00:00' slow.log
pt-query-digest --filter '$event->{db} eq "shop"' slow.log
pt-query-digest --limit 20 --order-by Query_time:sum slow.log
```
Read the **Profile** table: queries ranked by total response time. Fix the top few (often 3-5 fingerprints are >50% of DB time). Per query you get count, total/avg/p95 times, rows examined vs sent (ratio >> 1 = missing index), and a sample with `EXPLAIN` hint.

## mysqldumpslow (ships with MySQL)
```bash
mysqldumpslow -s t -t 10 /var/log/mysql/slow.log    # top 10 by total time
mysqldumpslow -s c -t 10 slow.log                   # by count
```
Cruder than pt-query-digest (no percentiles), but always available.

## Alternative without log files
```sql
SELECT DIGEST_TEXT, COUNT_STAR, ROUND(SUM_TIMER_WAIT/1e12,1) AS total_s, ROUND(AVG_TIMER_WAIT/1e9,1) AS avg_ms,
       SUM_ROWS_EXAMINED, SUM_ROWS_SENT
FROM performance_schema.events_statements_summary_by_digest ORDER BY SUM_TIMER_WAIT DESC LIMIT 10;
```
Or `sys.statement_analysis`. Good for continuous monitoring; the slow log gives exact samples with timestamps.

## Gotchas
- Slow log on a busy server with `long_query_time=0` can write GBs per hour; rotate it.
- `Query_time` is total execution time and `Lock_time` the time to acquire locks; check `Lock_time` before blaming the query plan.
- Replicas log slow replicated statements only with `log_slow_replica_statements = ON`.

## Checked

2026-10-31: confirmed long_query_time (minimum 0, default 10, microsecond resolution), log_queries_not_using_indexes, log_throttle_queries_not_using_indexes, log_slow_replica_statements (no effect with row-based replication) on the dev.mysql.com slow-query-log page; log_slow_extra introduced in MySQL 8.0.14 per the 8.0.14 release notes, with extra fields Thread_id, Errno, Killed, Bytes_*, Read_*, Sort_*, Created_tmp_tables, Created_tmp_disk_tables, Start, End; mysqldumpslow -s t (sort by query time), -s c (sort by count), -t N; performance_schema.events_statements_summary_by_digest columns and sys.statement_analysis on the sys-schema page. Corrected the log_slow_extra field list and the Query_time/Lock_time wording.
Method: documentation only; no commands were run.
