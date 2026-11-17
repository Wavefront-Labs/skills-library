---
id: computing-software.database-administration.oracle-database.online-redo-log-groups-and-sizing
name: online-redo-log-groups-and-sizing
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle-instance, online-redo-logs, redo-log-groups, log-switch, checkpoint-not-complete]
level: practitioner
status: docs-checked
description: "Inspect, multiplex, add and drop Oracle online redo log groups and members safely, and use ARCHIVE_LAG_TARGET to bound switch intervals."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-the-redo-log.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-LOG.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Online redo log groups and sizing

## Inspect
```sql
SELECT group#, thread#, sequence#, bytes/1024/1024 AS mb, members, archived, status FROM v$log;
SELECT group#, member, type, status FROM v$logfile ORDER BY group#;
-- switches per hour over the last week
SELECT TO_CHAR(first_time, 'YYYY-MM-DD HH24') hr, COUNT(*) switches
FROM v$log_history WHERE first_time > SYSDATE - 7
GROUP BY TO_CHAR(first_time, 'YYYY-MM-DD HH24') ORDER BY 1;
```
`V$LOG.STATUS`: `UNUSED` (never written, e.g. just added), `CURRENT` (being written),
`ACTIVE` (not current, still needed for crash recovery), `INACTIVE` (no longer needed for instance recovery),
`CLEARING` and `CLEARING_CURRENT` (being re-created after `CLEAR LOGFILE`).
Many switches per minute usually mean logs are too small; size from your own peak switch rate.

## Group rules
An instance needs **at least two groups** of redo log files, whatever the number of members per group.
You can drop a group only if it is inactive; to drop the current group, force a log switch first.

## Resizing (you cannot resize; add new, drop old)
```sql
ALTER DATABASE ADD LOGFILE THREAD 1 GROUP 11 ('+DATA', '+FRA') SIZE 4G;
ALTER DATABASE ADD LOGFILE THREAD 1 GROUP 12 ('+DATA', '+FRA') SIZE 4G;
ALTER DATABASE ADD LOGFILE THREAD 1 GROUP 13 ('+DATA', '+FRA') SIZE 4G;
-- cycle until the old groups are INACTIVE
ALTER SYSTEM SWITCH LOGFILE;
ALTER SYSTEM CHECKPOINT;
ALTER DATABASE DROP LOGFILE GROUP 1;      -- only when INACTIVE and archived
```
In RAC, add groups per thread.

## Multiplexing
Keep at least two members per group on separate disks: dropping a member is allowed even if it leaves groups
asymmetric, but fix that straight away to remove the single point of failure.
```sql
ALTER DATABASE ADD LOGFILE MEMBER '+FRA' TO GROUP 11;
```
You can drop a member only if it is not part of an active or current group; force a log switch first.

## Gotchas
- Without Oracle Managed Files, dropping a group or member only updates the control file; delete the OS file
  yourself after confirming the drop completed.
- `ARCHIVE_LAG_TARGET` (seconds, dynamic, `ALTER SYSTEM SET`) bounds how long the current log can go before a
  switch; it can be used even without a standby, and must have the same value on all RAC instances.
- Never drop the CURRENT or ACTIVE group.

## Verify
`v$log` shows all groups at the new size with two members each and the switch rate is acceptable at peak.

## Checked
2026-11-01. Confirmed against the Oracle 19c Administrator's Guide (Managing the Redo Log) and V$LOG reference:
status values, minimum of two groups, drop rules, OS files not deleted, asymmetric multiplexing, ARCHIVE_LAG_TARGET
behaviour (dynamic, usable without standby, same value across RAC). Removed as unconfirmed: the 3-5 switches per hour
target, OPTIMAL_LOGFILE_SIZE, the three-group advice, alert-log and wait-event text, standby redo log sizing, and the
INVALID member remark.
Method: documentation only; no commands were run.
