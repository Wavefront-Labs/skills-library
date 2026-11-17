---
id: computing-software.database-administration.sql-server.maxdop-and-cost-threshold-for-parallelism
name: maxdop-and-cost-threshold-for-parallelism
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, sp-configure, sql-server-configuration, maxdop, cost-threshold-for-parallelism, cxpacket, cxconsumer, parallelism, numa]
level: practitioner
status: docs-checked
description: "Set SQL Server MAXDOP and cost threshold for parallelism from NUMA layout and workload, at server, database and query level, and read CXPACKET waits correctly."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/configure-the-max-degree-of-parallelism-server-configuration-option
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/configure-the-cost-threshold-for-parallelism-server-configuration-option
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MAXDOP and cost threshold for parallelism

**Goal:** big queries go parallel efficiently, small OLTP queries stay serial, and
one query cannot grab every core.

## Microsoft's MAXDOP guidance (SQL Server 2016+)
| Server | Logical processors per NUMA node | MAXDOP |
|---|---|---|
| Single NUMA node | <= 8 | at or under the number of logical processors |
| Single NUMA node | > 8 | 8 |
| Multiple NUMA nodes | <= 16 | at or under the logical processors per NUMA node |
| Multiple NUMA nodes | > 16 | half the logical processors per NUMA node, max 16 |
"NUMA node" means the soft-NUMA nodes SQL Server 2016+ creates automatically (more than eight physical cores per node/socket),
or hardware nodes if soft-NUMA is disabled. Use the same guidance for Resource Governor `MAX_DOP`.
Setup in 2019+ proposes a value from the processor count. 0 means up to 64 processors and is not the recommended value
for most cases; 1 suppresses parallel plans; the limit is per task, not per query.

## Cost threshold
Default `cost threshold for parallelism` = 5, valid range 0-32,767. Microsoft calls 5 "a starting point, not a recommendation":
on modern systems raising it keeps smaller OLTP queries serial; change in small increments and observe a full business cycle.
Cost is the sum of estimated operator costs, a relative measure, not runtime. Signs it is too low: many CPU-light
queries parallel (`is_parallel_plan = 1` in Query Store), `CXPACKET`/`CXCONSUMER` dominating waits, possibly `THREADPOOL` and
`SOS_SCHEDULER_YIELD`. Too high: CPU-heavy queries stay serial and `SOS_SCHEDULER_YIELD` dominates.
It is ignored with one logical processor, one processor available through affinity mask, or MAXDOP 1.

```sql
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'max degree of parallelism', 8; RECONFIGURE;       -- example value, see table above
EXEC sp_configure 'cost threshold for parallelism', 50; RECONFIGURE;  -- example value only
```
Both take effect immediately (no restart); changing them needs `ALTER SETTINGS`. Per database, overriding the server:
```sql
ALTER DATABASE SCOPED CONFIGURATION SET MAXDOP = 4;
```
Per query: `OPTION (MAXDOP 1)` or a Query Store hint; Resource Governor workload groups (`MAX_DOP`) can cap it too.
Azure SQL Database: new databases default to MAXDOP 8 (database scoped config) and `cost threshold for parallelism` cannot be set there.

## Reading the waits
- `CXPACKET` and `CXCONSUMER` are the parallelism waits Microsoft lists when the cost threshold is too low.
- High parallelism waits are a symptom, not a reason to set MAXDOP 1 globally: look at the plans, indexes and estimates first.

## Gotchas
- The server MAXDOP also controls parallelism of index builds/rebuilds and `DBCC CHECKTABLE`/`CHECKDB`/`CHECKFILEGROUP`
  (trace flag 2528 disables parallel checks); override per operation with the `MAXDOP` index option instead of server-wide 1.
- Each parallel task uses one worker and one scheduler, so very high DOP with many sessions can contribute to `THREADPOOL` waits.
- SQL Server 2022+ adds DOP feedback (intelligent query processing) for repeating queries.

## Verify
```sql
SELECT name, value_in_use FROM sys.configurations
WHERE name IN ('max degree of parallelism','cost threshold for parallelism');
SELECT * FROM sys.database_scoped_configurations WHERE name = 'MAXDOP';
```
Compare `sys.dm_os_wait_stats` CXPACKET/THREADPOOL and query duration before/after.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 max degree of parallelism and cost threshold for parallelism pages (2017-2025, 2014-and-earlier table noted).
Confirmed: the 2016+ NUMA table and soft-NUMA basis, 2019 setup recommendation, MAXDOP 0/1 semantics, override levels, dynamic change, cost threshold default 5 and range, tuning indicators, CHECKDB and TF 2528, Azure SQL Database default 8. Removed the unconfirmed 30-50 target, the "1990s" remark, CXCONSUMER version gate and memory-grant claim.
Method: documentation only; no commands were run.
