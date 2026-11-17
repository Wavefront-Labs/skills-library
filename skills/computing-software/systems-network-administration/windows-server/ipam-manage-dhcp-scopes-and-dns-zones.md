---
id: computing-software.systems-network-administration.windows-server.ipam-manage-dhcp-scopes-and-dns-zones
name: ipam-manage-dhcp-scopes-and-dns-zones
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ipam, ipam-dhcp-management, ipam-dns-management, dhcp, dns]
level: practitioner
status: docs-checked
description: "Manage DHCP scopes, reservations and DNS zones and records centrally from IPAM, with the access scopes and roles needed and where IPAM falls short."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/ipam/manage-ipam
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/ipam/role-based-access-control
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/ipam/manage-role-based-access-control-with-windows-powershell
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/get-ipamdhcpscope
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Manage DHCP and DNS from IPAM

Once servers are discovered and set to **Managed** with access status unblocked, IPAM manages DHCP and DNS on them from one console. In Windows Server 2016 IPAM supports DNS resource record, conditional forwarder and zone management for both AD-integrated and file-backed DNS servers.

## DHCP from IPAM
Server Manager > IPAM > DNS and DHCP Servers (or DHCP Scopes):
- Scope, option and reservation editing is done in the console.
```powershell
Get-IpamDhcpScope -ServerFqdn dhcp01.ad.example.com
Get-IpamDhcpServer
```

## DNS from IPAM
- Zones: view, create and edit zones; records: view, add, edit and delete resource records; conditional forwarders (all Windows Server 2016 and later).
```powershell
Get-IpamDnsServer
Get-IpamDnsZone -ZoneType Forward -ZoneName ad.example.com
Get-IpamDnsResourceRecord
```
The IpamServer module retrieves these objects; creating and editing them is done in the console.

## Delegation
Role-based access control restricts users to specific DNS servers, zones, record types or records; combine roles with access scopes (e.g. "Branch-Sydney"). See the IPAM role-based access control skill.

## Limits
- GPO-provisioned access must be working (managed servers, access status unblocked).

## Verify
- [ ] A change made in IPAM appears on the DHCP/DNS server (for example `Get-DhcpServerv4Reservation`).

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs (IPAM articles) and windows-powershell-docs (Windows Server 2025 IpamServer module) repositories, latest commit 2026-10-23. Confirmed: Manage IPAM article (Windows Server 2016 DNS record, conditional forwarder and zone management for AD-integrated and file-backed servers); the IpamServer cmdlets Get-IpamDhcpScope (`-ServerFqdn`), Get-IpamDhcpServer, Get-IpamDnsServer, Get-IpamDnsZone (`-ZoneType`, `-ZoneName`) and Get-IpamDnsResourceRecord; RBAC scoping levels. Removed Add-IpamDhcpReservation and Add-IpamResourceRecord (no such cmdlets in the IpamServer module), the `-ServerName` parameter (the cmdlet takes `-ServerFqdn`), the PercentageUtilized column and the limits list.

Method: documentation only; no commands were run.
