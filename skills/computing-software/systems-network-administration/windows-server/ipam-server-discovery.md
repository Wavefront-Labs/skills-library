---
id: computing-software.systems-network-administration.windows-server.ipam-server-discovery
name: ipam-server-discovery
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ipam, ip-address-management, ipam-discovery, add-ipamdiscoverydomain, server-inventory, manageability-status, ipam-tasks, access-status]
level: practitioner
status: docs-checked
description: "Configure IPAM server discovery: discovery domains and roles, the discovery scheduled task, setting servers Managed, and fixing blocked access status."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/ipam/manage-resources-in-multiple-active-directory-forests
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/add-ipamdiscoverydomain
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/add-ipamserverinventory
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/invoke-ipamgpoprovisioning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPAM server discovery

## Configure discovery
Server Manager > IPAM > Configure server discovery: choose domains and roles (DC, DHCP, DNS).
```powershell
Add-IpamDiscoveryDomain -Name ad.example.com -DiscoverDc $true -DiscoverDhcp $true -DiscoverDns $true
Get-IpamDiscoveryDomain
Get-IpamServerInventory
```
To discover servers in other forests, each forest needs a two-way trust with the IPAM forest; in the console use Configure Server Discovery > Get forests. Servers can also be added manually (`Add-IpamServerInventory -Name dhcp-dmz -ServerType DHCP -ManageabilityStatus Managed`; ServerType accepts DC, DHCP, DNS and NPS; ManageabilityStatus accepts Unspecified, Managed and Unmanaged).

## Bring servers under management
For each discovered server: **Manageability status = Managed**. IPAM gathers data only from Managed servers and adds them to the
provisioning GPO security filter list. Then:
```powershell
Invoke-Command -ComputerName dhcp01,dns01 { gpupdate /force }
# IPAM console: right-click server > Retrieve All Server Data
```
IPAM collects data with scheduled tasks created during provisioning; if data is stale, check the IPAM tasks' last run results in Task Scheduler.

## Fix "Blocked" access status
- The server must be Managed so it is in the GPO security filter list; then run `gpupdate /force` on it.
- Check that the IPAM GPOs (`<prefix>_DHCP`, `<prefix>_DNS`, `<prefix>_DC_NPS`) applied with `gpresult` on the target.
- The IPAM server's computer account must be in the universal group `IPAMUG` created by `Invoke-IpamGpoProvisioning`.

## Verify
- [ ] All target servers Managed and access status Unblocked with recent data.
- [ ] IPAM data collection tasks complete without errors.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs (IPAM articles) and windows-powershell-docs (Windows Server 2025 IpamServer module) repositories, latest commit 2026-10-23. Confirmed: Add-IpamDiscoveryDomain parameters (`-Name`, `-DiscoverDc`, `-DiscoverDhcp`, `-DiscoverDns`); Add-IpamServerInventory `-ServerType` (DC, DHCP, DNS, NPS) and `-ManageabilityStatus` (Unspecified, Managed, Unmanaged; data gathered only when Managed); trust requirement and Get forests discovery step; GPO security-filter behaviour and IPAMUG. Removed the AD discovery rules, the Start-ScheduledTask command and task-name list, and the Event Log Readers and DNS permission remedies, which the checked pages do not state.

Method: documentation only; no commands were run.
