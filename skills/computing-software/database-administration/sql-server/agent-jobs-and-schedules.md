---
id: computing-software.database-administration.sql-server.agent-jobs-and-schedules
name: agent-jobs-and-schedules
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, sql-server-agent, agent-jobs, sp-add-job, job-schedules, job-history, proxy-accounts, availability-group-jobs]
level: practitioner
status: docs-checked
description: "Create, script and monitor SQL Server Agent jobs: steps, schedules, owners, proxies, retry and failure notifications, job history, and making jobs AG-aware."
sources:
  - https://learn.microsoft.com/en-us/sql/ssms/agent/create-a-job
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-add-job-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-add-schedule-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-add-jobstep-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-functions/sys-fn-hadr-is-primary-replica-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Server Agent jobs

**Goal:** scheduled maintenance and ETL run reliably, failures page someone, and
jobs survive availability-group failovers.

## Create in T-SQL (scriptable, source-controlled)
```sql
USE msdb;
EXEC sp_add_job @job_name = N'Purge sessions', @owner_login_name = N'sa', @enabled = 1,
     @notify_level_email = 2, @notify_email_operator_name = N'DBA Team';   -- 2 = on failure (0 never, 1 success, 3 always)
EXEC sp_add_jobstep @job_name = N'Purge sessions', @step_name = N'Delete expired',
     @subsystem = N'TSQL', @database_name = N'appdb',
     @command = N'DELETE TOP (5000) FROM dbo.sessions WHERE expires_at < SYSUTCDATETIME();',
     @retry_attempts = 3, @retry_interval = 5, @on_fail_action = 2;
EXEC sp_add_schedule @schedule_name = N'Every 15 min', @freq_type = 4, @freq_interval = 1,
     @freq_subday_type = 4, @freq_subday_interval = 15;
EXEC sp_attach_schedule @job_name = N'Purge sessions', @schedule_name = N'Every 15 min';
EXEC sp_add_jobserver @job_name = N'Purge sessions';      -- target local server; easy to forget
```
dbatools: `New-DbaAgentJob`, `Copy-DbaAgentJob` to sync to other replicas.

## Ownership and proxies
Owner should be a non-person login (e.g. `sa` disabled-but-existing, or a
service login) so jobs do not fail when an employee's AD account is disabled.
CmdExec/PowerShell steps run as the Agent service account unless you define a
**proxy** with a credential: least privilege for OS-level steps.

## Monitor
```sql
SELECT j.name, h.run_date, h.run_time, h.run_status, h.message
FROM msdb.dbo.sysjobhistory h JOIN msdb.dbo.sysjobs j ON j.job_id = h.job_id
WHERE h.step_id = 0 AND h.run_status <> 1 ORDER BY h.instance_id DESC;   -- failures
EXEC msdb.dbo.sp_help_jobactivity;  -- running now
```
History is row-limited: Agent removes the oldest rows once the total limit or the per-job limit is reached. Check the limits on the History page of SQL Server Agent properties (or `msdb.dbo.sp_set_sqlagent_properties`; on Linux use `mssql-conf`) and raise them so history does not vanish before you look.

## Availability groups
Jobs live in msdb per instance, not in the AG. Create them on every replica and
make step 1 a guard:
```sql
IF sys.fn_hadr_is_primary_replica(N'appdb') <> 1 RETURN;  -- or RAISERROR to stop quietly
```
The function returns 1 on the primary, 0 on a secondary and NULL when the database is not in an AG (so `<> 1` does not stop the step in that case).

## Gotchas
- Agent not running (Express edition has no Agent through SQL Server 2022; Linux containers need `-e MSSQL_AGENT_ENABLED=true`, and Agent is disabled by default on Linux).
- Job steps default to `master` if `@database_name` is omitted.

## Verify
Job appears with `enabled=1` and next run date (`sp_help_jobschedule`), a forced
failure sends the operator email.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: sp_add_job (notify_level_email values, owner sysadmin-only, sp_add_jobserver sets target instance), sp_add_jobstep (database_name defaults to master, on_fail_action 2 is the default quit-with-failure, retry_interval in minutes, TSQL default subsystem), sp_add_schedule (freq_type 4 daily, freq_interval = every n days, freq_subday_type 4 = minutes, minimum 10 seconds), sysjobhistory run_status and step_id 0, sp_help_jobschedule, SQL Server 2022 editions table (Agent not in Express), SQL Server on Linux environment variable page (MSSQL_AGENT_ENABLED, Agent disabled by default). Removed as unconfirmed: the history defaults of 1000 total and 100 per job rows (documented only for Azure SQL Managed Instance and Linux) and the claim that overlapping runs are skipped.
Method: documentation only; no commands were run.
