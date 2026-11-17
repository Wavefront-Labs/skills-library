---
id: computing-software.database-administration.sql-server.ag-listeners-and-multisubnet-failover
name: ag-listeners-and-multisubnet-failover
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, ag-listener, multisubnetfailover, availability-groups, registerallprovidersip, hostrecordttl, azure-load-balancer, dnn-listener]
level: advanced
status: docs-checked
description: "Create SQL Server AG listeners for single and multi-subnet clusters, set RegisterAllProvidersIP and HostRecordTTL, and use DNN or a load balancer on Azure VMs."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/create-or-configure-an-availability-group-listener-sql-server
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/listeners-client-connectivity-application-failover
  - https://learn.microsoft.com/en-us/azure/azure-sql/virtual-machines/windows/availability-group-distributed-network-name-dnn-listener-configure
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-availability-group-transact-sql
  - https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-utility
  - https://learn.microsoft.com/en-us/azure/azure-sql/virtual-machines/windows/availability-group-vnn-azure-load-balancer-configure
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AG listeners and MultiSubnetFailover

## Create
```sql
ALTER AVAILABILITY GROUP [AG1]
ADD LISTENER N'ag1-listener' (
  WITH IP ((N'10.1.0.50', N'255.255.255.0'),     -- subnet of DC1 nodes
           (N'10.2.0.50', N'255.255.255.0')),    -- subnet of DC2 nodes
  PORT = 1433);
```
The cluster creates a client access point (network name + IP resources) in the AG role. Check the
Active Directory permissions the cluster name object needs (or pre-stage the listener computer
object) in the "Configure availability group listener" page before creating it. Do not use DHCP for a production listener.

## Multi-subnet behaviour
Only the IP for the subnet hosting the primary is online. A listener created with SSMS, T-SQL or PowerShell registers
**all** its IPs in DNS (`RegisterAllProvidersIP = 1`). Set `MultiSubnetFailover=True` in the connection string: the driver opens a TCP socket to every IP in parallel and uses the first to answer. Microsoft recommends it for single- and multi-subnet listeners and FCI names; it works only over TCP.
```
Server=tcp:ag1-listener,1433;Database=appdb;MultiSubnetFailover=True;
```
Legacy clients that cannot set it: register one IP and lower the TTL (default 1200 s = 20 min) instead. The changes apply only after the listener resource goes offline and online; cached DNS records keep the old TTL until they expire, and cross-subnet failover can then take 15 minutes or more depending on TTL and DNS/AD replication:
```powershell
Get-ClusterResource "AG1_ag1-listener" | Set-ClusterParameter RegisterAllProvidersIP 0
Get-ClusterResource "AG1_ag1-listener" | Set-ClusterParameter HostRecordTTL 300
Stop-ClusterResource "AG1_ag1-listener"; Start-ClusterResource "AG1_ag1-listener"
```
Clients then reconnect only after DNS updates and the TTL expires (minutes).

## Azure VMs
A classic (VNN) listener on SQL Server on Azure VMs needs an **Azure Load Balancer** (see the Azure VNN load balancer article). Alternatives that need no load balancer:
- Put each replica in its own subnet of the same virtual network (multi-subnet AG).
- Or a **DNN listener** (distributed network name): create it with `Add-ClusterResource -Name <port> -ResourceType "Distributed Network Name" -Group <ag>`, set its `DnsName`, start it and add it to the AG resource dependency (Microsoft ships a script on the DNN page). Requires SQL Server 2019 CU8+, 2017 CU25+ or 2016 SP3+ on Windows Server 2016+, a unique port (never 1433) and clients that set `MultiSubnetFailover=True`. `sys.availability_group_listeners.is_distributed_network_name = 1` marks a DNN listener.

## Check
```sql
SELECT l.dns_name, l.port, ip.ip_address, ip.state_desc
FROM sys.availability_group_listeners l
JOIN sys.availability_group_listener_ip_addresses ip ON ip.listener_id = l.listener_id;
```
Test: `Test-NetConnection ag1-listener -Port 1433` from the app tier, and `sqlcmd -S tcp:ag1-listener -M -Q "SELECT @@SERVERNAME"`
(`-M` = multi-subnet failover in classic ODBC sqlcmd; the Go sqlcmd ignores `-M` and always enables it) before and after a test failover.

## Gotchas
- A listener on a port other than 1433 must be named with the port in the connection string (`listener,port`).
- Read-only routing needs a connection to the listener with `ApplicationIntent=ReadOnly`, a database in the AG, and routing configured on every replica.
- With TLS, the certificate on each node needs the listener FQDN in its Subject Alternative Name; Kerberos needs an SPN registered for the listener.

## Verify
Failover drill: application reconnects within seconds, `@@SERVERNAME` changes, no DNS-related delay.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: listener connectivity page (MultiSubnetFailover parallel connect, TCP only, recommended for single subnet too, ApplicationIntent=ReadOnly, nondefault port syntax, SAN and SPN notes), ALTER AVAILABILITY GROUP page (WITH IP syntax, DHCP not for production), Learn search results for RegisterAllProvidersIP/HostRecordTTL (default 20-minute cache, 300 s example, need offline/online), Azure DNN page (version gates, port, script, is_distributed_network_name), sqlcmd page (-M). Removed as unconfirmed: the ~21 s per dead IP figure, the CNO permission detail, the 59999 probe port detail, the gratuitous-ARP claim, and the VCO-deletion gotcha. Wrong in the draft: the 1433 gotcha contradicted the DNN page, which says never to use 1433.
Method: documentation only; no commands were run.
