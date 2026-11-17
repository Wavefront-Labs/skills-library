---
id: computing-software.database-administration.oracle-database.sql-performance-analyzer-for-upgrades
name: sql-performance-analyzer-for-upgrades
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, sql-performance-analyzer, spa, sql-tuning-set, dbms-sqlpa, upgrade-testing, regression-testing, real-application-testing]
level: sme
status: docs-checked
description: "Test Oracle upgrades and changes with SQL Performance Analyzer: capture a SQL tuning set, run before/after trials, compare, and fix regressions with baselines."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/ratug/introduction-to-sql-performance-analyzer.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_SQLPA.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_SQLTUNE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Performance Analyzer for upgrades

SPA executes a set of SQL before and after a change (upgrade, parameter, stats, index) and reports
per-statement regressions. Check your licence for the options it needs before use.

## 1. Capture a SQL tuning set (STS) on production
```sql
EXEC DBMS_SQLTUNE.CREATE_SQLSET('STS_PROD_OCT', 'production workload');
-- from the cursor cache over 2 hours (7200 s), sampling every 5 minutes (300 s); defaults are 1800 s and 300 s
EXEC DBMS_SQLTUNE.CAPTURE_CURSOR_CACHE_SQLSET(sqlset_name => 'STS_PROD_OCT', time_limit => 7200, repeat_interval => 300);
-- or from AWR snapshots
DECLARE c DBMS_SQLTUNE.SQLSET_CURSOR; BEGIN
  OPEN c FOR SELECT VALUE(p) FROM TABLE(DBMS_SQLTUNE.SELECT_WORKLOAD_REPOSITORY(41200, 41300,
     'parsing_schema_name NOT IN (''SYS'',''SYSTEM'')', NULL, NULL, NULL, NULL, 1, NULL, 'ALL')) p;
  DBMS_SQLTUNE.LOAD_SQLSET('STS_PROD_OCT', c);
END;
/
```
Move it to the test system: `DBMS_SQLTUNE.CREATE_STGTAB_SQLSET`, `PACK_STGTAB_SQLSET`, copy the staging table (for example with Data Pump), `UNPACK_STGTAB_SQLSET`.
The test database should be a restore/clone of production data.

## 2. Trials
```sql
VARIABLE t VARCHAR2(64)
EXEC :t := DBMS_SQLPA.CREATE_ANALYSIS_TASK(sqlset_name => 'STS_PROD_OCT', task_name => 'SPA_19C');
-- before: on the old version, or convert the STS's captured stats as the "before" trial
EXEC DBMS_SQLPA.EXECUTE_ANALYSIS_TASK('SPA_19C', 'CONVERT SQLSET', 'BEFORE');
-- after: on the upgraded database
EXEC DBMS_SQLPA.EXECUTE_ANALYSIS_TASK('SPA_19C', 'TEST EXECUTE', 'AFTER');
-- compare
EXEC DBMS_SQLPA.EXECUTE_ANALYSIS_TASK('SPA_19C', 'COMPARE PERFORMANCE', 'CMP', -
  DBMS_ADVISOR.ARGLIST('comparison_metric', 'buffer_gets', 'execution_name1', 'BEFORE', 'execution_name2', 'AFTER'));
```
`TEST EXECUTE` runs each statement to completion (at least twice, first run warms the cache; DDL is not supported, and by default only the query portion of DML runs, the `EXECUTE_FULLDML` task parameter runs full DML via the API); `EXPLAIN PLAN` mode only generates plans (it takes bind values into account).
`COMPARE PERFORMANCE` compares the last two executions by default using `elapsed_time`; set `comparison_metric` to another expression such as `buffer_gets` or `cpu_time + buffer_gets * 10`.

## 3. Report
```sql
SET LONG 10000000 LONGCHUNKSIZE 10000000 LINESIZE 300 PAGESIZE 0
SELECT DBMS_SQLPA.REPORT_ANALYSIS_TASK('SPA_19C', 'HTML', 'TYPICAL', 'SUMMARY') FROM dual;
SELECT DBMS_SQLPA.REPORT_ANALYSIS_TASK('SPA_19C', 'TEXT', 'REGRESSED', 'ALL') FROM dual;
```
The `level` argument filters (`REGRESSED`, `IMPROVED`, `CHANGED_PLANS`, `ALL` and others); the `section` is `SUMMARY` (default) or `ALL`. Shows improved / regressed / unchanged counts, impact on the workload, and plan changes per SQL.

## 4. Fix regressions
- Load the old plans as SQL plan baselines on the new system: from the STS (`DBMS_SPM.LOAD_PLANS_FROM_SQLSET` with a filter on the regressed SQL_IDs).
- Or run SQL Tuning Advisor on the regressed set: `DBMS_SQLTUNE.CREATE_TUNING_TASK` accepts a SQL tuning set.
- Re-run the `AFTER` trial to confirm.

## Gotchas
- Captured binds matter: SPA needs the bind values stored in the tuning set to execute statements and produce accurate statistics.
- Statements touching volatile data (sysdate predicates) may differ for data reasons, not plan reasons.
- `CONVERT SQLSET` builds a trial from statistics already in the tuning set, so you can avoid executing the statements when valid data exists.

## Verify
Regressed SQL list is empty or every regressed statement has a baseline or fix before go-live.

## Checked
2026-10-31. Against the Oracle Database 19c Real Application Testing guide (SQL Performance Analyzer introduction) and the DBMS_SQLPA, DBMS_SQLTUNE and DBMS_SPM references: execution types, `comparison_metric` default and expressions, `REPORT_ANALYSIS_TASK` arguments and levels, test-execute behaviour (DDL, DML query portion), `CAPTURE_CURSOR_CACHE_SQLSET` defaults, staging-table procedures, `SELECT_WORKLOAD_REPOSITORY` argument order, `LOAD_PLANS_FROM_SQLSET` and tuning tasks on a tuning set. Removed unconfirmed details: licensing/pack remarks, AutoUpgrade driving SPA, snapshot standby advice, the AWR-versus-cursor-cache bind claim and "buffer gets is most stable".
Method: documentation only; no commands were run.
