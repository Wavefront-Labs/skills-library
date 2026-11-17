---
id: computing-software.database-administration.sql-server.agent-proxies-and-credentials
name: agent-proxies-and-credentials
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, sql-server-agent, agent-proxy, sql-credential, cmdexec, powershell-job-step, least-privilege]
level: practitioner
status: docs-checked
description: "Run SQL Server Agent CmdExec, PowerShell and SSIS job steps under least-privilege Windows accounts using credentials and Agent proxies instead of the service account."
sources:
  - https://learn.microsoft.com/en-us/ssms/agent/create-a-sql-server-agent-proxy
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-credential
  - https://learn.microsoft.com/en-us/ssms/agent/sql-server-agent-subsystems
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-grant-proxy-to-subsystem-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-grant-login-to-proxy-transact-sql
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/create-credential-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Agent proxies and credentials

T-SQL job steps run in the job owner's security context. **Non-T-SQL subsystems** (CmdExec, PowerShell, SSIS, Replication, Analysis Services)
run as the **Agent service account** (which must be a sysadmin) unless a proxy is used. Giving the service account file
share or network rights for one job grants them to every job.

## 1. Credential: stores a Windows identity
```sql
CREATE CREDENTIAL cred_etl_share
  WITH IDENTITY = N'CORP\svc-etl-files', SECRET = N'<password>';
```
When IDENTITY is a Windows user, the secret is its password, stored encrypted with the service master key. Use a dedicated least-privilege domain account and rotate the password with `ALTER CREDENTIAL`. The user in the credential needs the **Access this computer from the network** right (`SeNetworkLogonRight`) on the SQL Server host.

## 2. Proxy: links the credential to subsystems and principals
```sql
EXEC msdb.dbo.sp_add_proxy @proxy_name = N'proxy_etl_files',
     @credential_name = N'cred_etl_share', @enabled = 1;
EXEC msdb.dbo.sp_grant_proxy_to_subsystem @proxy_name = N'proxy_etl_files', @subsystem_name = N'CmdExec';
EXEC msdb.dbo.sp_grant_proxy_to_subsystem @proxy_name = N'proxy_etl_files', @subsystem_name = N'PowerShell';
EXEC msdb.dbo.sp_grant_login_to_proxy @proxy_name = N'proxy_etl_files', @login_name = N'CORP\etl-operators';
```
Subsystem names for `sp_grant_proxy_to_subsystem`: `CmdExec`, `PowerShell`, `Dts` (SSIS package execution; the job step's `@subsystem` is `SSIS`), `ANALYSISQUERY`, `ANALYSISCOMMAND`,
`Snapshot`, `LogReader`, `Distribution`, `Merge`, `QueueReader` (and the deprecated `ActiveScripting`). Granting a proxy to a subsystem does not change the underlying account's permissions.

## 3. Use it in the job step
```sql
EXEC msdb.dbo.sp_add_jobstep @job_name = N'Nightly file import', @step_name = N'Copy files',
     @subsystem = N'CmdExec',
     @command = N'robocopy \\files\incoming \\files\staging *.csv /MOV',
     @proxy_name = N'proxy_etl_files';
```
SSMS: job step > "Run as" dropdown.

## Non-sysadmin job owners
Only sysadmin members can create, modify or delete proxies. Other users need one of the msdb roles `SQLAgentUserRole`, `SQLAgentReaderRole` or `SQLAgentOperatorRole`
plus access to the proxy (`sp_grant_login_to_proxy` accepts a login, a fixed server role or an msdb role).

## Gotchas
- When the Windows account's password changes, run `ALTER CREDENTIAL ... WITH IDENTITY = ..., SECRET = ...`
  or steps using the proxy fail to log on.
- Creating a proxy does not grant the account anything; if it cannot connect to SQL Server, steps that connect will fail.
- Credential secrets are encrypted with the service master key; moving them to another
  server means re-entering the secrets (or restoring the SMK).
- `xp_cmdshell` is a different mechanism with its own proxy credential; keep it disabled.

## Verify
Run the job and read the step message in `msdb.dbo.sysjobhistory` (it records the account the step ran as); `EXEC msdb.dbo.sp_help_proxy;` lists the proxies.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: create-a-sql-server-agent-proxy page (credential must exist first, SeNetworkLogonRight, sysadmin-only proxy management, msdb roles), sp_grant_proxy_to_subsystem (subsystem names including Dts, proxy grants do not change principal permissions), sp_grant_login_to_proxy (login, fixed server role or msdb role), sp_add_jobstep (default service-account context, proxy_name), CREATE CREDENTIAL (secret is the Windows password, encrypted by the service master key). Wrong in the draft: SSIS subsystem name for the grant is Dts, T-SQL steps run as the job owner (not the Agent account), and the dead subsystems link was replaced. Removed as unconfirmed: the exact CmdExec denial message, error numbers 1326/1385, the batch-logon claim (the proxy page names the network logon right), the gMSA statement, the xp_cmdshell proxy account literal and the exact history message text.
Method: documentation only; no commands were run.
