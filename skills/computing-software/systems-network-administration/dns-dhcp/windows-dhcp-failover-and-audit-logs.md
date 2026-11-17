---
id: computing-software.systems-network-administration.dns-dhcp.windows-dhcp-failover-and-audit-logs
name: windows-dhcp-failover-and-audit-logs
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, windows-dhcp, dhcp-failover, windows-dhcp-failover, hot-standby, load-balance, mclt, add-dhcpserverv4failover, dhcp-audit-log, dhcp-authorization, dhcpserver-powershell, partner-down]
level: practitioner
status: docs-checked
description: "Configure Windows Server DHCP failover (load balance or hot standby, MCLT, state switchover), replicate scope changes, authorise servers in AD, and read the DHCP audit logs."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/dhcp-failover
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/add-dhcpserverv4failover
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows DHCP failover and audit logs

## Failover relationship
```powershell
Add-DhcpServerv4Failover -ComputerName dhcp1 -PartnerServer dhcp2 -Name "dhcp1-dhcp2" `
  -ScopeId 10.20.10.0,10.20.20.0 -LoadBalancePercent 50 -MaxClientLeadTime 01:00:00 `
  -SharedSecret '<SECRET>' -AutoStateTransition $true -StateSwitchInterval 01:00:00
# hot standby variant:
Add-DhcpServerv4Failover -ComputerName dhcp1 -PartnerServer dhcp2 -Name "hq-dr" -ScopeId 10.30.0.0 `
  -ServerRole Active -ReservePercent 5 -MaxClientLeadTime 01:00:00
Get-DhcpServerv4Failover
```
- **Load balance**: both serve (hash split, default 50/50). **Hot standby**: active serves, standby
  keeps `ReservePercent` of addresses for when the active is down.
- **MCLT** (Maximum Client Lead Time): how far a server may extend a lease beyond what the partner
  knows; also how long after entering partner-down before a server can use the whole pool.
- **StateSwitchInterval / AutoStateTransition**: automatically move from communication-interrupted
  to partner-down after the interval; without it an admin must set partner-down manually
  (see `Set-DhcpServerv4Failover`).
- IPv4 only: DHCPv6 scopes cannot be failover-enabled.

## Keep configs in sync
Changes to a failover-enabled scope must be replicated to the partner manually; replication overwrites the partner's settings, so run it from the server whose settings you want to keep:
```powershell
Invoke-DhcpServerv4FailoverReplication -ComputerName dhcp1 -Name "dhcp1-dhcp2"
```
Run after changes (or schedule it); differences cause clients to get different options depending on
which server answers.

## Authorisation in AD
Authorise Windows DHCP servers in AD:
`Add-DhcpServerInDC -DnsName dhcp1.corp.example -IPAddress 10.0.0.67`; `Get-DhcpServerInDC`.

## Audit logs
`Get-DhcpServerAuditLog` returns the audit-log configuration (path and settings) of the DHCP server.
Look up the log file layout and event ID meanings in the Microsoft DHCP audit-log reference before
parsing it.
Ship them to the SIEM; they are the record of who had an IP when.

## Verify
- [ ] `Get-DhcpServerv4Failover` shows state Normal on both servers.
- [ ] Stopping dhcp1 lets dhcp2 serve all clients after the state switch interval.
- [ ] Audit log events reach the SIEM.

## Checked
2026-10-28. Confirmed against the Microsoft Learn DHCP failover overview and Add-DhcpServerv4Failover reference: load balance default 50:50 via MAC hash, hot standby ReservePercent default 5, MaxClientLeadTime default 1 hour, standby uses the whole pool only after the MCLT expires, AutoStateTransition/StateSwitchInterval, manual replication, DHCPv4-only. Confirmed in the DhcpServer module index: Invoke-DhcpServerv4FailoverReplication, Set-DhcpServerv4Failover, Add-DhcpServerInDC, Get-DhcpServerInDC, Get-DhcpServerAuditLog. Removed as unconfirmed: audit-log file name, rotation and event ID table.
Method: documentation only; no commands were run.
