---
id: computing-software.database-administration.oracle-database.awr-baselines-and-compare-period-reports
name: awr-baselines-and-compare-period-reports
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, awr-baseline, awr-diff, awrddrpt, compare-period-report, dbms-workload-repository, moving-window-baseline]
level: advanced
status: docs-checked
description: "Keep Oracle AWR baselines (fixed and moving window), set snapshot retention, and produce compare-period (AWR diff) reports to explain 'it was fast last week'."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgdba/gathering-database-statistics.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgdba/comparing-database-performance-over-time.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_WORKLOAD_REPOSITORY.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWR baselines and compare-period reports

Diagnostics Pack required.

## Retention and interval
Default: hourly snapshots kept 8 days. Too short to compare month-end with last month-end.
```sql
EXEC DBMS_WORKLOAD_REPOSITORY.MODIFY_SNAPSHOT_SETTINGS(retention => 60*24*45, interval => 30);  -- 45 days, 30 min
SELECT snap_interval, retention FROM dba_hist_wr_control;
```
Size SYSAUX for it (AWR data is stored in SYSAUX unless `tablespace_name` is given). `interval` is in minutes (10 minutes to 1 year; 0 disables snapshots), `retention` in minutes (1 day minimum).
The moving window baseline (`SYSTEM_MOVING_WINDOW`) defaults to the retention period and must be <= retention (raise retention first):
`EXEC DBMS_WORKLOAD_REPOSITORY.MODIFY_BASELINE_WINDOW_SIZE(window_size => 30);` (days; maximum 13 weeks).

## Fixed baselines
Preserve known-good periods beyond retention:
```sql
EXEC DBMS_WORKLOAD_REPOSITORY.CREATE_BASELINE(start_snap_id => 41200, end_snap_id => 41210, baseline_name => 'MONTH_END_SEP26', expiration => NULL);
-- by time
EXEC DBMS_WORKLOAD_REPOSITORY.CREATE_BASELINE(start_time => TIMESTAMP '2026-09-30 18:00:00', end_time => TIMESTAMP '2026-09-30 23:00:00', baseline_name => 'MONTH_END_SEP26_T');
SELECT baseline_name, baseline_type, start_snap_time, end_snap_time, expiration FROM dba_hist_baseline;
```
Repeating templates create baselines automatically (e.g. every Monday 09-12; `expiration` is days and has no default in the signature):
`DBMS_WORKLOAD_REPOSITORY.CREATE_BASELINE_TEMPLATE(day_of_week => 'MONDAY', hour_in_day => 9, duration => 3, start_time => ..., end_time => ..., baseline_name_prefix => 'MON_AM_', template_name => 'mon_am', expiration => 90);`
Baselines are preserved until they expire (`expiration` NULL = kept forever).

## Compare-period report
```sql
@?/rdbms/admin/awrddrpt.sql       -- prompts for two snapshot ranges (same or different DBID/instance)
```
Or directly:
```sql
SELECT * FROM TABLE(DBMS_WORKLOAD_REPOSITORY.AWR_DIFF_REPORT_HTML(
  dbid1 => 1234567890, inst_num1 => 1, bid1 => 41200, eid1 => 41210,
  dbid2 => 1234567890, inst_num2 => 1, bid2 => 42100, eid2 => 42110));
```

## Reading it
1. Load profile: did the **workload** change (executes/s, transactions/s, logical reads/s)? Same work done slower vs more work.
2. Top timed events side by side: which wait class grew (User I/O, Concurrency, Cluster)?
3. Time model: DB CPU vs DB time; parse time; PL/SQL time.
4. SQL ordered by elapsed time difference: one SQL_ID changed plan (`plan_hash_value` differs)? Then
   `@?/rdbms/admin/awrsqrpt.sql` (statistics for one SQL statement over a snapshot range) and SQL plan management to fix.
5. Initialization parameter differences: someone changed a parameter (the section name varies by release; look for it in the diff report).
Normalise by period length: the report shows per-second and per-transaction figures; compare those.

## Gotchas
- Different snapshot lengths make totals misleading; use rates.
- Pick snapshot ranges within one instance startup; a range spanning a restart is not valid for reports.
- `dba_hist_*` queries count as Diagnostics Pack usage.

## Verify
Baselines exist for the key business periods, retention covers at least one full business cycle, and a diff report for the latest incident is filed with the RCA.

## Checked
Date 2026-10-22. Oracle Database 19c PL/SQL Packages and Types Reference (DBMS_WORKLOAD_REPOSITORY), Performance Tuning
Guide, Database Reference (DBA_HIST_BASELINE). Confirmed: default hourly snapshots kept 8 days, `DBA_HIST_WR_CONTROL`,
MODIFY_SNAPSHOT_SETTINGS / MODIFY_BASELINE_WINDOW_SIZE / CREATE_BASELINE / CREATE_BASELINE_TEMPLATE /
AWR_DIFF_REPORT_HTML signatures and units, moving window default and limits, DBA_HIST_BASELINE columns.
Removed unconfirmed: `awrgdrpt.sql` RAC description, `ORA-20200`, `awrinfo.sql`, "snapshots in a baseline are not purged"
wording (replaced by documented expiration behaviour). `awrddrpt.sql` is named by the DBMS_WORKLOAD_REPOSITORY page as
the recommended interactive script for the diff report.
Method: documentation only; no commands were run.
