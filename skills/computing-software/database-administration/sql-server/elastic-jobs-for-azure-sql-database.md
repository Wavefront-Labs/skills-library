---
id: computing-software.database-administration.sql-server.elastic-jobs-for-azure-sql-database
name: elastic-jobs-for-azure-sql-database
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, azure-sql, azure-sql-database, elastic-jobs, job-agent, target-group, sql-server-agent-alternative, managed-identity, scheduled-tsql, multi-tenant]
level: practitioner
status: docs-checked
description: "Schedule T-SQL across Azure SQL databases with an elastic job agent: job database, target groups, managed identity auth, idempotent steps and history."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/elastic-jobs-overview
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/elastic-jobs-tsql-create-manage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elastic jobs for Azure SQL Database

**Goal:** the SQL Server Agent equivalent for Azure SQL Database (which has no Agent):
run maintenance or schema changes on a schedule across many databases.
(Managed Instance has real SQL Server Agent; use that there.)

## Components
- **Job database**: an Azure SQL Database (recommended service objective DTU S1 or higher) holding job
  definitions, history and the `jobs` schema stored procedures.
- **Elastic job agent**: Azure resource bound to the job database (portal, PowerShell or the REST API).
- **Target group**: servers, elastic pools or individual databases, with include/exclude
  members. Server and pool targets are evaluated at run time, so new databases are
  picked up automatically.

## Authentication
Recommended: a **user-assigned managed identity** on the job agent; create a
contained user for it in each target database (and `master` for server/pool
enumeration):
```sql
CREATE USER [job-agent-umi] FROM EXTERNAL PROVIDER;
GRANT ALTER ON SCHEMA::dbo TO [job-agent-umi];   -- grant only what the steps need
```
Older setups use database-scoped credentials (`job credential` + `master credential`
for refreshing the target list) with matching SQL logins on targets.

## Define a job (run in the job database)
```sql
EXEC jobs.sp_add_target_group @target_group_name = 'AllTenants';
EXEC jobs.sp_add_target_group_member @target_group_name = 'AllTenants',
     @target_type = 'SqlServer', @server_name = 'tenants-srv.database.windows.net';
EXEC jobs.sp_add_target_group_member @target_group_name = 'AllTenants',
     @membership_type = 'Exclude', @target_type = 'SqlDatabase',
     @server_name = 'tenants-srv.database.windows.net', @database_name = 'jobdb';

EXEC jobs.sp_add_job @job_name = 'IndexMaint', @description = 'Nightly stats/index',
     @schedule_interval_type = 'Days', @schedule_interval_count = 1,
     @schedule_start_time = '<FUTURE_UTC_START>';
EXEC jobs.sp_add_jobstep @job_name = 'IndexMaint', @step_name = 'stats',
     @command = N'EXEC dbo.IndexOptimize @Databases = ''CURRENT_DATABASE'', @UpdateStatistics = ''ALL'';',
     @target_group_name = 'AllTenants',
     @retry_attempts = 3, @step_timeout_seconds = 3600;
EXEC jobs.sp_update_job @job_name = 'IndexMaint', @enabled = 1;
EXEC jobs.sp_start_job 'IndexMaint';                 -- ad hoc run
```

## Monitor
```sql
SELECT * FROM jobs.job_executions;   -- filter on the columns you need
```
Steps can write results to an output table (`@output_type = 'SqlDatabase'`,
`@output_database_name`, `@output_table_name`) for cross-tenant reporting.

## Gotchas
- Scripts must be idempotent: a step is retried after transient failures, so it may run more than once
  (for example `IF NOT EXISTS ... CREATE`).
- The agent tier limits concurrent targets (default JA100 = 100; JA200, JA400, JA800 above it); use `@max_parallelism` on a step to limit concurrent databases against an elastic pool.
- Times are UTC. Create schedules that start in the future: a schedule with a past start time runs immediately when enabled.

## Verify
- [ ] Managed identity user exists in every target (and master for server targets).
- [ ] A test run succeeded on all targets; failures alert (Azure Monitor on job metrics).
- [ ] Steps are idempotent.

## Checked

2026-10-28. Confirmed in the Learn elastic jobs overview and T-SQL pages: UMI is the recommended authentication, contained user FROM EXTERNAL PROVIDER, DTU S1 or higher recommended for the job database, JA100/JA200/JA400/JA800 tiers, @max_parallelism on sp_add_jobstep, idempotent scripts, past start times run immediately, jobs.job_executions, @membership_type 'Exclude', @output_database_name. Removed: GA 2024, az elastic-job-agent command and New-AzSqlElasticJobAgent name, db_owner grant, lifecycle value list and unconfirmed column names, firewall bullet, past schedule date.

Method: documentation only; no commands were run.
