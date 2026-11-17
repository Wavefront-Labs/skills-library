---
id: computing-software.database-administration.sql-server.network-configuration-tcp-ports-and-sql-browser
name: network-configuration-tcp-ports-and-sql-browser
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, sql-server-configuration-manager, tcp-port-1433, sql-browser, named-instance, static-port, spn, firewall]
level: practitioner
status: docs-checked
description: "Configure SQL Server network protocols: static TCP ports for named instances, SQL Browser, firewall rules, SPNs for Kerberos, and connection troubleshooting."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/configure-a-server-to-listen-on-a-specific-tcp-port
  - https://learn.microsoft.com/en-us/sql/tools/configuration-manager/sql-server-browser-service
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/register-a-service-principal-name-for-kerberos-connections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network configuration: TCP ports and SQL Browser

## Defaults
- Default instance: TCP 1433. Named instances: a **dynamic** port chosen at startup; clients
  find it by asking SQL Browser on **UDP 1434**.
- Named instances select an available port when the service starts, so the port can change; pin a static port for every named instance that sits behind a firewall.

## Set a static port
SQL Server Configuration Manager -> SQL Server Network Configuration -> Protocols for
`<INSTANCE>` -> TCP/IP -> IP Addresses tab -> **IPAll**: clear `TCP Dynamic Ports` (delete the 0) and set
`TCP Port` (e.g. 50001). Restart the service. If Listen All is Yes, only the IPAll values are used.
Check the connection:
```sql
SELECT local_tcp_port, net_transport, auth_scheme FROM sys.dm_exec_connections WHERE session_id = @@SPID;
```

## Firewall
Behind a firewall, open the TCP port the instance uses and, for named-instance lookups through SQL Browser, UDP 1434. With static ports clients can connect as `sql01,50001` without SQL Browser. See the Windows Firewall page in the SQL Server documentation for the rules.

## Kerberos SPNs
If a Kerberos security token cannot be obtained (for example no SPN is registered), authentication uses NTLM; `auth_scheme` in `sys.dm_exec_connections` shows which one is used.
```
setspn -S MSSQLSvc/sql01.corp.example.com:50001 CORP\svc-sql
```

## Troubleshooting order
1. `Test-NetConnection sql01 -Port 50001` (network and firewall).
2. Is the TCP protocol enabled for the instance?
3. Named instance via Browser: Browser service running and UDP 1434 open?

## Verify
- [ ] Each instance has a documented fixed port; firewall rules match.
- [ ] `auth_scheme` = KERBEROS for remote Windows logins.

## Checked

2026-10-28. Confirmed against Microsoft Learn (configure a server to listen on a specific TCP port, SQL Server Browser service, register an SPN for Kerberos connections): default instance on TCP 1433, named instances use dynamic ports chosen at startup, SQL Browser claims UDP 1434, IPAll and TCP Dynamic Ports steps, Listen All behaviour, setspn -S MSSQLSvc form, NTLM fallback, auth_scheme in sys.dm_exec_connections. Removed unconfirmed: dbatools and NetFirewall commands, xp_readerrorlog, setspn -X and -L, Express/Developer default, error 18456 note, forced tcp: prefix, attack-surface remark.

Method: documentation only; no commands were run.
