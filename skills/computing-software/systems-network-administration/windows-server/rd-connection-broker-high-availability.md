---
id: computing-software.systems-network-administration.windows-server.rd-connection-broker-high-availability
name: rd-connection-broker-high-availability
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, rds, rd-connection-broker-ha, sql-server, remote-desktop-services, load-balancing]
level: advanced
status: docs-checked
description: "Make the RD Connection Broker highly available: SQL Server or Azure SQL database, DNS round robin name, adding the second broker and certificate updates."
sources:
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/rds-connection-broker-cluster
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/set-rdconnectionbrokerhighavailability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RD Connection Broker high availability

A single Connection Broker is a single point of failure for the whole RDS deployment. HA mode moves its database to
SQL and lets additional brokers share the deployment.

## Prerequisites
- SQL Server or Azure SQL Database reachable from the brokers.
- The SQL ODBC driver installed on each broker.
- A DNS round-robin name for the broker cluster (for example `rdcb.ad.example.com`) holding each broker's address.

## Configure
```powershell
Set-RDConnectionBrokerHighAvailability -ConnectionBroker rdcb01.ad.example.com `
  -DatabaseConnectionString 'DRIVER=ODBC Driver 17 for SQL Server;SERVER=sql01.ad.example.com;Trusted_Connection=Yes;APP=Remote Desktop Services Connection Broker;DATABASE=RDCB' `
  -ClientAccessName rdcb.ad.example.com
Get-RDConnectionBrokerHighAvailability -ConnectionBroker rdcb01.ad.example.com
```

## Verify
- [ ] Stopping one broker's service still lets users connect and reconnect to existing sessions.

## Checked
2026-10-28: Confirmed on Learn pages rds-connection-broker-cluster and set-rdconnectionbrokerhighavailability: Set-RDConnectionBrokerHighAvailability with -DatabaseConnectionString and -ClientAccessName (DNS round-robin name), Get-RDConnectionBrokerHighAvailability, SQL Server or Azure SQL Database, connection string format with Trusted_Connection and APP=. Removed: SQL version and dbcreator claims, ODBC 17 version, Add-RDServer example, Server Manager path, certificate and RDP file notes, gotchas about APP=, group membership and managed identities, active-active wording.
Method: documentation only; no commands were run.
