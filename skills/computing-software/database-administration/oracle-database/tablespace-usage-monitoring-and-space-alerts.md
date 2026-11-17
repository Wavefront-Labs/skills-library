---
id: computing-software.database-administration.oracle-database.tablespace-usage-monitoring-and-space-alerts
name: tablespace-usage-monitoring-and-space-alerts
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle-tablespaces, tablespace-usage-metrics, space-alert-thresholds, dbms-server-alert, capacity-planning, ora-01653]
level: practitioner
status: docs-checked
description: "Monitor Oracle tablespace usage correctly (autoextend max, not current size) with DBA_TABLESPACE_USAGE_METRICS, set server alert thresholds, and track growth."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/DBA_TABLESPACE_USAGE_METRICS.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_SERVER_ALERT.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-space-for-schema-objects.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_SPACE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tablespace usage monitoring and space alerts

## Use the metric that accounts for autoextend
`DBA_TABLESPACE_USAGE_METRICS` reports used space against the **maximum possible size**
(including autoextend `MAXSIZE`), in database blocks:
```sql
SELECT m.tablespace_name,
       ROUND(m.used_space * t.block_size / 1024/1024/1024, 1)      AS used_gb,
       ROUND(m.tablespace_size * t.block_size / 1024/1024/1024, 1) AS max_gb,
       ROUND(m.used_percent, 1) AS used_pct
FROM dba_tablespace_usage_metrics m JOIN dba_tablespaces t USING (tablespace_name)
ORDER BY used_pct DESC;
```
Queries that compare `dba_free_space` to current `dba_data_files.bytes` raise false alarms on
autoextending files and miss real risks when MAXSIZE is near or the **filesystem/ASM** cannot
actually grow the file. Check disk group free space too:
`SELECT name, free_mb, total_mb, usable_file_mb FROM v$asm_diskgroup;`

## Server-generated alerts (thresholds)
Read the current thresholds from `DBA_THRESHOLDS` before changing them.
```sql
BEGIN
  DBMS_SERVER_ALERT.SET_THRESHOLD(
    metrics_id => DBMS_SERVER_ALERT.TABLESPACE_PCT_FULL,
    warning_operator => DBMS_SERVER_ALERT.OPERATOR_GE, warning_value => '80',
    critical_operator => DBMS_SERVER_ALERT.OPERATOR_GE, critical_value => '90',
    observation_period => 1, consecutive_occurrences => 1,
    instance_name => NULL, object_type => DBMS_SERVER_ALERT.OBJECT_TYPE_TABLESPACE,
    object_name => 'USERS');
END;
/
SELECT object_name, reason, suggested_action FROM dba_outstanding_alerts;
SELECT * FROM dba_thresholds WHERE metrics_name LIKE 'Tablespace%';
```
For very large tablespaces use `TABLESPACE_BYT_FREE` (a free-space threshold in kilobytes) since a
percentage of a huge tablespace still leaves a lot of room. Enterprise Manager or your monitoring tool should read these alerts.

## Growth trend (capacity planning)
AWR keeps tablespace usage history:
```sql
SELECT TRUNC(TO_DATE(h.rtime, 'MM/DD/YYYY HH24:MI:SS')) day, t.name,
       MAX(h.tablespace_usedsize) * 8192 / 1024/1024/1024 used_gb   -- adjust block size
FROM dba_hist_tbspc_space_usage h JOIN v$tablespace t ON t.ts# = h.tablespace_id
GROUP BY TRUNC(TO_DATE(h.rtime, 'MM/DD/YYYY HH24:MI:SS')), t.name ORDER BY 1;
```
(AWR requires the Diagnostics Pack licence.) Segment growth: `DBMS_SPACE.OBJECT_GROWTH_TREND`.

## When full
`ORA-01653` (table), `ORA-01654` (index) or `ORA-01688` (table partition) report that the object cannot extend. Fix: add a datafile or raise MAXSIZE:
```sql
ALTER TABLESPACE users ADD DATAFILE '+DATA' SIZE 10G AUTOEXTEND ON NEXT 1G MAXSIZE 32767M;
ALTER DATABASE DATAFILE 5 AUTOEXTEND ON MAXSIZE UNLIMITED;
```
Resumable space allocation can suspend jobs instead of failing while you add space.

## Verify
After adding space, `used_pct` in the metrics view drops, `dba_outstanding_alerts` clears, and
the failing job succeeds.

## Checked
2026-10-31. Confirmed in the 19c Database Reference (`DBA_TABLESPACE_USAGE_METRICS`: `USED_SPACE` in
blocks, `USED_PERCENT` against the maximum possible size; `DBA_TABLESPACES`, `DBA_THRESHOLDS`,
`DBA_OUTSTANDING_ALERTS`, `DBA_HIST_TBSPC_SPACE_USAGE`, `V$ASM_DISKGROUP`), `DBMS_SERVER_ALERT`
(`TABLESPACE_PCT_FULL`, `TABLESPACE_BYT_FREE`), `DBMS_SPACE` (`OBJECT_GROWTH_TREND`) and the
ORA-01653 / 01654 / 01688 error pages. Removed: default 85%/97% thresholds and the undo/temp remark,
the "30 TB" figure and the old ORA-01653 message text (current wording differs).
Method: documentation only; no commands were run.
