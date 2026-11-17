---
id: computing-software.database-administration.sql-server.blocking-and-deadlock-graphs
name: blocking-and-deadlock-graphs
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, blocking, deadlock, deadlock-graph, blocked-process-report, head-blocker, lck-m, xml-deadlock-report, rcsi, wait-stats, dmv]
level: advanced
status: docs-checked
description: "Find SQL Server head blockers live, capture blocked-process reports and deadlock graphs with Extended Events, and fix the access patterns behind them."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-deadlocks-guide
  - https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/performance/understand-resolve-blocking
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/blocked-process-threshold-server-configuration-option
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/optimized-locking
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blocking and deadlock graphs

## Live blocking: find the head blocker
```sql
SELECT r.session_id, r.blocking_session_id, r.wait_type, r.wait_time/1000 AS wait_s,
       r.wait_resource, DB_NAME(r.database_id) db, t.text
FROM sys.dm_exec_requests r CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.blocking_session_id <> 0;
-- the head blocker is a blocking_session_id that is not itself blocked; often idle:
SELECT s.session_id, s.status, s.open_transaction_count, s.last_request_end_time,
       s.host_name, s.program_name, c.most_recent_sql_handle
FROM sys.dm_exec_sessions s JOIN sys.dm_exec_connections c ON c.session_id = s.session_id
WHERE s.session_id = <head>;
```
A "sleeping" head blocker with `open_transaction_count > 0` = app opened a transaction
and never committed (missing commit on an error path, or user prompt mid-transaction).
`KILL <spid>` rolls it back; rollback of a long transaction can take as long as the work.
`sp_WhoIsActive @find_block_leaders = 1` adds a `blocked_session_count` column that counts sessions blocked directly or indirectly by each session.

## Capture blocking after the fact: blocked process report
```sql
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'blocked process threshold', 15; RECONFIGURE;   -- seconds; 0 disables; very low values flood the report
CREATE EVENT SESSION blocking ON SERVER
ADD EVENT sqlserver.blocked_process_report
ADD TARGET package0.event_file (SET filename = N'<XE_DIR>\blocking.xel', max_file_size = 64)
WITH (STARTUP_STATE = ON);
ALTER EVENT SESSION blocking ON SERVER STATE = START;
```
Each report has `<blocked-process>` and `<blocking-process>` with input buffers;
The event is generated once per reporting interval for each blocked task, on a best-effort basis, and not for system tasks.

## Deadlocks
Already captured by the `system_health` session:
```sql
SELECT CAST(event_data AS xml) AS deadlock
FROM sys.fn_xe_file_target_read_file('system_health*.xel', NULL, NULL, NULL)
WHERE object_name = 'xml_deadlock_report';
```
Save the XML as `.xdl` and open in SSMS for the graph; `sp_BlitzLock` summarises many.
Read it: victim process, each process's `inputbuf` and isolation level, and the
resource list (keylock/pagelock/objectlock with index names and lock modes).

## Typical fixes
- **Access objects in the same order** in every transaction.
- **Covering index** so a reader does not need a key lookup that collides with a
  writer (classic key lookup deadlock on the clustered + nonclustered index).
- Keep transactions short; no user interaction or remote calls inside them.
- **RCSI** (`ALTER DATABASE appdb SET READ_COMMITTED_SNAPSHOT ON`) removes
  reader/writer blocking and update locks are not used, which reduces deadlocks; it costs version store space and changes semantics for code
  relying on blocking reads.
- `SERIALIZABLE` causes range-lock
  deadlocks; check the isolation level in the graph.
- Retry deadlock victims (error 1205) in the app; deadlocks will never be zero.
- Optimized locking (SQL Server 2025 and Azure SQL Database): TID locking holds one transaction-ID lock instead of many row or key locks, and lock after qualification (needs RCSI) checks predicates against the latest committed version without locking first.

## Verify
- [ ] Blocked process threshold + XE session in place before the next incident.
- [ ] Deadlock count trend tracked (`system_health` `xml_deadlock_report` events).
- [ ] App retries 1205 with backoff.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: blocked process threshold page for SQL Server 2025 (sp_configure option, 0 to 86,400 seconds, 0 disables, low values flood reports, once per interval for each blocked task, best effort, not for system tasks, effective immediately), Learn guidance on system_health xml_deadlock_report read via sys.fn_xe_file_target_read_file and saved as .xdl for the SSMS graph, optimized locking article (TID locking, LAQ requires RCSI, SQL Server 2025 and Azure SQL), deadlocks guide (RCSI means no update locks), sp_WhoIsActive @find_block_leaders (blocked_session_count; per dbatools help text), sp_BlitzLock (First Responder Kit deadlock analysis). Removed as unconfirmed: the 5+ second recommendation, the Michael J Swart viewer, the .NET TransactionScope remark, the tempdb-specific version store claim and the Number of Deadlocks/sec counter.
Method: documentation only; no commands were run.
