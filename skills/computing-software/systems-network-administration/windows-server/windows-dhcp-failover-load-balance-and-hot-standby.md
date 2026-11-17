---
id: computing-software.systems-network-administration.windows-server.windows-dhcp-failover-load-balance-and-hot-standby
name: windows-dhcp-failover-load-balance-and-hot-standby
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, dhcp-failover, load-balance-mode, hot-standby-mode, mclt, add-dhcpserverv4failover, dhcp-high-availability]
level: practitioner
status: docs-checked
description: "Configure Windows Server DHCP failover: load balance vs hot standby, MCLT, replicating scope changes, partner down and troubleshooting."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/dhcp-failover
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/manage-dhcp-failover-relationships
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/dhcp-server-events
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/add-dhcpserverv4failover
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/invoke-dhcpserverv4failoverreplication
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/set-dhcpserverv4failover
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DHCP failover (load balance and hot standby)

Windows Server DHCP failover (2012+) pairs two servers that share lease information for IPv4 scopes. It replaces split-scope and clustered DHCP.

## Modes
| Mode | Behaviour | Use |
|---|---|---|
| Load balance (default) | both servers receive requests, one answers based on a hash of the client MAC address (default 50/50) | two servers in the same site |
| Hot standby | the active server answers; the standby serves new leases from a reserved percentage (default 5%) of addresses if the active server does not respond | branch with a central standby |

## Create
```powershell
Add-DhcpServerv4Failover -ComputerName dhcp01 -PartnerServer dhcp02 -Name "HQ-Failover" `
  -ScopeId 10.20.2.0,10.20.3.0 -LoadBalancePercent 50 `
  -MaxClientLeadTime 01:00:00 -AutoStateTransition $true -StateSwitchInterval 01:00:00 `
  -SharedSecret '<SHARED_SECRET>'
# hot standby:
Add-DhcpServerv4Failover -ComputerName hq-dhcp -PartnerServer br-dhcp -Name "Branch1" -ScopeId 10.30.1.0 `
  -ServerRole Active -ReservePercent 5 -MaxClientLeadTime 01:00:00
Get-DhcpServerv4Failover -ComputerName dhcp01
```
- Run from one server; the scopes are replicated to the partner.
- **MCLT** (maximum client lead time, default 1 hour): in hot standby, if the standby uses up its reserve before the MCLT expires it refuses new leases (still renewing existing ones) until the MCLT expires.
- **Auto state transition** (default False): when True, the server moves from COMMUNICATION INTERRUPTED to PARTNER DOWN after `StateSwitchInterval`. Otherwise an admin sets partner down manually.
- Without `-SharedSecret`, message digest authentication is off; failover messages use TCP port 647.
- Server clocks must stay within one minute of each other; setup halts with a critical error if they differ by more, and a receiving server logs a critical event for messages more than a minute off.

## Day-2: scope changes do NOT sync automatically
Options, reservations, exclusions and policies changed on one server must be replicated:
```powershell
Invoke-DhcpServerv4FailoverReplication -ComputerName dhcp01 -Name "HQ-Failover"        # whole relationship
Invoke-DhcpServerv4FailoverReplication -ComputerName dhcp01 -ScopeId 10.20.2.0
```
Make replication part of every change (or scheduled task). Lease data is shared automatically. When partners run different OS versions, change settings and replicate from the server with the newer OS.

## Partner down
```powershell
Set-DhcpServerv4Failover -ComputerName dhcp01 -Name "HQ-Failover" -PartnerDown          # when dhcp02 is known dead
Get-DhcpServerv4Failover -ComputerName dhcp01 | Select Name, State, PartnerServer
```
Relevant states: NORMAL, COMMUNICATION INTERRUPTED, PARTNER DOWN and RECOVER; transitions are logged as failover events (error level when leaving NORMAL or entering PARTNER DOWN, information when entering NORMAL).

## Troubleshooting
| Symptom | Fix |
|---|---|
| Clients split unevenly | check the load balance percentage; replicate config |
| State stuck in COMMUNICATION INTERRUPTED | firewall TCP 647, shared secret mismatch, time skew |
| Options differ between servers | run failover replication |
| Events 20291/20292 | BINDING-ACK messages sent or received with a reject reason from the partner |
Logs: Applications and Services Logs > Microsoft > Windows > DHCP-Server (Operational, Administrative, System, Filter Notification and Audit channels).

## Verify
- [ ] Relationship in Normal state; stopping DHCP on one server still lets clients renew and obtain leases.
- [ ] A test option change replicated and identical on both servers (`Get-DhcpServerv4OptionValue` diff).

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DhcpServer module) repositories, latest commit 2026-10-23. Confirmed: load balance default with a 50/50 MAC-hash split; hot standby reserve default 5%; MCLT default 1 hour and the exhausted-reserve behaviour; `AutoStateTransition` default False and `StateSwitchInterval` semantics; TCP 647; one-minute time tolerance; manual replication of scope settings and lease sharing; newer-OS-first replication rule; events 20291 and 20292; parameters of Add-DhcpServerv4Failover, Invoke-DhcpServerv4FailoverReplication and Set-DhcpServerv4Failover (`-PartnerDown`). Removed the Bad Address symptom, the RecoverWait state and the name-resolution cause, which the checked pages do not state; `-SharedSecret` is now a placeholder because the cmdlet takes a string.

Method: documentation only; no commands were run.
