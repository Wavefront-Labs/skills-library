---
id: computing-software.systems-network-administration.dns-dhcp.windows-server-ipam
name: windows-server-ipam
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, windows-ipam, ipam, windows-dhcp, windows-dns, address-management]
level: practitioner
status: docs-checked
description: "Windows Server IPAM scope: server discovery, central DNS management, role-based access control, GPO provisioning and range import cmdlets, and where to read the detail."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/ipam/ipam-top
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/
  - https://raw.githubusercontent.com/MicrosoftDocs/windowsserverdocs/main/WindowsServerDocs/networking/technologies/ipam/Manage-IPAM.md
  - https://raw.githubusercontent.com/MicrosoftDocs/windowsserverdocs/main/WindowsServerDocs/networking/technologies/ipam/Role-based-Access-Control.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Server IPAM

IPAM is an integrated suite of tools for planning, deploying, managing and monitoring an IP address
infrastructure. It automatically discovers IP address infrastructure servers and DNS servers on the
network and lets you manage them from a central interface. The Learn page lists Windows Server 2016
to 2025 as applicable versions.

## What it manages
- Windows Server 2016 IPAM supports DNS resource record, conditional forwarder and DNS zone
  management for both domain-joined Active Directory-integrated and file-backed DNS servers.
- Role-based access control can restrict users to specific DNS resource records, to records of a
  given type (for example PTR or MX), or to records in specific zones; access can be set at DNS
  server, zone and resource record level.
- The Manage IPAM guide has sections on managing resources in multiple Active Directory forests
  and on purging utilization data.

## Cmdlets (ipamserver module)
- `Invoke-IpamGpoProvisioning`: creates and links group policies in a domain for the access
  settings the IPAM server needs on the servers it manages.
- `Import-IpamRange`, `Import-IpamAddress`, `Import-IpamSubnet`: import objects from a file.
- `Add-IpamRange`, `Add-IpamAddress`, `Add-IpamAddressSpace`: add objects to IPAM.
Read each cmdlet's page for parameters before use.

## Limits
- This is a Windows-ecosystem tool; the pages describe Windows DNS and DHCP servers, so plan other
  DNS/DHCP products separately.

## Verify
- [ ] Every DNS/DHCP server you expect is discovered and reports as managed in the IPAM console.
- [ ] Access control roles restrict users only to the records, types and zones intended.

## Checked
2026-11-01. Confirmed from the IPAM overview page, the ipamserver cmdlet index and the Manage IPAM
and Role-based Access Control pages in the Windows Server docs repository. Removed (not stated on
those pages): the GPO names, install command, discovery click paths, database sizing advice, IPAM
security group names, the Windows Server 2012 claim, the "no BIND/Kea/Infoblox" statement as a
fact, and the address-tracking details.
Method: documentation only; no commands were run.
