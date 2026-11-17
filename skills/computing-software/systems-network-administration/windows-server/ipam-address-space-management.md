---
id: computing-software.systems-network-administration.windows-server.ipam-address-space-management
name: ipam-address-space-management
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ipam, ip-address-management, ipam-address-space, ip-address-blocks, ip-address-ranges, utilization-thresholds, add-ipamblock, add-ipamrange, find-ipamfreeaddress, custom-fields]
level: practitioner
status: docs-checked
description: "Model address space in IPAM: blocks, ranges, addresses, custom fields, utilisation thresholds and alerts, and finding free IPs for static assignments."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/add-ipamblock
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/add-ipamrange
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/add-ipamaddress
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/find-ipamfreeaddress
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/get-ipamaddressutilizationthreshold
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/import-ipamaddress
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# IPAM address space management

## Hierarchy
**IP address blocks** (e.g. `10.0.0.0/8`) > **IP address ranges** (e.g.
a /24 per VLAN) > **IP addresses**
(individual records, statics, reservations).

```powershell
Add-IpamBlock -NetworkId 10.20.0.0/16 -Description 'London site'
Add-IpamRange -NetworkId 10.20.30.0/24 -StartIPAddress 10.20.30.10 -EndIPAddress 10.20.30.250 `
  -ManagedByService 'IPAM' -ServiceInstance 'Localhost' -Description 'Server VLAN 30'
Add-IpamAddress -IpAddress 10.20.30.15 -DeviceName app15 -AssignmentType Static -Description 'App server'
```

## Find free addresses for statics
```powershell
Get-IpamRange -AddressFamily IPv4 | ? Description -eq 'Server VLAN 30' |
  Find-IpamFreeAddress -NumAddress 3 -TestReachability
```
`-TestReachability` tests the reachability of the candidate addresses. Without `-NumAddress` the cmdlet returns one free address.

## Utilisation
- Thresholds: `Get-IpamAddressUtilizationThreshold` returns UnderUtilizationThreshold 20 and OverUtilizationThreshold 80 in the cmdlet documentation's example; change them with `Set-IpamAddressUtilizationThreshold`.
- **Custom fields** (`Add-IpamCustomField`, `Add-IpamCustomFieldAssociation`) on ranges and addresses make filtering and logical groups possible.

## Keep it true
Import existing spreadsheets with `Import-IpamAddress` (CSV; the only required field is the IP address; the `InventoryImport` parameter set also removes addresses in the range that are missing from the CSV), then make IPAM the
place where new statics are allocated. Reconcile periodically against DNS and DHCP.

## Verify
- [ ] Every VLAN subnet exists as a range with Site/VLAN custom fields.
- [ ] `Find-IpamFreeAddress -TestReachability` returns genuinely unused addresses.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs (IPAM articles) and windows-powershell-docs (Windows Server 2025 IpamServer module) repositories, latest commit 2026-10-23. Confirmed: parameters of Add-IpamBlock, Add-IpamRange (`-ManagedByService`, `-ServiceInstance` Localhost in the docs example), Add-IpamAddress and Find-IpamFreeAddress (`-NumAddress`, `-TestReachability`); utilisation thresholds 20 and 80 from the Get-IpamAddressUtilizationThreshold example; Import-IpamAddress CSV rules and the InventoryImport behaviour. Removed `-Rir None` (the documented RIR values are AFRINIC, APNIC, ARIN, LACNIC and RIPE), the claim that the cmdlet pings and checks DNS, the AddressUtilization task name and the 'Unmapped address space' wording, which the checked pages do not state.

Method: documentation only; no commands were run.
