---
id: computing-software.database-administration.sql-server.resource-governor-workload-groups-and-pools
name: resource-governor-workload-groups-and-pools
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, resource-governor, workload-group, resource-pool, classifier-function, max-grant-percent, cap-cpu-percent]
level: advanced
status: docs-checked
description: "Limit CPU, memory grants and IO for SQL Server workloads with Resource Governor pools, workload groups and a classifier function, and monitor their effect."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/resource-governor/resource-governor
  - https://learn.microsoft.com/en-us/sql/relational-databases/resource-governor/create-and-test-a-classifier-user-defined-function
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-resource-governor-workload-groups-transact-sql
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/create-resource-pool-transact-sql
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/create-workload-group-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/resource-governor/resource-governor-classifier-function
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource Governor

Not available in every edition of SQL Server (see Microsoft's editions and supported features pages); also in Azure SQL Managed Instance.
Up to 64 resource pools (40 on Managed Instance). Typical use: stop reporting or ETL sessions from starving OLTP. Creating pools and groups needs `CONTROL SERVER`.

## Build it
```sql
USE master;
CREATE RESOURCE POOL ReportingPool WITH (
  MAX_CPU_PERCENT = 40,        -- only applies when there is CPU contention
  CAP_CPU_PERCENT = 60,        -- hard cap (2012+); short spikes above it are possible
  MAX_MEMORY_PERCENT = 30,     -- query workspace memory
  MAX_IOPS_PER_VOLUME = 2000); -- 2014+; 0 means the pool is not IO-governed
CREATE WORKLOAD GROUP ReportingGroup WITH (
  REQUEST_MAX_MEMORY_GRANT_PERCENT = 10,
  MAX_DOP = 4,
  REQUEST_MAX_CPU_TIME_SEC = 600,    -- raises cpu_threshold_exceeded; aborts (error 10961) only with trace flag 2422 (2016 SP2 / 2017 CU3+)
  GROUP_MAX_REQUESTS = 20)
USING ReportingPool;
GO
CREATE FUNCTION dbo.rg_classifier() RETURNS sysname WITH SCHEMABINDING AS
BEGIN
  RETURN CASE
    WHEN APP_NAME() LIKE N'Report Server%' OR SUSER_SNAME() = N'CORP\svc-reports' THEN N'ReportingGroup'
    ELSE N'default' END;     -- the classifier must be in master and schema-bound
END;
GO
ALTER RESOURCE GOVERNOR WITH (CLASSIFIER_FUNCTION = dbo.rg_classifier);
ALTER RESOURCE GOVERNOR RECONFIGURE;
```

## Classifier rules
- Evaluated for **every new session**, even with connection pooling, after authentication and any logon triggers. Client connections can time out if it is slow,
  so keep it simple and avoid data access.
- Microsoft's examples use `HOST_NAME()`, `SUSER_SNAME()` and `APP_NAME()`. Application names are supplied by the client, so do not use them for security.
- A session keeps its group for its lifetime. NULL, `default`, a nonexistent group, or a failing function all give the `default` group. Only one classifier at a time;
  a change needs `ALTER RESOURCE GOVERNOR RECONFIGURE`, and the function cannot be altered or dropped until it is removed as classifier.
- The DAC is not subject to classification: if the configuration breaks logins, connect with the DAC (or start in single-user mode) and
  `ALTER RESOURCE GOVERNOR WITH (CLASSIFIER_FUNCTION = NULL); ALTER RESOURCE GOVERNOR RECONFIGURE;` or disable resource governor.

## Monitor
```sql
SELECT g.name, s.session_id, s.program_name, s.login_name
FROM sys.dm_exec_sessions s JOIN sys.dm_resource_governor_workload_groups g ON g.group_id = s.group_id
WHERE s.is_user_process = 1;

SELECT name, total_request_count, active_request_count, queued_request_count,
       total_cpu_usage_ms, total_cpu_limit_violation_count, max_request_grant_memory_kb
FROM sys.dm_resource_governor_workload_groups;
SELECT name, used_memory_kb, max_memory_kb, total_cpu_usage_ms, read_io_throttled_total
FROM sys.dm_resource_governor_resource_pools;   -- read_io_throttled_total is NULL unless the pool is IO-governed
```
Statistics run since the Database Engine started; `ALTER RESOURCE GOVERNOR RESET STATISTICS` zeroes them. These DMVs show the in-memory configuration;
use the `sys.resource_governor_*` catalog views for stored configuration. They need VIEW SERVER STATE (VIEW SERVER PERFORMANCE STATE on 2022+).

## Gotchas
- `MAX_CPU_PERCENT` only applies under CPU contention; use `CAP_CPU_PERCENT` for a hard limit. The sum of the MIN percentages across pools cannot exceed 100.
- `REQUEST_MAX_MEMORY_GRANT_PERCENT` (default 25, a percentage of the pool's `MAX_MEMORY_PERCENT`; fractional values from SQL Server 2019) limits one request's workspace memory.
  In user-defined groups an oversized request first loses DOP and then fails with error 8657; the `internal` and `default` groups let it take the memory it needs,
  so the setting is not a cap there. Values above about 70 risk memory-grant timeouts (error 8645).
- Effective MAXDOP: a query hint is honoured up to the group's `MAX_DOP`, and `MAX_DOP` overrides the server and database-scoped settings.
- `GROUP_MAX_REQUESTS` makes extra sessions wait rather than fail. SQL Server 2025 adds `GROUP_MAX_TEMPDB_DATA_MB`/`_PERCENT` (error 1138 when exceeded).

## Verify
Sessions land in the intended groups, and under a load test OLTP latency stays flat while reporting slows.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for CREATE RESOURCE POOL, CREATE WORKLOAD GROUP, Resource Governor Classifier Function and the two resource governor DMVs (2017-2025).
Confirmed: pool and group options and defaults, CAP versus MAX CPU, IOPS version gate, REQUEST_MAX_CPU_TIME_SEC and trace flag 2422, memory-grant percentage behaviour including the default-group exception, MAXDOP precedence, classifier requirements, DAC bypass, DMV columns and permissions. Corrected: the default-group memory cap claim and the CPU-time wording. Removed unconfirmed claims: Enterprise-only, ORIGINAL_DB_NAME/IS_MEMBER suggestions, Perfmon objects and the internal-pool statement.
Method: documentation only; no commands were run.
