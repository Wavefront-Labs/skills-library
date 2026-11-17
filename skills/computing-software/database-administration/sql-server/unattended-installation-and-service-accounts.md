---
id: computing-software.database-administration.sql-server.unattended-installation-and-service-accounts
name: unattended-installation-and-service-accounts
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, configurationfile-ini, sql-service-accounts, unattended-install, gmsa, virtual-accounts, setup-exe, slipstream]
level: practitioner
status: docs-checked
description: "Install SQL Server unattended from ConfigurationFile.ini with the right service accounts (virtual accounts, gMSA), tempdb layout, collation, and post-install checks."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/install-windows/install-sql-server-using-a-configuration-file
  - https://learn.microsoft.com/en-us/sql/database-engine/install-windows/install-sql-server-from-the-command-prompt
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/configure-windows-service-accounts-and-permissions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unattended installation and service accounts

## Generate the file once
Run the GUI setup up to the "Ready to Install" page; the path of the generated `ConfigurationFile.ini` is shown there. Cancel, edit, reuse. Generate a new file for each SQL Server version.

## Key settings
```ini
[OPTIONS]
ACTION="Install"
FEATURES=SQLENGINE,FULLTEXT
INSTANCENAME="MSSQLSERVER"
SQLSVCACCOUNT="CORP\gmsa-sql01$"
AGTSVCACCOUNT="CORP\gmsa-sqlagt01$"
SQLSVCSTARTUPTYPE="Automatic"
AGTSVCSTARTUPTYPE="Automatic"
SQLCOLLATION="SQL_Latin1_General_CP1_CI_AS"
SQLSYSADMINACCOUNTS="CORP\SQL-DBAs"
SECURITYMODE="SQL"
SQLSVCINSTANTFILEINIT="True"
SQLUSERDBDIR="<DATA_DIR>"
SQLUSERDBLOGDIR="<LOG_DIR>"
SQLTEMPDBDIR="<TEMPDB_DIR>"
SQLTEMPDBFILECOUNT="8"            # default: 8 or the number of cores, whichever is lower (1 on Express)
SQLTEMPDBFILESIZE="<MB>"           # initial size of each tempdb data file; see the parameter reference for limits
SQLBACKUPDIR="<BACKUP_DIR>"
UPDATEENABLED="True"
UPDATESOURCE="<CU_SHARE>"
TCPENABLED="1"
IACCEPTSQLSERVERLICENSETERMS="True"
QUIET="True"
```
`SECURITYMODE="SQL"` enables SQL authentication and requires `/SAPWD`; without it only Windows authentication is supported. `UPDATESOURCE` is where Setup obtains product updates ("MU", a folder path or a UNC share).
Run: `setup.exe /ConfigurationFile=ConfigurationFile.ini /SAPWD="<SECRET>"` (keep secrets out of the file).
Read `Summary.txt` in the Setup Bootstrap log folder to confirm the result.

## Service accounts
| Option | When |
|---|---|
| Virtual account | standalone hosts; password can be omitted in setup |
| Managed service account (for example a gMSA, `CORP\name$`) | domain hosts; password can be omitted in setup |
| Domain user | you own password rotation |
Rules: use separate accounts for different SQL Server services and do not give the service account extra permissions; change the Database Engine or Agent account only in SQL Server Configuration Manager, which also updates the Windows permissions and per-service SID setup. "Lock pages in memory" is needed only when paging is turned off entirely.
Set `SQLSVCINSTANTFILEINIT="True"` to enable instant file initialization for the service account (default False).

## After install
Set max server memory, MAXDOP and cost threshold, model file sizes, backup compression default and error log count, then register SPNs for Kerberos.

## Verify
`SELECT servicename, service_account, instant_file_initialization_enabled FROM sys.dm_server_services;`

## Checked

2026-10-28. Confirmed against Microsoft Learn (install from the command prompt, install using a configuration file, service accounts and permissions): ConfigurationFile.ini path shown on the Ready to Install page, /SAPWD required with /SECURITYMODE=SQL, /SQLTEMPDBFILECOUNT default, /SQLSVCINSTANTFILEINIT default False, /UpdateSource values, /TCPENABLED, virtual and managed service accounts may omit passwords, separate accounts per service, change accounts in Configuration Manager, lock pages in memory only when paging is off, Summary.txt in the Setup Bootstrap log folder. Removed unconfirmed: 3010 exit code, SQLTEMPDBFILESIZE figure, gMSA PowerShell prerequisites, volume maintenance right name, dbatools command, NT SERVICE account name and default claim, Domain Admin remark.

Method: documentation only; no commands were run.
