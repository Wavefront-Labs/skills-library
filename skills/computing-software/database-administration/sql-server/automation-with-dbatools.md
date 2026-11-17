---
id: computing-software.database-administration.sql-server.automation-with-dbatools
name: automation-with-dbatools
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, dbatools, powershell, automation, sql-server-agent, migration, start-dbamigration, test-dbalastbackup, estate-inventory]
level: practitioner
status: docs-checked
description: "Automate SQL Server estate tasks with the dbatools PowerShell module: inventory, migrations, backup tests, config checks."
sources:
  - https://dbatools.io/commands/
  - https://github.com/dataplat/dbatools
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Automation with dbatools

**Goal:** do the same task on one or many instances with one tested command, instead of clicking through SSMS per server. dbatools is an open-source (MIT) PowerShell module.

## Install and connect
```powershell
Install-Module dbatools -Scope CurrentUser
$servers = Get-Content .\servers.txt               # or Get-DbaRegServer -SqlInstance <CMS_SERVER>
```
Recent SQL Server client libraries require encryption and certificate validation by default, which can break existing scripts against instances with self-signed certificates; the command reference describes `Set-DbatoolsInsecureConnection` for that case (it relaxes security, so prefer fixing the certificates).

## Command map (names confirmed on the command reference)
| Task | Command |
|---|---|
| Databases and space | `Get-DbaDatabase`, `Get-DbaDbSpace` (files, usage, free space, autogrowth) |
| Backup gaps | `Get-DbaLastBackup` (latest full, differential and log backup dates from msdb history) |
| Prove backups restore | `Test-DbaLastBackup` (restores the latest backups, as a new name, and runs DBCC CHECKDB) |
| Memory | `Test-DbaMaxMemory` (calculates recommended max memory) |
| MAXDOP | `Set-DbaMaxDop` (without a value, applies the recommended setting) |
| Orphaned users | `Repair-DbaDbOrphanUser` |
| Agent jobs | `Find-DbaAgentJob` (filters by name, step, status, schedule, notifications) |
| Error log | `Get-DbaErrorLog` (reads error log files 0-99; Windows only per the reference) |
| Maintenance | `Install-DbaMaintenanceSolution` (deploys Ola Hallengren's framework) |
| Live activity | `Install-DbaWhoIsActive` (installs Adam Machanic's sp_WhoIsActive) |
| Ad hoc T-SQL | `Invoke-DbaQuery` |

```powershell
Get-DbaLastBackup -SqlInstance $servers
Test-DbaLastBackup -SqlInstance <PROD_SERVER> -Destination <TEST_SERVER>
Test-DbaMaxMemory -SqlInstance $servers
```
Check each command's parameters with `Get-Help <command> -Full` before using; options are not listed on the summary page.

## Migrations
`Start-DbaMigration` consolidates most dbatools migration tools into one command for complete instance migrations. Piecemeal alternatives: `Copy-DbaLogin` (transfers logins, preserving authentication details and security context), `Copy-DbaAgentJob`, `Copy-DbaLinkedServer`, `Copy-DbaDatabase`. Preserving login SIDs avoids orphaned users after a database move.

## Gotchas
- Pin a module version on job servers and update deliberately after testing.
- Test migrations and scheduled scripts on non-production first.

## Verify
- [ ] Module installed for the account that runs scheduled scripts.
- [ ] A fleet check (last backups, max memory, failed jobs) runs and its output is reviewed.

## Checked
2026-11-09. Confirmed that every command named exists on the dbatools command reference and what each does (descriptions), plus install line, MIT licence and the encryption-default note from the GitHub README and commands page. Partial read: only list-level descriptions, not per-command parameter pages. Removed because the pages do not state them: all switch and parameter specifics (`-BackupRestore`, `-SharedPath`, `-IsFailed`, `-EnableException`, `-WhatIf`, `-InstallJobs`), Agent CmdExec job step advice, and the PowerShell version claim.
Method: documentation only; no commands were run.
