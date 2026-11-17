---
id: computing-software.database-administration.sql-server.database-scoped-configuration
name: database-scoped-configuration
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, database-scoped-configuration, legacy-cardinality-estimation, maxdop, parameter-sniffing, clear-procedure-cache, compatibility-level, sql-server-configuration]
level: practitioner
status: docs-checked
description: "Use ALTER DATABASE SCOPED CONFIGURATION to set MAXDOP, legacy CE, sniffing and other per-database options, including separate values for AG secondaries."
sources:
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-scoped-configuration-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-database-scoped-configurations-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database scoped configuration

**Goal:** change optimizer and engine behaviour for one database (SQL Server 2017+ per the current reference, Azure SQL; individual options have their own version gates)
without instance-wide `sp_configure` or trace flags, and travel with the database
across AG failover and to Azure.

## Inspect
```sql
USE appdb;
SELECT name, value, value_for_secondary, is_value_default
FROM sys.database_scoped_configurations ORDER BY name;
```

## Common settings
```sql
ALTER DATABASE SCOPED CONFIGURATION SET MAXDOP = 4;                 -- overrides server MAXDOP
ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET MAXDOP = 8;   -- readable secondaries
ALTER DATABASE SCOPED CONFIGURATION SET LEGACY_CARDINALITY_ESTIMATION = ON; -- CE 70 without dropping compat level
ALTER DATABASE SCOPED CONFIGURATION SET PARAMETER_SNIFFING = OFF;   -- like OPTIMIZE FOR UNKNOWN everywhere; last resort
ALTER DATABASE SCOPED CONFIGURATION SET QUERY_OPTIMIZER_HOTFIXES = ON; -- TF 4199 per DB
ALTER DATABASE SCOPED CONFIGURATION SET OPTIMIZE_FOR_AD_HOC_WORKLOADS = ON; -- SQL Server 2019+, per-DB plan stubs
ALTER DATABASE SCOPED CONFIGURATION SET LAST_QUERY_PLAN_STATS = ON; -- 2019+, sys.dm_exec_query_plan_stats
ALTER DATABASE SCOPED CONFIGURATION SET ELEVATE_ONLINE = WHEN_SUPPORTED; -- 2019+, OFF | WHEN_SUPPORTED | FAIL_UNSUPPORTED, default OFF
ALTER DATABASE SCOPED CONFIGURATION SET ELEVATE_RESUMABLE = WHEN_SUPPORTED; -- 2019+, same values
ALTER DATABASE SCOPED CONFIGURATION SET IDENTITY_CACHE = OFF;      -- default ON; OFF avoids gaps after restart/failover, primary only
ALTER DATABASE SCOPED CONFIGURATION CLEAR PROCEDURE_CACHE;          -- flush only this DB's plans
```
Intelligent query processing features can be switched off individually
(`BATCH_MODE_ON_ROWSTORE = OFF`, `TSQL_SCALAR_UDF_INLINING = OFF`,
`PARAMETER_SENSITIVE_PLAN_OPTIMIZATION = OFF`; the first two are SQL Server 2019+, PSP is 2022+) when one regresses after a
compatibility level upgrade, keeping the rest.

## Precedence
For MAXDOP: a query hint overrides both `sp_configure` and the scoped setting, but the
Resource Governor workload group MAXDOP caps all of them (a hint of 0 is overridden by it).
A non-zero scoped MAXDOP overrides `sp_configure`.

## Upgrade pattern
Raise compatibility level to get new features, and if a CE regression appears set
`LEGACY_CARDINALITY_ESTIMATION = ON` (or per query `USE HINT('FORCE_LEGACY_CARDINALITY_ESTIMATION')`)
while you fix the queries with Query Store, instead of dropping compat level back.

## Gotchas
- Settings live in the database: restored copies and AG secondaries inherit them,
  which is the point, but surprises anyone diffing only server config.
- `PRIMARY` is valid only for secondaries (use whatever the primary has) and is the default there; all secondaries share one set of values, you cannot configure individual secondaries.
- `CLEAR PROCEDURE_CACHE` causes a compile storm for that DB; prefer evicting one
  plan: the statement accepts an optional plan handle, `CLEAR PROCEDURE_CACHE [plan_handle]`.

## Verify
- [ ] Non-default rows in `sys.database_scoped_configurations` are documented with a reason.
- [ ] Per-DB MAXDOP matches the workload; secondary value reviewed for reporting replicas.

## Checked
Date 2026-10-23. Documentation release: ALTER DATABASE SCOPED CONFIGURATION reference (SQL Server 2025 default view, 2017-2022 applies-to lines).
Confirmed: option names and value sets, `FOR SECONDARY` and `PRIMARY` semantics, `CLEAR PROCEDURE_CACHE [plan_handle]`, 2019+ gates for ad hoc, last plan stats, ELEVATE_*, batch mode on rowstore and scalar UDF inlining, 2022 gate for PSP, MAXDOP precedence rules.
Method: documentation only; no commands were run.
