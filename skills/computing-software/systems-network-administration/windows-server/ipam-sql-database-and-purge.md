---
id: computing-software.systems-network-administration.windows-server.ipam-sql-database-and-purge
name: ipam-sql-database-and-purge
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ipam, ipam-sql-database, move-ipamdatabase, data-purge, sql-server]
level: advanced
status: docs-checked
description: "Move the IPAM database from WID to SQL Server with Move-IpamDatabase, size it, and purge old utilisation and audit data to keep IPAM fast."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/move-ipamdatabase
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/set-ipamdatabase
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/remove-ipamutilizationdata
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/remove-ipamipaddressauditevent
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/update-ipamserver
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/ipam/purge-utilization-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPAM database on SQL Server and data purge

IPAM can use Windows Internal Database (WID) or SQL Server; `Move-IpamDatabase` migrates it to SQL Server.

## Move to SQL Server
1. A SQL Server instance reachable from the IPAM server. Isolate the IPAM server and shut down IPAM clients before migrating.
2. If you connect with the IPAM server's computer account, that account needs permission to create and write to the database. Pre-create the database with the same collation as the source (from WID use `SQL_LATIN1_GENERAL_CP1_CI_AS`); otherwise SQL Server's default collation is used and errors can follow.
3. Move:
```powershell
Move-IpamDatabase -DatabaseServer sql01.ad.example.com -DatabaseName IPAM -DatabaseAuthType Windows -DatabasePort 1433
Get-IpamDatabase
```
The cmdlet creates a new IPAM schema, copies all data and then points IPAM at the new database; if it fails it returns an error and leaves the current settings unchanged. When migrating from WID it renames the old data and log files with a time stamp. It can also migrate from one SQL Server database to another. `Set-IpamDatabase` changes the connection settings (server, name, port, authentication); the documentation recommends the default port 1433.

## Purge
IPAM keeps address utilisation history and audit (configuration and IP address tracking) data.
- Utilisation data: in Server Manager > IPAM open IP Address Blocks, IP Address Inventory or IP Address Range Groups, then TASKS > **Purge Utilization Data**, choose a date; all records on or before it are deleted. You must be in IPAM Administrators or local Administrators. PowerShell: `Remove-IpamUtilizationData -EndDate '<DATE>'`.
- Audit data: `Remove-IpamIpAddressAuditEvent -EndDate`, `Remove-IpamConfigurationEvent` and `Remove-IpamDhcpConfigurationEvent`.

## After an OS upgrade
`Update-IpamServer` applies IPAM schema updates (it validates the existing database first and logs to `%SystemDrive%\Windows\System32\IPAM\logs`) and keeps customised task schedules.

## Verify
- [ ] `Get-IpamDatabase` shows the SQL Server; IPAM data collection tasks complete without errors.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs (IPAM articles) and windows-powershell-docs (Windows Server 2025 IpamServer module) repositories, latest commit 2026-10-23. Confirmed: Move-IpamDatabase behaviour (migrates from WID or SQL Server to SQL Server, new schema and data copy, unchanged settings on failure, WID file rename, collation SQL_LATIN1_GENERAL_CP1_CI_AS, isolate server and stop clients) and parameters (`-DatabaseServer`, `-DatabaseName`, `-DatabaseAuthType`, `-DatabasePort`); Set-IpamDatabase and default port 1433; Purge Utilization Data procedure and required membership; Remove-IpamUtilizationData, Remove-IpamIpAddressAuditEvent, Remove-IpamConfigurationEvent and Remove-IpamDhcpConfigurationEvent cmdlets; Update-IpamServer behaviour. Corrected the claim that no purge cmdlet exists and the dbcreator/db_owner login advice; removed the not-supported-back-to-WID statement, the growth figure, recovery-model advice and task names, which the checked pages do not state.

Method: documentation only; no commands were run.
