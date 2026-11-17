---
id: computing-software.database-administration.sql-server.extended-events-sessions
name: extended-events-sessions
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, extended-events, xevents, event-file, ring-buffer, system-health, sql-trace-replacement, query-tracing, dmv]
level: advanced
status: gated
description: "Build lightweight SQL Server Extended Events sessions with predicates and file targets, read them with T-SQL, and use the built-in system_health session."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/extended-events/extended-events
  - https://learn.microsoft.com/en-us/sql/relational-databases/extended-events/use-the-system-health-session
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/create-event-session-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-functions/sys-fn-xe-file-target-read-file-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extended Events sessions

**Goal:** capture exactly the events you need (slow queries, errors, waits) at low
overhead; Extended Events replaces the deprecated SQL Trace and SQL Server Profiler and is described by Microsoft as lightweight.

## Slow-query session
```sql
CREATE EVENT SESSION slow_queries ON SERVER
ADD EVENT sqlserver.rpc_completed (
    ACTION (sqlserver.client_app_name, sqlserver.client_hostname, sqlserver.database_name,
            sqlserver.username, sqlserver.query_hash, sqlserver.sql_text)
    WHERE duration > 1000000                       -- 1000000 = 1 s assumes microseconds (gated: unconfirmed, source is paywalled or blocked)
      AND sqlserver.database_name = N'appdb'),
ADD EVENT sqlserver.sql_batch_completed (
    ACTION (sqlserver.client_app_name, sqlserver.database_name, sqlserver.username)
    WHERE duration > 1000000 AND sqlserver.database_name = N'appdb')
ADD TARGET package0.event_file (SET filename = N'<XE_DIR>\slow_queries.xel',
                                max_file_size = 256, max_rollover_files = 8)
WITH (MAX_DISPATCH_LATENCY = 5 SECONDS, EVENT_RETENTION_MODE = ALLOW_SINGLE_EVENT_LOSS,
      STARTUP_STATE = ON);
ALTER EVENT SESSION slow_queries ON SERVER STATE = START;
```
Rules: put filters in the `WHERE` predicate: if it is false the event is dropped and actions and targets are skipped (each predicate is limited to 3,000
characters). Actions add work to every event that passes, so collect only what you need. Session options: `MAX_DISPATCH_LATENCY` defaults to 30 seconds
(minimum 1; 0 or INFINITE flush only when buffers are full), `MAX_MEMORY` defaults to 4 MB, `EVENT_RETENTION_MODE` ALLOW_SINGLE_EVENT_LOSS minimizes impact (NO_EVENT_LOSS can stall
user queries), and `STARTUP_STATE = ON` starts the session when the instance starts (use `ALTER EVENT SESSION ... ON SERVER STATE = START` to start it now).
A session can have only one target of each type. Permissions: `CREATE ANY EVENT SESSION` (2022+) or `ALTER ANY EVENT SESSION`. Azure SQL Database needs
`ON DATABASE` sessions (and `sys.database_event_session_*` views).
The action names in the sample (`client_app_name`, `client_hostname`, `database_name`, `username`, `query_hash`, `sql_text`) and the event `duration` unit were not confirmed against the event and action reference. (gated: unconfirmed, source is paywalled or blocked) The documentation pages used here do not list them; list real names with the `sys.dm_xe_objects` query in "Find events" and read the field description in `sys.dm_xe_object_columns`.

## Read the file
```sql
SELECT x.value('(event/@timestamp)[1]','datetime2') ts,
       x.value('(event/data[@name="duration"]/value)[1]','bigint')/1000 AS ms,   -- /1000 assumes microseconds (gated: unconfirmed, source is paywalled or blocked)
       x.value('(event/action[@name="sql_text"]/value)[1]','nvarchar(max)') AS sql_text
FROM (SELECT CAST(event_data AS xml) x
      FROM sys.fn_xe_file_target_read_file(N'<XE_DIR>\slow_queries*.xel', NULL, NULL, NULL)) t
ORDER BY ms DESC;
```
`sys.fn_xe_file_target_read_file(path, mdpath, initial_file_name, initial_offset)`: the local path must include a file name pattern (one `*` wildcard allowed), `mdpath` can be NULL
from SQL Server 2016, and `initial_file_name`/`initial_offset` must be given together for incremental reads. It needs `VIEW SERVER STATE` (2022+: `VIEW SERVER PERFORMANCE STATE`).
Output columns include `event_data` (XML), `file_name`, `file_offset` and, from 2017, `timestamp_utc`. SSMS can also read .xel files and show live data.

## Targets
- `event_file`: writes XEL files (`filename`, `max_file_size` in MB, `max_rollover_files` as in the example); the usual durable choice.
- `ring_buffer`: in memory; Microsoft recommends setting the target `MAX_MEMORY` parameter to 1,024 KB or less to avoid truncated XML output.
- Others, such as `histogram`, exist: list them and their parameters from `sys.dm_xe_objects` (`object_type = 'target'`) and `sys.dm_xe_object_columns` (customizable columns).

## Built-in sessions
- `system_health`: starts automatically with SQL Server and Azure SQL Managed Instance with no noticeable overhead. It records errors of severity 20 or higher, memory-related errors
  (17803, 701, 802, 8645, 8651, 8657, 8902), non-yielding scheduler problems (17883), detected deadlocks with the deadlock graph, latch waits over 15 seconds, lock waits over 30 seconds,
  long preemptive waits, `sp_server_diagnostics` results and several ring-buffer events. Targets: ring buffer plus event files (5 MB x 4 files, or 100 MB x 10 on Standard/Enterprise).
  Microsoft recommends not stopping, altering or deleting it (restore with the `u_tables.sql` script in the instance's Install folder). Check it first after any incident.
- Azure SQL Database has no built-in `system_health` session; sessions are database-scoped and file targets go to Azure Storage blobs.

## Find events
```sql
SELECT p.name pkg, o.name event, o.description FROM sys.dm_xe_objects o
JOIN sys.dm_xe_packages p ON p.guid = o.package_guid
WHERE o.object_type = 'event' AND o.name LIKE '%wait%';
SELECT s.name, CAST(t.target_data AS xml) AS target_data FROM sys.dm_xe_sessions s JOIN sys.dm_xe_session_targets t ON t.event_session_address = s.address;   -- running sessions
```

## Verify
- [ ] Session has a selective predicate and a size-capped file target.
- [ ] `sys.dm_xe_sessions` shows it running.
- [ ] Debug sessions are stopped and dropped after the investigation.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for Extended Events overview, CREATE EVENT SESSION, Use the system_health session and sys.fn_xe_file_target_read_file (2017-2025).
Confirmed: syntax, predicate behaviour, session option defaults and retention modes, event_file parameters, ring_buffer memory advice, read-file arguments and columns, system_health contents, targets and restore script, permissions, SQL Trace deprecation. The `duration` unit and the action names in the slow-query sample were not on the pages read, so they carry the gated marker and the skill status is `gated`. Removed unconfirmed claims: Profiler being "far heavier", cheap-predicates-first and action-cost advice, `AlwaysOn_health`, histogram/pair_matching descriptions, dbatools, `xml_deadlock_report` event name and the dropped-event check.
Method: documentation only; no commands were run.
