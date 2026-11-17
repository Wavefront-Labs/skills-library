---
id: computing-software.database-administration.oracle-database.dbms-xplan-and-real-time-sql-monitoring
name: dbms-xplan-and-real-time-sql-monitoring
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, awr, ash, dbms-xplan, display-cursor, sql-monitor, real-time-sql-monitoring, report-sql-monitor, gather-plan-statistics, cardinality-misestimate, explain-plan]
level: advanced
status: docs-checked
description: "Read actual Oracle execution plans with DBMS_XPLAN.DISPLAY_CURSOR and ALLSTATS LAST, and live or historical SQL Monitor reports, to find where a query spends time."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/generating-and-displaying-execution-plans.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_XPLAN.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/monitoring-database-operations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DBMS_XPLAN and real-time SQL monitoring

## Estimated vs actual
`EXPLAIN PLAN` shows what the optimizer would do *now*, with no bind peeking and
possibly different from what ran. Diagnose with the plan actually used, from the cursor cache.

## Actual plan with row source statistics
```sql
SELECT /*+ GATHER_PLAN_STATISTICS */ ... ;          -- or ALTER SESSION SET statistics_level = ALL
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(NULL, NULL, 'ALLSTATS LAST'));   -- ALLSTATS = IOSTATS MEMSTATS; LAST = most recent execution only
-- another session's statement
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR('gd8x5fz7cpk3m', 0, 'ALLSTATS LAST'));
-- from AWR (plan only, no row stats)
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_WORKLOAD_REPOSITORY('gd8x5fz7cpk3m', 1838229974));   -- (sql_id, plan_hash_value, format, dbid, ...); replaces deprecated DISPLAY_AWR
```
Columns to read:
- `E-Rows` (estimate per start) vs `A-Rows` (actual total) / `Starts`: compare
  `E-Rows x Starts` with `A-Rows`. A 10x+ error at an operation is where the plan went
  wrong; the fix is about **that** estimate (stats, histograms, extended stats, SQL shape).
- `A-Time` is the actual time per operation; `Buffers` the buffer gets.
- `MEMSTATS` (part of `ALLSTATS`) adds memory-management statistics for memory-intensive operations such as hash joins and sorts.
The `ADAPTIVE` format level is documented for DISPLAY_CURSOR; `TYPICAL` is the default format and `-keyword` excludes an item (for example `-PROJECTION`). `MEMSTATS` needs `pga_aggregate_target` set.

## Real-time SQL Monitoring (Tuning Pack)
Monitoring is on when `STATISTICS_LEVEL` is TYPICAL (default) or ALL, and `CONTROL_MANAGEMENT_PACK_ACCESS` is `DIAGNOSTIC+TUNING` (default). A statement is monitored automatically when one execution has used at least 5 seconds of CPU or I/O time, it runs in parallel, or it has `/*+ MONITOR */` (`/*+ NO_MONITOR */` disables it). Live, per-line progress and waits, no need to re-run.
```sql
SELECT sql_id, sql_exec_id, status, cpu_time, buffer_gets
FROM v$sql_monitor ORDER BY sql_exec_start DESC FETCH FIRST 20 ROWS ONLY;

SET LONG 10000000 LONGCHUNKSIZE 10000000 LINESIZE 250 PAGESIZE 0 TRIMSPOOL ON
SPOOL sqlmon.html
SELECT DBMS_SQL_MONITOR.REPORT_SQL_MONITOR(sql_id => 'gd8x5fz7cpk3m', type => 'ACTIVE') FROM dual;
SPOOL OFF
-- type: TEXT (default), HTML, ACTIVE or XML; DBMS_SQLTUNE.REPORT_SQL_MONITOR() is the older package
```
AWR captures SQL Monitor reports automatically (XML) for the most expensive finished statements; `DBA_HIST_REPORTS` holds the metadata (`COMPONENT_NAME` = sqlmonitor, `REPORT_ID`, `KEY1` = SQL ID, `KEY2` = execution ID) and `DBA_HIST_REPORTS_DETAILS` the content; pass the report id as `rid` to `DBMS_AUTO_REPORT.REPORT_REPOSITORY_DETAIL`. Retention follows the AWR policy (`DBMS_WORKLOAD_REPOSITORY.MODIFY_SNAPSHOT_SETTINGS`); reports are not exported with AWR data. Capture the report during the incident.

## Plan comparison
- Different plans across children: `SELECT child_number, plan_hash_value FROM v$sql WHERE sql_id=...`,
  and `v$sql_shared_cursor` for why a child was not shared (bind mismatch, optimizer env).
- `DBMS_XPLAN.COMPARE_PLANS(reference_plan, compare_plan_list, type, level, section)` returns a comparison report as a CLOB.

## Verify
- [ ] Diagnosis cites the operation with the largest estimate error or time share.
- [ ] Active SQL Monitor report saved for long-running incidents.
- [ ] Fix confirmed with a new ALLSTATS LAST plan showing improved A-Rows/Buffers.

## Checked
Date 2026-10-22. Oracle Database 19c PL/SQL Packages Reference (DBMS_XPLAN) and SQL Tuning Guide (monitoring database
operations). Confirmed: DISPLAY_CURSOR signature and ALLSTATS/LAST/MEMSTATS/ADAPTIVE keywords, DISPLAY_WORKLOAD_REPOSITORY
signature, automatic monitoring rules and Tuning Pack requirement, MONITOR/NO_MONITOR hints, DBMS_SQL_MONITOR.REPORT_SQL_MONITOR
types, DBA_HIST_REPORTS and REPORT_REPOSITORY_DETAIL `rid`, COMPARE_PLANS signature. Removed (not on the pages read):
`+PEEKED_BINDS`, `+OUTLINE`, `+NOTE` format examples, "12c+" and "12.2+" gates, the `type => 'active'` argument to
REPORT_REPOSITORY_DETAIL, the in-memory retention remark. Trimmed the column-reading list to the columns shown in the 19c Tuning Guide example output (Starts, E-Rows, A-Rows, A-Time, Buffers); removed unconfirmed remarks on Reads, OMem/1Mem/Used-Mem/Used-Tmp, predicate conversions and the Note section. Replaced the 404 reading-execution-plans source.
Method: documentation only; no commands were run.
