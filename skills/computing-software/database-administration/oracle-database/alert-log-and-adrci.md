---
id: computing-software.database-administration.oracle-database.alert-log-and-adrci
name: alert-log-and-adrci
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-instance, alert-log, adrci, automatic-diagnostic-repository, adr, trace-files, incident-package, ora-00600, ora-07445, v-diag-alert-ext]
level: practitioner
status: docs-checked
description: "Find and read the Oracle alert log and trace files in the ADR, use adrci to view, purge and package incidents for Oracle Support, and query alerts in SQL."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/diagnosing-and-resolving-problems.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-adr-command-interpreter-adrci.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alert log and ADRCI

## Where things are
```sql
SELECT name, value FROM v$diag_info;   -- ADR Base, ADR Home, Diag Trace, Diag Alert, Default Trace File
```
Layout: `<ADR_BASE>/diag/rdbms/<db_unique_name>/<instance>/` with `trace/`
(alert_<SID>.log text alert log and process trace files), `alert/` (log.xml),
`incident/`, `cdump/`. Listener and ASM have their own ADR homes (`diag/tnslsnr`, `diag/asm`).

## Read the alert log
```bash
tail -f $ORACLE_BASE/diag/rdbms/orcl/orcl/trace/alert_orcl.log
```
```sql
-- from SQL (12c+), e.g. last day's errors
SELECT originating_timestamp, message_text
FROM v$diag_alert_ext
WHERE originating_timestamp > SYSTIMESTAMP - INTERVAL '1' DAY
  AND message_text LIKE '%ORA-%'
ORDER BY originating_timestamp;
```
What to alert on: `ORA-00600` / `ORA-07445` (internal errors -> incidents),
`ORA-01555`, `ORA-1653/1654` (unable to extend), `ORA-00257`/`ORA-19815` (archiver/FRA
full), `ORA-04031` (shared pool), `Checkpoint not complete` (redo too small),
`TNS-` errors, instance terminations and deadlocks (`ORA-00060`, trace file named).

## ADRCI
```bash
adrci
adrci> show homes
adrci> set home diag/rdbms/orcl/orcl
adrci> show alert -tail 100 -f                        # follow
adrci> show alert -p "message_text like '%ORA-600%'"  # filter
adrci> show problem                                  # grouped by problem key
adrci> show incident -mode detail -p "incident_id=12345"
adrci> ips pack incident 12345 in /u01/pkg              # zip for Oracle Support SR; path is a directory
adrci> show control                                   # retention policies (hours)
adrci> set control (SHORTP_POLICY = 168, LONGP_POLICY = 720)   # hours: 168 = 7 days, 720 = 30 days (defaults are 720 and 8760)
adrci> purge -age 10080 -type trace                   # minutes
```
Non-interactive (cron purge for every home):
```bash
for h in $(adrci exec="show homes" | grep diag); do
  adrci exec="set home $h; purge -age 10080 -type trace; purge -age 43200 -type incident"
done
```
`purge -type alert` removes old XML alert (`log.xml`) data, but ADR does not rotate the text `alert_<SID>.log`: rotate `alert_<SID>.log` with logrotate
(copytruncate) or move it aside; Oracle recreates it (rotation behaviour is not covered by the ADRCI reference; confirm on your platform).

## Trace files
Process traces named `<SID>_<proc>_<ospid>.trc`. Find one for a session:
```sql
SELECT p.tracefile FROM v$session s JOIN v$process p ON p.addr = s.paddr WHERE s.sid = 123;
```
Enable 10046 SQL trace for a session: `EXEC DBMS_MONITOR.SESSION_TRACE_ENABLE(123, 4567, waits => TRUE, binds => FALSE);`
then summarise with `tkprof <file>.trc out.txt sort=exeela`.

## Verify
- [ ] Alert log monitored for the ORA- list above (OEM, Prometheus exporter, or grep job).
- [ ] ADR retention set and a purge job keeps `diag` filesystem below threshold.
- [ ] `ips pack` tested so packaging for an SR is not learnt mid-incident.

## Checked
Date 2026-10-22. Oracle Database 19c Utilities (ADRCI) and Database Reference. Confirmed: `show alert -tail N -f` and
`-p` predicate, `ips pack incident <id> ... in <path>`, `exec="cmd; cmd"`, `set control` policy units are hours with
defaults SHORTP 720 and LONGP 8760, `purge -age` is in minutes with `-type` ALERT/INCIDENT/TRACE/CDUMP/HM/UTSCDMP,
`V$DIAG_ALERT_EXT` has `ORIGINATING_TIMESTAMP` and `MESSAGE_TEXT`. Corrected: policy comment, purge of XML alert log.
Method: documentation only; no commands were run.
