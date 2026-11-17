---
id: computing-software.systems-network-administration.windows-server.rras-lan-routing-and-nat
name: rras-lan-routing-and-nat
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, remote-access, rras, rras-nat, lan-routing, new-netnat, ip-forwarding, static-routes, new-netroute, lab-networking]
level: practitioner
status: docs-checked
description: "Use Windows Server as a router or NAT gateway: IP forwarding, static routes with New-NetRoute, RRAS LAN routing and NAT, and the lightweight New-NetNat option."
sources:
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-access/remote-access
  - https://learn.microsoft.com/en-us/powershell/module/netnat/new-netnat
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/new-netroute
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RRAS LAN routing and NAT

Mainly for labs, isolated test networks and small edge cases; use dedicated network gear in production.

## Simple forwarding between two NICs
```powershell
Set-NetIPInterface -InterfaceAlias 'LAN-A','LAN-B' -Forwarding Enabled
New-NetRoute -DestinationPrefix 10.50.0.0/16 -InterfaceAlias 'LAN-B' -NextHop 10.20.0.1 -RouteMetric 10
Get-NetRoute -AddressFamily IPv4 | ? DestinationPrefix -ne '0.0.0.0/0' | Sort RouteMetric
```
Routes added with `New-NetRoute` are saved in both the ActiveStore and the PersistentStore by default; `-PolicyStore ActiveStore` creates one that is lost at reboot.
Hosts on each side need a route back (default gateway or static route) to the other subnet.

## RRAS LAN routing + NAT (GUI-managed)
```powershell
Install-WindowsFeature RemoteAccess -IncludeManagementTools
Install-RemoteAccess -VpnType RoutingOnly
```
Then configure NAT and static routes in the Routing and Remote Access console (menu paths vary by Windows Server version, so follow the current Remote Access docs).

## Lightweight NAT for Hyper-V internal switches (no RRAS)
```powershell
New-VMSwitch -Name NatSwitch -SwitchType Internal
New-NetIPAddress -IPAddress 192.168.100.1 -PrefixLength 24 -InterfaceAlias 'vEthernet (NatSwitch)'
New-NetNat -Name LabNat -InternalIPInterfaceAddressPrefix 192.168.100.0/24
Add-NetNatStaticMapping -NatName LabNat -Protocol TCP -ExternalIPAddress 0.0.0.0 -ExternalPort 8443 -InternalIPAddress 192.168.100.10 -InternalPort 443
```
`New-NetNat` takes `-InternalIPInterfaceAddressPrefix`; `Add-NetNatStaticMapping` takes `-NatName`, `-Protocol`, `-ExternalIPAddress`, `-ExternalPort`, `-InternalIPAddress` and `-InternalPort`.

## Verify
- [ ] `tracert` from a client shows the Windows router as a hop.
- [ ] `Get-NetNatSession` shows translations for lab VMs.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, windows-powershell-docs (winserver2025-ps RemoteAccess, NetNat, NetTCPIP), azure-docs vpn-gateway articles, SupportArticles-docs (troubleshoot-always-on-vpn, ms.date 2026-02-12).
Confirmed from the winserver2025-ps NetTCPIP and NetNat reference pages: New-NetRoute default store behaviour, Set-NetIPInterface -Forwarding, New-NetNat and Add-NetNatStaticMapping parameters, Get-NetNatSession,
and Install-RemoteAccess -VpnType RoutingOnly with Install-WindowsFeature RemoteAccess (anycast DNS page).
Removed the 'Install-WindowsFeature Routing' line, the console menu path and the one-NetNat-per-host claim, which the pages do not state.
Method: documentation only; no commands were run.
