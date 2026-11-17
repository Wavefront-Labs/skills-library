---
id: computing-software.database-administration.sql-server.system-health-session-and-default-trace
name: system-health-session-and-default-trace
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, system-health-session, default-trace, extended-events, deadlock, fn-trace-gettable, sp-server-diagnostics]
level: practitioner
status: docs-checked
description: "Mine SQL Server's always-on diagnostics: deadlocks, long waits and errors from the system_health XE session, and what the deprecated default trace still offers."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/extended-events/use-the-system-health-session
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-functions/sys-fn-xe-file-target-read-file-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-traces-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-functions/sys-fn-trace-gettable-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# system_health session and default trace

The system_health Extended Events session is included with SQL Server and starts automatically
with the Database Engine: the first place to look after an incident when no custom monitoring
was set up. The default trace is the older, deprecated mechanism.

## system_health (Extended Events)
Per the Learn page it collects: `sql_text` and `session_id` for sessions with an error of severity
>= 20 or a memory-related error, non-yielding scheduler problems (error 17883), detected deadlocks
with the deadlock graph, sessions that waited on latches (or other interesting resources) for
> 15 seconds or on locks for > 30 seconds, long preemptive waits, `sp_server_diagnostics` component
results, and ring buffer events for connectivity and security errors.

Microsoft recommends you do not stop, alter or delete the session: changes can be overwritten by a
future product update. If it is deleted, the `u_tables.sql` script in the instance's
`MSSQL\Install` folder restores it, and you then start it with `ALTER EVENT SESSION`.

It writes to a ring buffer target and an event file target. The event file target is limited to
4 files of 5 MB; in Standard and Enterprise editions the limits are 10 files of 100 MB.
Read the file target (the file name accepts `*` as a wildcard):
```sql
SELECT object_name, timestamp_utc, CAST(event_data AS xml) AS event_xml
FROM sys.fn_xe_file_target_read_file('system_health*.xel', NULL, NULL, NULL)
WHERE timestamp_utc > DATEADD(DAY, -1, GETUTCDATE());   -- add a filter on object_name for the event you want
```
`timestamp_utc` needs SQL Server 2017 or later. Ring buffer contents:
```sql
SELECT CAST(xet.target_data AS xml) AS target_data
FROM sys.dm_xe_session_targets xet
JOIN sys.dm_xe_sessions xe ON xe.address = xet.event_session_address
WHERE xe.name = 'system_health';
```
SSMS can also open the event file target with the Extended Events viewer.

## Default trace (deprecated)
`sys.traces` and `sys.fn_trace_gettable` are marked "will be removed in a future version";
Microsoft says to use Extended Events instead. The default trace is the row with `is_default = 1`:
```sql
SELECT path FROM sys.traces WHERE is_default = 1;                 -- needs ALTER TRACE
SELECT * FROM sys.fn_trace_gettable(N'<path to log.trc>', DEFAULT);  -- DEFAULT reads all rollover files
```
`sys.fn_trace_gettable` can read a trace that is still active; it does not load rollover files when the
original file name ends with an underscore and a number. Event names come from `sys.trace_events`.
Which events the default trace records, and its file sizes, are not covered by the pages checked here
(the default trace configuration page needs a sign-in): check the current Learn pages before relying on them.

## Gotchas
- Rolled-over files are lost: copy files off, or build your own Extended Events session for long retention.
- `timestamp_utc` is UTC; convert before correlating with app logs.
- Azure SQL Database has no built-in system_health session; in Azure SQL Managed Instance it exists.

## Verify
The ring buffer query and the file target query both return rows on the instance.

## Checked
2026-10-31. Confirmed against the Learn pages for the system_health session, `sys.fn_xe_file_target_read_file`, `sys.traces` and `sys.fn_trace_gettable`: the collected data, the 5 MB x 4 and 100 MB x 10 file limits, the advice not to alter the session, the restore script, the wildcard and `timestamp_utc` column, `is_default`, the deprecation notices, the ALTER TRACE permission.
Corrected: file retention was attributed to "before 2019 / 2019+" (the page says Standard and Enterprise editions); the advice to drop and recreate the file target was removed.
Removed as unconfirmed: the default trace file count and size, its recorded events and the event-name query, the `sys.configurations` check, the Azure SQL Database telemetry function, the `.xdl` tip and the `AlwaysOn_health` pointer; a Learn page about public server permissions was cited as a source by mistake and was dropped.
Method: documentation only; no commands were run.
