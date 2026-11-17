---
id: computing-software.database-administration.oracle-database.sql-plan-baselines
name: sql-plan-baselines
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, awr, sql-plan-baselines, sql-plan-management, spm, dbms-spm, plan-stability, evolve, fixed-baseline, plan-regression, coe-xfr-sql-profile]
level: advanced
status: docs-checked
description: "Pin a known-good Oracle execution plan with SQL plan baselines: load from cursor cache or AWR, fix or evolve plans, and check which baseline a SQL uses."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/managing-sql-plan-baselines.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_SPM.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL plan baselines (SQL plan management)

**Goal:** a statement that flipped to a bad plan goes back to the good one now, and
cannot flip again without a verified-better plan. Check the licensing guide for your edition
before relying on SPM features.

## Find the good plan
```sql
SELECT sql_id, plan_hash_value, executions, ROUND(elapsed_time/NULLIF(executions,0)/1e3) ms_per_exec, child_number
FROM v$sql WHERE sql_id = 'gd8x5fz7cpk3m';
-- history
SELECT snap_id, plan_hash_value, executions_delta, ROUND(elapsed_time_delta/NULLIF(executions_delta,0)/1e3) ms
FROM dba_hist_sqlstat WHERE sql_id = 'gd8x5fz7cpk3m' ORDER BY snap_id;
```

## Load it as a baseline
From the cursor cache (plan still cached):
```sql
DECLARE n PLS_INTEGER;
BEGIN
  n := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(sql_id => 'gd8x5fz7cpk3m', plan_hash_value => 1838229974,
         fixed => 'NO', enabled => 'YES');
  DBMS_OUTPUT.PUT_LINE(n || ' plans loaded');
END;
/
```
From AWR (or load from a SQL tuning set with `LOAD_PLANS_FROM_SQLSET`):
```sql
n := DBMS_SPM.LOAD_PLANS_FROM_AWR(begin_snap => 1200, end_snap => 1250,
       basic_filter => q'[sql_id = 'gd8x5fz7cpk3m' AND plan_hash_value = 1838229974]');
```
Good plan only exists for a different SQL text (e.g. you hinted a copy): load the hinted
plan's `sql_id`/`plan_hash_value` against the original statement's `sql_handle`
(`LOAD_PLANS_FROM_CURSOR_CACHE(sql_id => <hinted>, plan_hash_value => <phv>, sql_handle => <original handle>)`).

## Inspect and manage
```sql
SELECT sql_handle, plan_name, enabled, accepted, fixed, reproduced, origin, last_executed
FROM dba_sql_plan_baselines WHERE sql_text LIKE '%orders o JOIN customers%';
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_SQL_PLAN_BASELINE(sql_handle => 'SQL_8a2f...', format => 'BASIC +NOTE'));
-- is it used?
SELECT sql_id, sql_plan_baseline FROM v$sql WHERE sql_id = 'gd8x5fz7cpk3m';
-- DBMS_XPLAN.DISPLAY_CURSOR Note section: "SQL plan baseline SQL_PLAN_xxx used for this statement"
n := DBMS_SPM.ALTER_SQL_PLAN_BASELINE(sql_handle => 'SQL_8a2f...', plan_name => 'SQL_PLAN_8n...',
       attribute_name => 'fixed', attribute_value => 'YES');
n := DBMS_SPM.DROP_SQL_PLAN_BASELINE(sql_handle => 'SQL_8a2f...', plan_name => NULL);  -- all plans for the SQL
```
- **Accepted** plans are the only ones the optimizer may use.
- **Fixed** plans are preferred by the optimizer over non-fixed plans in the baseline.

## Evolution
New plans found for a baselined SQL are stored unaccepted. The
`SYS_AUTO_SPM_EVOLVE_TASK` (an automated task in the maintenance window, controlled by the SPM
parameter `AUTO_SPM_EVOLVE_TASK`) verifies them and, with `ACCEPT_PLANS` true (the default), accepts those it recommends.
Manual:
```sql
SELECT DBMS_SPM.EVOLVE_SQL_PLAN_BASELINE(sql_handle => 'SQL_8a2f...', verify => 'YES', commit => 'YES') FROM dual;
```
`OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES = TRUE` captures for every repeatable SQL: rarely
worth it database-wide; prefer targeted loading. Before upgrades, capture the workload
into an STS and load baselines after the upgrade to prevent regressions.

## Gotchas
- SPM space is in SYSAUX; unused plans are purged after `PLAN_RETENTION_WEEKS` (default 53, range 5 to 523).
- A baseline + a SQL profile + hints can interact; check the Note section of the plan.

## Verify
- [ ] `v$sql.sql_plan_baseline` populated for the SQL ID and elapsed time back to normal.
- [ ] Baseline documented (why, which plan hash), reviewed after upgrades.

## Checked
2026-10-31. Confirmed in the 19c SQL Tuning Guide (Managing SQL Plan Baselines) and DBMS_SPM
reference: `LOAD_PLANS_FROM_CURSOR_CACHE` / `LOAD_PLANS_FROM_AWR` / `LOAD_PLANS_FROM_SQLSET`, the
`fixed` argument (default NO) and fixed-plan preference, `DBMS_XPLAN.DISPLAY_SQL_PLAN_BASELINE`,
`SYS_AUTO_SPM_EVOLVE_TASK` and `AUTO_SPM_EVOLVE_TASK`, `ACCEPT_PLANS` default, `PLAN_RETENTION_WEEKS`
(53, range 5-523), SYSAUX space, `OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES` capturing all repeatable
statements. Removed: Enterprise Edition / Tuning Pack licensing claim, "18c+" gate, "nightly", the
`reproduced = NO` behaviour, "cheapest accepted plan wins" and the literal-SQL / `CURSOR_SHARING`
note (not found in the fetched pages). SQL IDs and handles are placeholders.
Method: documentation only; no commands were run.
