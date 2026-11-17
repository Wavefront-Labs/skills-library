---
id: computing-software.systems-network-administration.windows-server.rds-session-based-deployment
name: rds-session-based-deployment
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, remote-desktop-services, rds, rd-session-host, rd-connection-broker, rd-web-access, new-rdsessiondeployment, session-collection]
level: practitioner
status: docs-checked
description: "Deploy session-based Remote Desktop Services: broker, session hosts, web access, New-RDSessionDeployment, collections, RemoteApp publishing and broker HA."
sources:
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/rds-deploy-infrastructure
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/rds-connection-broker-cluster
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/new-rdsessiondeployment
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/set-rdconnectionbrokerhighavailability
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/set-rdsessionhost
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDS session-based deployment

## Roles
| Role | Job |
|---|---|
| RD Connection Broker | load balancing, reconnection to existing sessions, deployment config DB |
| RD Session Host (RDSH) | runs user sessions and RemoteApps |
| RD Web Access | web feed and portal for RemoteApps/desktops |
| RD Gateway | access from outside the corporate network over an encrypted tunnel |
| RD Licensing | issues RDS CALs |

## Deploy
From a domain-joined management server (Server Manager also does "Quick Start" for labs):
```powershell
New-RDSessionDeployment -ConnectionBroker rdcb01.corp.example.com -WebAccessServer rdweb01.corp.example.com `
  -SessionHost rdsh01.corp.example.com,rdsh02.corp.example.com
New-RDSessionCollection -CollectionName Office -SessionHost rdsh01.corp.example.com,rdsh02.corp.example.com `
  -ConnectionBroker rdcb01.corp.example.com -CollectionDescription 'Office desktops'
Set-RDSessionCollectionConfiguration -CollectionName Office -UserGroup 'CORP\RDS-Office-Users' `
  -DisconnectedSessionLimitMin 120 -IdleSessionLimitMin 60 -ConnectionBroker rdcb01.corp.example.com
New-RDRemoteApp -CollectionName Office -DisplayName 'Excel' -FilePath "$env:ProgramFiles\Microsoft Office\root\Office16\EXCEL.EXE" -ConnectionBroker rdcb01.corp.example.com
```
- Install the same applications on every session host in the collection.
- Certificates: `Set-RDCertificate -Role` accepts RDRedirector, RDPublishing, RDWebAccess and RDGateway (see the RDS
  deployment certificates skill).

## Broker high availability
Needs a database (SQL Server in your environment or Azure SQL Database) and a DNS round-robin name that holds the broker
FQDNs (`-ClientAccessName`):
```powershell
Set-RDConnectionBrokerHighAvailability -ConnectionBroker rdcb01 -DatabaseConnectionString '<ODBC connection string>' `
  -ClientAccessName rdcb.corp.example.com
Add-RDServer -Server rdcb02 -Role RDS-CONNECTION-BROKER -ConnectionBroker rdcb01
```
Install on each broker the ODBC driver whose version matches the connection string for your database.

## Operate
- Drain a host: `Set-RDSessionHost -SessionHost rdsh01 -NewConnectionAllowed NotUntilReboot` (values: Yes, NotUntilReboot, No).
- List, log off and message users: `Get-RDUserSession`, `Invoke-RDUserLogoff`, `Send-RDUserMessage`.

## Verify
- [ ] `https://rdweb01/RDWeb` shows apps; users land on both hosts; reconnection returns
  users to their disconnected session.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed in the windows-powershell-docs reference: New-RDSessionDeployment (-ConnectionBroker, -SessionHost, -WebAccessServer), New-RDSessionCollection, Set-RDSessionCollectionConfiguration (-UserGroup, -DisconnectedSessionLimitMin, -IdleSessionLimitMin), New-RDRemoteApp, Set-RDSessionHost -NewConnectionAllowed values, Set-RDConnectionBrokerHighAvailability (-DatabaseConnectionString, -ClientAccessName as the DNS round-robin name), Add-RDServer roles and Set-RDCertificate roles; the deployment steps, the Azure SQL or local SQL Server database and the matching ODBC driver in the Connection Broker cluster article. Removed as unconfirmed: the install mode commands, the ODBC Driver 17 string, the dbcreator login requirement, and UDP in the gateway role description.

Method: documentation only; no commands were run.
