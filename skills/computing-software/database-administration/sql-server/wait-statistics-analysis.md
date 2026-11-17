---
id: computing-software.database-administration.sql-server.wait-statistics-analysis
name: wait-statistics-analysis
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, wait-stats, sys-dm-os-wait-stats, dmv, cxpacket, pageiolatch, writelog, lck-m, sos-scheduler-yield, signal-wait, performance-troubleshooting]
level: advanced
status: docs-checked
description: "Diagnose SQL Server bottlenecks from sys.dm_os_wait_stats deltas: filter benign waits, read signal vs resource time, and map top waits to causes."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-os-wait-stats-transact-sql
  - https://www.sqlskills.com/help/waits/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wait statistics analysis

**Goal:** answer "what is SQL Server waiting on?" from data, then go to the right
deeper tool, instead of guessing from CPU graphs.

## Take a delta, not cumulative totals
`sys.dm_os_wait_stats` is cumulative since restart (or `DBCC SQLPERF('sys.dm_os_wait_stats', CLEAR)`).
Snapshot, wait during the problem, snapshot again:
```sql
SELECT wait_type, waiting_tasks_count, wait_time_ms, signal_wait_time_ms
INTO #w1 FROM sys.dm_os_wait_stats;
WAITFOR DELAY '00:05:00';
SELECT w2.wait_type,
       w2.wait_time_ms - w1.wait_time_ms AS wait_ms,
       w2.signal_wait_time_ms - w1.signal_wait_time_ms AS signal_ms,
       w2.waiting_tasks_count - w1.waiting_tasks_count AS waits,
       (w2.wait_time_ms - w1.wait_time_ms) * 1.0 / NULLIF(w2.waiting_tasks_count - w1.waiting_tasks_count,0) AS avg_ms
FROM sys.dm_os_wait_stats w2 JOIN #w1 w1 ON w1.wait_type = w2.wait_type
WHERE w2.wait_type NOT LIKE 'SLEEP%'   -- also exclude other benign/idle waits (see the sqlskills wait types library)
ORDER BY wait_ms DESC;
```

## Signal vs resource
`signal_wait_time_ms` = difference between the time the waiting thread was signaled and when it started running.
A large signal share together with `SOS_SCHEDULER_YIELD` points to CPU pressure.

## Map top waits to causes
| Wait | Usual meaning | Next step |
|---|---|---|
| `PAGEIOLATCH_SH/EX` | reading data pages from disk | scans from missing indexes, low memory; `sys.dm_io_virtual_file_stats` latency |
| `WRITELOG` | log flush latency | log disk latency, tiny transactions in loops, AG sync commit |
| `CXPACKET` / `CXCONSUMER` | parallelism | normal in moderation; check MAXDOP / cost threshold, skewed parallel plans |
| `LCK_M_*` | blocking | blocking chain, `blocked-process-report` |
| `SOS_SCHEDULER_YIELD` | CPU-bound queries | top CPU queries in Query Store |
| `RESOURCE_SEMAPHORE` | waiting for memory grants | oversized grants, spills, memory |
| `PAGELATCH_*` | in-memory page contention | tempdb allocation, last-page insert hotspot |
| `ASYNC_NETWORK_IO` | client not consuming results | app row-by-row fetch, huge result sets |
| `HADR_SYNC_COMMIT` | waiting for sync AG secondary | secondary log disk / network |
| `THREADPOOL` | worker exhaustion | blocking pile-up, too much parallelism; urgent |

## Per-session and per-query
```sql
SELECT * FROM sys.dm_exec_session_wait_stats WHERE session_id = 87 ORDER BY wait_time_ms DESC;
```
Azure SQL Database: `sys.dm_db_wait_stats` (database scoped).

## Gotchas
- High wait time with a low count can be one long event; look at avg_ms.
- Never tune by cumulative-since-restart numbers on a server that has been up for months.
- Waits tell you where time goes, not whether it is a problem: compare with a baseline.

## Verify
- [ ] A baseline delta captured at normal load exists to compare against.
- [ ] Top 3 non-benign waits during the incident are mapped to an evidence-backed cause.

## Checked
2026-10-28. Confirmed against the sys.dm_os_wait_stats page: cumulative counters with DBCC SQLPERF CLEAR, signal_wait_time_ms definition, wait type descriptions for PAGEIOLATCH_SH, WRITELOG, CXPACKET, CXCONSUMER, LCK_M_*, SOS_SCHEDULER_YIELD, RESOURCE_SEMAPHORE, PAGELATCH_EX (last-page insert), ASYNC_NETWORK_IO, HADR_SYNC_COMMIT, THREADPOOL; sys.dm_exec_session_wait_stats; sys.dm_db_wait_stats listed for Azure SQL.
Removed unconfirmed claims: the idle-wait exclusion list, the 20-25 percent signal-wait threshold, the sp_BlitzFirst and Paul Randal filter-list attribution, Query Store wait stats view and version.
Method: documentation only; no commands were run.
