---
id: computing-software.database-administration.oracle-database.sql-trace-10046-and-tkprof
name: sql-trace-10046-and-tkprof
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, sql-trace, event-10046, tkprof, trcsess, dbms-monitor, performance-tuning]
level: advanced
status: docs-checked
description: "Trace an Oracle session or service with DBMS_MONITOR (event 10046 with waits and binds), consolidate with trcsess, and summarize with tkprof."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/performing-application-tracing.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_MONITOR.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL trace (10046) and tkprof

AWR/ASH show sampled, system-wide data. An extended SQL trace records every call for one session, with optional wait
and bind detail, so you can see where a job's time went.

## Enable
Check `TIMED_STATISTICS` (default true when `STATISTICS_LEVEL` is `TYPICAL` or `ALL`, false for `BASIC`),
`MAX_DUMP_FILE_SIZE` (default `UNLIMITED`) and `DIAGNOSTIC_DEST` first.
```sql
-- a specific session (from v$session)
EXEC DBMS_MONITOR.SESSION_TRACE_ENABLE(session_id => 123, serial_num => 4567, waits => TRUE, binds => TRUE);
EXEC DBMS_MONITOR.SESSION_TRACE_DISABLE(session_id => 123, serial_num => 4567);
-- every session of a service/module/action (connection pools: you don't know the SID in advance)
EXEC DBMS_MONITOR.SERV_MOD_ACT_TRACE_ENABLE(service_name => 'sales_batch', module_name => 'NIGHTLY_LOAD', waits => TRUE, binds => FALSE);
EXEC DBMS_MONITOR.SERV_MOD_ACT_TRACE_DISABLE(service_name => 'sales_batch', module_name => 'NIGHTLY_LOAD');
-- your own session
ALTER SESSION SET TRACEFILE_IDENTIFIER = 'slow_report';   -- becomes part of the trace file name
ALTER SESSION SET EVENTS '10046 trace name context forever, level 8';   -- level 8 writes wait events
```
In `DBMS_MONITOR`, `waits` defaults to TRUE and `binds` to FALSE. `module_name` is optional: omitted, the whole
service is traced. `CLIENT_ID_TRACE_ENABLE` traces by client identifier. `DBA_ENABLED_TRACES` shows outstanding
traces and how each was enabled.

## Find and merge the files
Trace files live under the ADR home set by `DIAGNOSTIC_DEST`; the documentation's example path has the form
`.../diag/rdbms/<db>/<inst>/trace/<inst>_ora_<pid>.trc`. In a shared server configuration one session's trace is
scattered over several process files; `trcsess` consolidates them. You must give one of `session`, `clientid`,
`service`, `action` or `module` (several options are combined); `session` is `index.serial` as in `V$SESSION`.
```
trcsess output=batch.trc service=sales_batch module=NIGHTLY_LOAD *.trc
```
With no trace files listed, `trcsess` reads all files in the current directory. Run `tkprof` on its output.

## Summarize with tkprof
```bash
tkprof input.trc slow_report.txt sort=exeela,fchela,prsela sys=no waits=yes
```
`tkprof input_file output_file` are the required arguments. `waits=yes` (default) summarizes wait events; `sort`
orders statements descending by the sum of the listed options (`EXEELA`, `FCHELA`, `PRSELA` are elapsed time
executing, fetching and parsing); without `sort`, statements appear in order of first use. If a cursor was not
closed, tkprof output lacks the actual plan: use its `explain` option. Wait events are also summed over the whole
trace at the end of the report.

## Gotchas
- Wait and bind detail makes trace files large: trace a bounded window and mind `MAX_DUMP_FILE_SIZE`.
- If trace files belong to another OS user, you need permission to read them with `tkprof`.

## Verify
The tkprof report's total elapsed time roughly matches the observed job duration, and the top statement and wait
event explain most of it.

## Checked
2026-11-09. Read the 19c Performance Tuning Guide (performing application tracing: trace file parameters,
`TRACEFILE_IDENTIFIER`, `trcsess`, `tkprof` syntax, sort options and wait events, `DBA_ENABLED_TRACES`) and the
`DBMS_MONITOR` reference (procedure signatures and defaults). Removed as not stated there: the level 4/12 meanings,
the `v$diag_info`/`v$process` trace-file queries, the tuning pattern rules of thumb, the `orasrp`/Method R/Trace
Analyzer remark and the "40 minutes" framing.
Method: documentation only; no commands were run.
