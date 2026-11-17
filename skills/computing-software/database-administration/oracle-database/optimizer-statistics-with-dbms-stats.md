---
id: computing-software.database-administration.oracle-database.optimizer-statistics-with-dbms-stats
name: optimizer-statistics-with-dbms-stats
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, awr, dbms-stats, optimizer-statistics, gather-table-stats, histograms, incremental-statistics, stale-statistics, lock-stats, pending-statistics, extended-statistics, restore-table-stats]
level: advanced
status: docs-checked
description: "Gather and manage Oracle optimizer statistics with DBMS_STATS: auto task, preferences, histograms, incremental partition stats, locking, pending and restoring stats."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/gathering-optimizer-statistics.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_STATS.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optimizer statistics with DBMS_STATS

## Default: the automatic task
The `auto optimizer stats collection` AutoTask runs in all predefined maintenance windows by default and,
unlike manual gathers, prioritises objects with no or very old statistics. Check it is enabled and ran:
```sql
SELECT client_name, status FROM dba_autotask_client;
SELECT * FROM (SELECT opid, operation, target, start_time, end_time, status
  FROM dba_optstat_operations ORDER BY start_time DESC) WHERE ROWNUM <= 20;
```
Change behaviour with **preferences**, not ad hoc gather scripts with hard-coded options:
```sql
EXEC DBMS_STATS.SET_TABLE_PREFS('APP','ORDERS','STALE_PERCENT','5');
EXEC DBMS_STATS.SET_TABLE_PREFS('APP','ORDERS','METHOD_OPT','FOR ALL COLUMNS SIZE AUTO FOR COLUMNS SIZE 254 STATUS');
EXEC DBMS_STATS.SET_GLOBAL_PREFS('CONCURRENT','ALL');   -- jobs per partition; bounded by JOB_QUEUE_PROCESSES; needs Resource Manager enabled
SELECT DBMS_STATS.GET_PREFS('ESTIMATE_PERCENT','APP','ORDERS') FROM dual;  -- keep AUTO_SAMPLE_SIZE
```

## Manual gathers
```sql
EXEC DBMS_STATS.GATHER_TABLE_STATS('APP','ORDERS', cascade => TRUE, degree => 8, no_invalidate => FALSE);
EXEC DBMS_STATS.GATHER_SCHEMA_STATS('APP', options => 'GATHER STALE');
EXEC DBMS_STATS.GATHER_DICTIONARY_STATS;
EXEC DBMS_STATS.GATHER_FIXED_OBJECTS_STATS;   -- once under representative load, and after upgrades
```
Gather right after bulk loads inside batch jobs (the maintenance window may be too late);
bulk loads can also trigger online statistics gathering (conditions are in the SQL Tuning Guide).
`no_invalidate => FALSE` invalidates dependent cursors immediately; the default
(`DBMS_STATS.AUTO_INVALIDATE`) lets Oracle decide when to invalidate them.

## Staleness and history
```sql
-- from 12.2 the *_TAB_STATISTICS views include cached info, so FLUSH_DATABASE_MONITORING_INFO is not needed first
SELECT table_name, num_rows, last_analyzed, stale_stats FROM dba_tab_statistics WHERE owner = 'APP' AND stale_stats = 'YES';
SELECT * FROM dba_tab_modifications WHERE table_owner = 'APP';
```

## Histograms
`SIZE AUTO` lets Oracle decide which columns get histograms. To drop a harmful histogram,
regather with `METHOD_OPT => 'FOR COLUMNS SIZE 1 col'` (set as a table pref; at global,
schema, database or dictionary level only `FOR ALL` syntax is allowed).

## Partitioned tables: incremental statistics
```sql
EXEC DBMS_STATS.SET_TABLE_PREFS('APP','SALES','INCREMENTAL','TRUE');
EXEC DBMS_STATS.SET_TABLE_PREFS('APP','SALES','INCREMENTAL_STALENESS','USE_STALE_PERCENT,USE_LOCKED_STATS');
```
With `INCREMENTAL`, global statistics are maintained without a full table scan, derived from partition-level statistics. `INCREMENTAL_STALENESS` accepts `USE_STALE_PERCENT` and `USE_LOCKED_STATS`.

## Correlated columns: extended statistics
```sql
SELECT DBMS_STATS.CREATE_EXTENDED_STATS('APP','CUSTOMERS','(COUNTRY, STATE)') FROM dual;
```
Creates a virtual column for the column group; regather statistics afterwards so the optimizer can use it for correlated predicates.

## Safety nets
```sql
EXEC DBMS_STATS.LOCK_TABLE_STATS('APP','QUEUE_TABLE');          -- volatile tables: lock representative stats
EXEC DBMS_STATS.SET_TABLE_PREFS('APP','ORDERS','PUBLISH','FALSE'); -- gather as pending
ALTER SESSION SET optimizer_use_pending_statistics = TRUE;          -- test, then
EXEC DBMS_STATS.PUBLISH_PENDING_STATS('APP','ORDERS');
EXEC DBMS_STATS.RESTORE_TABLE_STATS('APP','ORDERS', SYSTIMESTAMP - INTERVAL '1' DAY);  -- undo a bad gather
SELECT DBMS_STATS.GET_STATS_HISTORY_RETENTION FROM dual;            -- retention in days
```
`DBMS_STATS.DIFF_TABLE_STATS_IN_HISTORY` shows what changed between two times.

## Verify
- [ ] Auto task enabled and completing (`dba_optstat_operations` no timeouts).
- [ ] No important tables with `stale_stats = YES` or null `last_analyzed`.
- [ ] Batch jobs gather after loads; fixed-object stats gathered post-upgrade.

## Checked
2026-10-31. Against the Oracle Database 19c SQL Tuning Guide (Gathering Optimizer Statistics) and the DBMS_STATS reference: AutoTask client name and default windows, `DBA_AUTOTASK_CLIENT`, `DBA_OPTSTAT_OPERATIONS`, `DBA_TAB_STATISTICS.STALE_STATS`, `DBA_TAB_MODIFICATIONS`, `STALE_PERCENT`, `METHOD_OPT`, `PUBLISH`, `INCREMENTAL`, `INCREMENTAL_STALENESS` values, `CONCURRENT` preference and Resource Manager requirement, `AUTO_INVALIDATE`, the 12.2 note on `FLUSH_DATABASE_MONITORING_INFO`, pending-statistics, restore, diff and extended-statistics subprograms. Removed unconfirmed details: the `CONCURRENT` value `AUTOMATIC`, the 31 day history retention default, histogram type list and `sys.col_usage$` remark, per-partition synopsis wording and the plan-flip claim.
Method: documentation only; no commands were run.
