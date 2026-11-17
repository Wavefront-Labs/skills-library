---
id: computing-software.database-administration.sql-server.performance-baselines-with-perfmon-counters
name: performance-baselines-with-perfmon-counters
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, performance-baseline, perfmon-counters, dm-os-performance-counters, page-life-expectancy, batch-requests, monitoring]
level: practitioner
status: docs-checked
description: "Build a SQL Server performance baseline from perfmon counters and sys.dm_os_performance_counters, handle cumulative counters correctly, and spot deviations."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-os-performance-counters-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance-monitor/use-sql-server-objects
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/establish-a-performance-baseline
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Performance baselines with perfmon counters

Without a baseline, "the server is slow" has no reference. Capture the same counters every
few minutes for weeks, then compare incidents against the same hour/weekday.

## Counters worth collecting
| Counter | Note |
|---|---|
| SQLServer:SQL Statistics \ Batch Requests/sec | workload volume, the denominator for everything else |
| SQL Compilations/sec, SQL Re-Compilations/sec | compare the compilation rate with Batch Requests/sec |
| Buffer Manager \ Page life expectancy (per NUMA node in Buffer Node) | compare to its own baseline, not a fixed threshold |
| Buffer Manager \ Lazy writes/sec, Page reads/sec | memory pressure |
| Memory Manager \ Memory Grants Pending | compare to baseline |
| General Statistics \ User Connections | |
| Locks \ Lock Waits/sec, Number of Deadlocks/sec | |
| Access Methods \ Forwarded Records/sec, Full Scans/sec | |
| Processor \ % Processor Time, LogicalDisk \ Avg. Disk sec/Read and /Write | OS side |

## Collect from T-SQL
Counters with `cntr_type = 272696576` are cumulative per-second counters: you must diff two samples.
```sql
CREATE TABLE dba.PerfCounter (captured_at datetime2 NOT NULL, object_name nvarchar(128),
  counter_name nvarchar(128), instance_name nvarchar(128), cntr_value bigint, cntr_type int);

INSERT dba.PerfCounter
SELECT sysdatetime(), RTRIM(object_name), RTRIM(counter_name), RTRIM(instance_name), cntr_value, cntr_type
FROM sys.dm_os_performance_counters
WHERE counter_name IN ('Batch Requests/sec','SQL Compilations/sec','SQL Re-Compilations/sec',
  'Page life expectancy','Lazy writes/sec','Memory Grants Pending','User Connections',
  'Lock Waits/sec','Number of Deadlocks/sec','Forwarded Records/sec');
```
Schedule every 5 minutes in an Agent job. Per-second rate between samples:
```sql
SELECT cur.captured_at, cur.counter_name,
  (cur.cntr_value - prev.cntr_value) / NULLIF(DATEDIFF(second, prev.captured_at, cur.captured_at),0) AS per_sec
FROM dba.PerfCounter cur
CROSS APPLY (SELECT TOP 1 * FROM dba.PerfCounter p WHERE p.counter_name = cur.counter_name
  AND p.instance_name = cur.instance_name AND p.captured_at < cur.captured_at ORDER BY p.captured_at DESC) prev
WHERE cur.cntr_type = 272696576;
```
Ratio counters (`537003264`) divide by their `base` counter. A restart resets cumulative values: discard negative deltas.

## Collect from the OS
Collect the same counters from the OS with a Performance Monitor data collector set. Named instances use `MSSQL$<instance name>:` object names (see the Use SQL Server objects page).

## Use the baseline
Compare p50/p95 per hour-of-week; alert on sustained deviation (for example PLE far below its baseline
for a sustained period), not absolute thresholds. Add wait stats snapshots alongside counters.

## Checked

2026-10-28. Confirmed in the sys.dm_os_performance_counters page: cntr_type values 272696576 and 537003264, base counters for ratio types, and that DMV values do not persist across a restart (sqlserver_start_time in sys.dm_os_sys_info). Removed: the 10% compilation rule, the fixed 300 PLE value, the memory-grants rule, the logman command and options, the dbatools counter-sample reference, the 90-day retention figure, the 50% / 15 minute alert example.

Method: documentation only; no commands were run.

## Verify
Job running, retention set (purge old rows), and a chart of batch requests/sec for the past week looks like the known business cycle.
