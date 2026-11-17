---
id: computing-software.cloud-infrastructure-engineering.azure.azure-sql-elastic-jobs
name: azure-sql-elastic-jobs
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-sql, elastic-jobs, job-agent, target-groups, database-maintenance]
level: advanced
status: docs-checked
description: "Run T-SQL across many Azure SQL databases on a schedule with elastic jobs: job agent, managed identity auth, target groups, steps, retries and output."
sources: ["https://learn.microsoft.com/azure/azure-sql/database/elastic-jobs-overview", "https://learn.microsoft.com/azure/azure-sql/database/elastic-jobs-tsql-create-manage", "https://learn.microsoft.com/azure/azure-sql/database/elastic-jobs-tutorial"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure SQL elastic jobs

**Goal:** schedule maintenance or schema changes across a fleet of Azure SQL databases (SQL Agent does not exist in SQL Database).

## Components
- **Job database**: an Azure SQL Database (S1+ recommended) storing job definitions and history.
- **Elastic job agent**: Azure resource pointing at the job database.
- **Target groups**: servers, elastic pools, individual databases, with include/exclude members; evaluated at run time, so new databases in a server are picked up.
- **Jobs and steps**: T-SQL commands.

## Auth (preferred: managed identity)
1. Assign a **user-assigned managed identity** to the job agent.
2. Create a contained user for it in every target database:
```sql
CREATE USER [jobagent-umi] FROM EXTERNAL PROVIDER;
-- grant only the permissions the job steps need
```
Database-scoped credentials are the older alternative.

## Define a job (T-SQL in the job database)
```sql
EXEC jobs.sp_add_target_group 'AllProd';
EXEC jobs.sp_add_target_group_member 'AllProd', @target_type='SqlServer', @server_name='sqlprod1.database.windows.net';
EXEC jobs.sp_add_job @job_name='IndexMaint', @description='Index maintenance';
EXEC jobs.sp_add_jobstep @job_name='IndexMaint', @step_name='Run', @target_group_name='AllProd',
     @command=N'EXEC dbo.IndexOptimize @Databases=''USER_DATABASES''';
EXEC jobs.sp_start_job 'IndexMaint';
SELECT * FROM jobs.job_executions WHERE job_name='IndexMaint' ORDER BY start_time DESC;
```
Collect results into a table with `@output_type='SqlDatabase'`, `@output_server_name`, `@output_database_name`, `@output_table_name`.

## Gotchas
- Steps must be **idempotent**: a script can run more than once and must give the same result.
- Parallelism: `@max_parallelism` on the step to limit load on pools.
- Private connectivity: an elastic jobs service-managed private endpoint can connect the job agent to target and output servers.
- Job agents default to JA100 (up to 100 concurrent job executions); change the service level if the fleet needs more.

## Verify
- [ ] `jobs.job_executions` shows the outcome per target; output table populated.

## Checked
2026-10-28. Confirmed on the elastic jobs overview and T-SQL pages: job database DTU S1 or higher recommended, user-assigned managed identity recommended, dynamic target groups (unlike SQL Agent), `jobs.sp_add_target_group`, `sp_add_jobstep`, `sp_start_job`, `jobs.job_executions`, `@output_type = 'SqlDatabase'`, `@max_parallelism`, idempotent scripts, service-managed private endpoints, JA100 default.
Removed (not confirmed): retry and timeout parameters, `sp_update_job`, the Days schedule values, db_owner grant, at-least-once wording, Azure services firewall advice, `Succeeded` status value.

Method: documentation only; no commands were run.
