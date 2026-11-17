---
id: computing-software.database-administration.sql-server.environment-validation-with-dbachecks
name: environment-validation-with-dbachecks
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, dbachecks, pester, dbatools, health-check, compliance, powershell]
level: practitioner
status: docs-checked
description: "Validate SQL Server estates against standards with dbachecks: run Pester-based checks, set server lists with Set-DbcConfig, and report via Power BI or mail."
sources:
  - https://github.com/dataplat/dbachecks
  - https://dbachecks.readthedocs.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment validation with dbachecks

dbachecks is an open-source PowerShell module that crowd-sources SQL Server validation checklists as Pester tests (backups are being performed, integrity checks run and no corruption, disk space, enabled jobs succeeding, backup path access, identity columns not about to max out).

## Requirements
- PowerShell 5+. Install from the PowerShell Gallery, which auto-installs `dbatools` and `PSFramework`.
- Install **Pester 4.10.0** yourself: the README says dbachecks is inconsistent with Pester v5, so remove v5 or force-import 4.10.0.
```powershell
Install-Module Pester -SkipPublisherCheck -Force -RequiredVersion 4.10.0
Import-Module Pester -Force -RequiredVersion 4.10.0
```
- It gathers data through dbatools, supporting SQL 2000 to vNext including Linux instances; Windows-API checks (services, disk space) do not work against Linux. It does not install on PowerShell Core.
- The README notes v2 development has stopped in favour of a v3 on Pester v5.

## Run
`Invoke-DbcCheck` wraps `Invoke-Pester`; a "Check" is a Pester tag. List checks with `Get-DbcCheck` (tags with `Get-DbcTagCollection`).
```powershell
Invoke-DbcCheck -SqlInstance $servers -Checks SuspectPage, LastBackup
Invoke-DbcCheck -Check Backup -SqlInstance sql2016
Invoke-DbcCheck -Check Storage -ComputerName server1, server2
Invoke-DbcCheck -Check Database -ExcludeCheck Backup -SqlInstance sql2016
```
`-SqlInstance` is for SQL checks, `-ComputerName` for Windows-server checks. `-ExcludeCheck` always takes precedence over `-Check`.

## Configure
```powershell
Set-DbcConfig -Name app.sqlinstance -Value sql2016, sql2017
Set-DbcConfig -Name app.computername -Value sql2016, sql2017
Get-DbcConfig
Get-DbcConfig *skip*
Set-DbcConfig -Name skip.dbcc.datapuritycheck -Value $true
Set-DbcConfig -Name app.sqlcredential -Value (Get-Credential sa)
```
`Set-DbcConfig` persists values. `app.sqlcredential` sets the SqlCredential for the whole module, not your console session.

## Report
- Power BI: pipe the result to `Update-DbcPowerBiDataSource` (optionally `-Environment`), then `Start-DbcPowerBi` and refresh the report.
```powershell
Invoke-DbcCheck -SqlInstance sql2017 -Checks SuspectPage, LastBackup -Show Summary -PassThru | Update-DbcPowerBiDataSource
Start-DbcPowerBi
```
- Mail: `Invoke-DbcCheck ... -OutputFormat NUnitXml -PassThru` then `Send-DbcMailMessage -To ... -From ... -SmtpServer ...`.

## Custom checks and Agent
- Add your own repository of Pester checks by appending to `app.checkrepos`: `Set-DbcConfig -Name app.checkrepos -Value <CHECKS_DIR> -Append`; they then run through `Invoke-DbcCheck`.
- In SQL Server Agent the README recommends a CmdExec step; if you use a PowerShell step, `Set-Location` outside `SQLSERVER:` first.
- Without Gallery access, `Save-Module -Name dbachecks, dbatools, PSFramework, Pester` on a connected machine and copy the modules into `$env:PSModulePath`.

## Gotchas
- Pester version: use 4.10.0 with the v2 module.
- A failing check means fix the server or change the config deliberately; do not silently exclude.

## Verify
`Invoke-DbcCheck` completes against your server list and failures are reviewed.

## Checked
2026-11-09. Read the GitHub README and the readthedocs home page (same content). Removed (not stated on those pages): the check group list, the `policy.*` threshold config names, `Export-DbcConfig`/`Import-DbcConfig`, `Convert-DbcResult`/`Write-DbcTable`, and the claim that v2 needs Pester 5 (the README says Pester 4.10.0).
Method: documentation only; no commands were run.
