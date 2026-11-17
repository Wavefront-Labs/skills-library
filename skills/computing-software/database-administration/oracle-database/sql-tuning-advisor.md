---
id: computing-software.database-administration.oracle-database.sql-tuning-advisor
name: sql-tuning-advisor
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, awr, sql-tuning-advisor, dbms-sqltune, sql-profile, sql-tuning-set]
level: advanced
status: docs-checked
description: "Run the Oracle SQL Tuning Advisor with DBMS_SQLTUNE on a SQL ID, AWR range or tuning set, then accept, disable or drop SQL profiles."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_SQLTUNE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Tuning Advisor

Check your Oracle licensing terms for the advisor and the packs it relies on before use; the DBMS_SQLTUNE
reference does not cover licensing.

## Tune one statement
```sql
DECLARE t VARCHAR2(64);
BEGIN
  t := DBMS_SQLTUNE.CREATE_TUNING_TASK(sql_id => '7h35uxf5uhmm1', scope => 'COMPREHENSIVE',
         time_limit => 600, task_name => 'tune_7h35');
  DBMS_SQLTUNE.EXECUTE_TUNING_TASK('tune_7h35');
END;
/
SET LONG 1000000 LONGCHUNKSIZE 1000000 LINESIZE 200 PAGESIZE 0
SELECT DBMS_SQLTUNE.REPORT_TUNING_TASK('tune_7h35') FROM dual;
```
`CREATE_TUNING_TASK` is a function returning the task name (unique per user) and comes in forms for SQL text, a
SQL ID from the shared SQL area (optionally with `plan_hash_value`), an AWR range, a SQL tuning set and a SQL
Performance Analyzer task:
- AWR: `begin_snap`, `end_snap`, `sql_id` (plus `plan_hash_value`, `dbid`).
- SQL tuning set: `sqlset_name` with optional `basic_filter`, `object_filter`, `rank1`-`rank3`,
  `result_percentage`, `result_limit`, `plan_filter` and `sqlset_owner`.
- `time_limit` is the maximum duration in seconds; `scope` is `LIMITED` (statistics, access path and SQL structure
  analysis, no SQL profile recommendations) or `COMPREHENSIVE` (the default; adds SQL profiling).
- `database_link_to` lets a standby tune statements from the primary in an Active Data Guard setup.

## Accept a profile
```sql
EXEC DBMS_SQLTUNE.ACCEPT_SQL_PROFILE(task_name => 'tune_7h35', name => 'prof_7h35', force_match => TRUE, replace => TRUE);
SELECT * FROM dba_sql_profiles;
EXEC DBMS_SQLTUNE.ALTER_SQL_PROFILE('prof_7h35', 'STATUS', 'DISABLED');   -- roll back
EXEC DBMS_SQLTUNE.DROP_SQL_PROFILE('prof_7h35');
```
`force_match` and `replace` default to `FALSE`. `ALTER_SQL_PROFILE` can change `STATUS` (`ENABLED` or `DISABLED`),
`NAME`, `DESCRIPTION` and `CATEGORY`, and needs the `ALTER ANY SQL PROFILE` privilege.

## Verify
- [ ] Before/after: elapsed time, buffer gets per execution from `v$sql` or AWR for the SQL ID.
- [ ] Each accepted profile documented with task name and rollback command.
- [ ] Underlying stats issues fixed rather than masked by profiles.

## Checked
2026-11-09. Confirmed against the 19c `DBMS_SQLTUNE` reference: `CREATE_TUNING_TASK` forms, parameters and `scope`
values, `ALTER_SQL_PROFILE` attributes and privilege, `ACCEPT_SQL_PROFILE` `force_match`/`replace` defaults,
the `dba_sql_profiles` view name and the execute/report subprograms. Removed because the cited pages do not state them: the
licensing and `CONTROL_MANAGEMENT_PACK_ACCESS` claims, finding-type descriptions, the profile mechanism, the
`sqltrpt.sql` script, SQL Access Advisor and plan-baseline advice, and the Automatic SQL Tuning section
(`DBMS_AUTO_SQLTUNE`). The first source (`tgsql/analyzing-sql-with-sql-tuning-advisor.html`) returned 404 and was
dropped. The SQL*Plus display settings and the `v$sql`/AWR verification advice are generic practice, not claims from the page.
Method: documentation only; no commands were run.
