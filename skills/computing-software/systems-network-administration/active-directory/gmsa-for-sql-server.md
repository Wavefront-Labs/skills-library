---
id: computing-software.systems-network-administration.active-directory.gmsa-for-sql-server
name: gmsa-for-sql-server
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, gmsa, gmsa-sql-server, sql-server, kerberos]
level: advanced
status: docs-checked
description: "Run SQL Server engine and Agent under gMSAs: create and grant hosts, install with the account, SPNs, and AlwaysOn and FCI considerations."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/configure-windows-service-accounts-and-permissions
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/group-managed-service-accounts-overview
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/register-a-service-principal-name-for-kerberos-connections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gMSA for SQL Server

gMSAs remove the "SQL service account password in a spreadsheet" problem: Windows manages the password and the host retrieves it from a domain controller.

## Create
```powershell
New-ADGroup SQL-Prod-Hosts -GroupScope Global -Path "OU=Groups,DC=corp,DC=example,DC=com"
Add-ADGroupMember SQL-Prod-Hosts -Members SQL01$,SQL02$
New-ADServiceAccount gmsa-sqlprod -DNSHostName gmsa-sqlprod.corp.example.com `
  -PrincipalsAllowedToRetrieveManagedPassword SQL-Prod-Hosts -KerberosEncryptionType AES128,AES256
New-ADServiceAccount gmsa-sqlagt -DNSHostName gmsa-sqlagt.corp.example.com -PrincipalsAllowedToRetrieveManagedPassword SQL-Prod-Hosts
```
A host picks up new group membership in new Kerberos tickets (restart the host, or purge the machine ticket cache with `klist purge -li 0x3e7`), then on each host:
```powershell
Install-ADServiceAccount gmsa-sqlprod; Test-ADServiceAccount gmsa-sqlprod   # must be True
```

## Use it
- Setup or SQL Server Configuration Manager: account `CORP\gmsa-sqlprod$`, **password blank**.
- Create the gMSA in Active Directory before SQL Server setup; setup cannot create it.

## SPNs
To register SPNs manually, use setspn (the SQL Server SPN article also describes granting "Validated write to service principal name" so the service can register its own SPNs):
```cmd
setspn -S MSSQLSvc/sql01.corp.example.com:1433 CORP\gmsa-sqlprod$
setspn -S MSSQLSvc/sql01.corp.example.com CORP\gmsa-sqlprod$
```
For Always On listeners see the SPN guidance in the SQL Server availability group documentation.

## Supported topologies
- Standalone instances: SQL Server 2014 and later on Windows Server 2012 R2 or later.
- Failover cluster instances and availability groups: SQL Server 2016 and later.
- Analysis Services failover clusters: managed accounts and virtual accounts are not supported; use a domain account.
- Windows failover clusters themselves do not support gMSAs; services running on the cluster can use one.

## Verify
- [ ] `sys.dm_server_services` shows the gMSA; `SELECT auth_scheme FROM sys.dm_exec_connections WHERE session_id=@@SPID` returns KERBEROS from a remote client.
- [ ] `setspn -L CORP\gmsa-sqlprod$` lists all SPNs, no duplicates (`setspn -X`).

## Checked
Checked 2026-10-27 against Microsoft Learn (Windows Server gMSA overview and manage articles, 07/2025; SQL Server service accounts article; SQL Server SPN registration article; setspn and klist references).
- Confirmed: New-ADServiceAccount parameters -DNSHostName, -PrincipalsAllowedToRetrieveManagedPassword and -KerberosEncryptionType (accepted values include AES128 and AES256); Install-ADServiceAccount and Test-ADServiceAccount; KDS root key and domain/forest functional level 2012 prerequisites.
- Confirmed: SQL Server gMSA support starts at 2014 for standalone instances and 2016 for failover cluster instances and availability groups; Windows Server 2012 R2 or later; setspn -S, -L, -X; sys.dm_exec_connections auth_scheme returns KERBEROS; sys.dm_server_services reports the service_account column.
- Removed: the 30-day rotation figure and the services.msc prohibition, which no source confirmed.

Method: documentation only; no commands were run.
