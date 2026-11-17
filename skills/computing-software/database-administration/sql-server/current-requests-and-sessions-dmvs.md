---
id: computing-software.database-administration.sql-server.current-requests-and-sessions-dmvs
name: current-requests-and-sessions-dmvs
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, dmv, dm-exec-requests, dm-exec-sessions, live-troubleshooting, blocking, query-plan]
level: practitioner
status: docs-checked
description: "See what SQL Server is running now with sys.dm_exec_requests, sessions and connections: text, plan, waits, blocking, tempdb use and open transactions."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-requests-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-sessions-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-query-statistics-xml-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/query-profiling-infrastructure
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-db-session-space-usage-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Current requests and sessions DMVs

## What is running
```sql
SELECT r.session_id, r.status, r.command, r.blocking_session_id AS blocked_by,
       r.wait_type, r.wait_time, r.last_wait_type, r.cpu_time, r.total_elapsed_time,
       r.logical_reads, r.writes, r.granted_query_memory * 8 AS grant_kb, r.dop,
       DB_NAME(r.database_id) AS db, s.login_name, s.host_name, s.program_name,
       SUBSTRING(t.text, r.statement_start_offset/2 + 1,
         (CASE r.statement_end_offset WHEN -1 THEN DATALENGTH(t.text)
          ELSE r.statement_end_offset END - r.statement_start_offset)/2 + 1) AS statement,
       p.query_plan
FROM sys.dm_exec_requests r
JOIN sys.dm_exec_sessions s ON s.session_id = r.session_id
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
OUTER APPLY sys.dm_exec_query_plan(r.plan_handle) p
WHERE s.is_user_process = 1 AND r.session_id <> @@SPID
ORDER BY r.total_elapsed_time DESC;
```
- `statement_start/end_offset` extract the current statement within a batch/procedure.
- `sys.dm_exec_query_statistics_xml(session_id)` (2016 SP1+) returns the in-flight plan with partial statistics for a running request; it works under standard or lightweight profiling, and lightweight profiling is on by default from SQL Server 2019.
- `percent_complete` populates for BACKUP DATABASE, RESTORE DATABASE, DBCC CHECKDB/CHECKFILEGROUP/CHECKTABLE, DBCC SHRINKFILE/SHRINKDATABASE, ALTER INDEX REORGANIZE, ROLLBACK, recovery and TDE encryption.
- For parallel row-mode requests only the coordinator task is visible: `reads`, `writes`, `logical_reads` and `row_count` are not updated for it, while the wait columns and `granted_query_memory` are.
- Needs `VIEW SERVER STATE` (`VIEW SERVER PERFORMANCE STATE` from SQL Server 2022), otherwise you see only your own session.

## Sleeping sessions with open transactions (silent blockers)
```sql
SELECT s.session_id, s.login_name, s.host_name, s.program_name, s.status,
       s.open_transaction_count, s.last_request_end_time,
       DATEDIFF(SECOND, s.last_request_end_time, GETDATE()) AS idle_s
FROM sys.dm_exec_sessions s
WHERE s.open_transaction_count > 0 AND s.status = 'sleeping'
ORDER BY s.last_request_end_time;
```
These do not appear in `dm_exec_requests` (no request running) but hold locks. Last statement:
`SELECT text FROM sys.dm_exec_connections c CROSS APPLY sys.dm_exec_sql_text(c.most_recent_sql_handle) WHERE c.session_id = 72;`

## tempdb consumption per session
```sql
SELECT session_id, (user_objects_alloc_page_count + internal_objects_alloc_page_count) * 8 / 1024 AS alloc_mb
FROM sys.dm_db_session_space_usage ORDER BY alloc_mb DESC;
```
These counters are updated only when tasks finish, so they do not show work still running (see `sys.dm_db_task_space_usage` for running tasks).

## Connections
`sys.dm_exec_connections`: client address, protocol, `encrypt_option`, `auth_scheme`
(KERBEROS vs NTLM), `net_packet_size`.

## Gotchas
- `wait_time` is for the current wait only; for cumulative per-session waits use
  `sys.dm_exec_session_wait_stats`.
- `blocking_session_id` negative values: -2 orphaned distributed transaction, -3 deferred recovery transaction, -4 latch
  owner could not be determined (internal state transition), -5 latch owner not tracked for this latch type (the session is waiting on an asynchronous action).
- For a richer one-call view use `sp_WhoIsActive @find_block_leaders = 1`.

## Verify
The query returns the long-running statement and its plan; the session's
`blocked_by` chain leads to a head blocker you can investigate or `KILL`.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: sys.dm_exec_requests page for SQL Server 2025 (column names and types, granted_query_memory in pages, dop from 2016, percent_complete command list, blocking_session_id values -2 to -5, coordinator-task note, permissions incl. VIEW SERVER PERFORMANCE STATE in 2022), sys.dm_exec_query_statistics_xml and query profiling infrastructure pages (2016 SP1, lightweight profiling default in 2019), sys.dm_db_session_space_usage (tempdb page counters updated at task end), sys.dm_exec_connections (encrypt_option, auth_scheme, net_packet_size, most_recent_sql_handle), sys.dm_exec_sessions (open_transaction_count, last_request_end_time), sp_WhoIsActive @find_block_leaders via dbatools help text. Wrong in the draft: -3 was missing from the blocking_session_id list. Removed as unconfirmed: sp_WhoIsActive @get_plans.
Method: documentation only; no commands were run.
