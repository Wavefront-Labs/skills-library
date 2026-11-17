---
id: computing-software.systems-network-administration.windows-server.dhcp-server-authorization
name: dhcp-server-authorization
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-dhcp-server, dhcpserver-module, dhcp-authorization, add-dhcpserverindc, rogue-dhcp, dhcp-snooping, dhcp-administrators, dnsupdateproxy, dhcp-dns-credentials]
level: practitioner
status: docs-checked
description: "Authorise Windows DHCP servers in AD, clean stale authorisations, understand rogue detection limits, and set DHCP DNS update credentials and security groups."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/dhcp-deploy-wps
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/dynamic-update
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/dhcp-server-events
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/add-dhcpserverindc
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/set-dhcpserverdnscredential
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCP server authorisation and security setup

## Authorise
Unauthorised DHCP servers in an AD domain do not lease addresses to clients. Authorising requires domain administrative rights.
```powershell
Install-WindowsFeature DHCP -IncludeManagementTools
Add-DhcpServerSecurityGroup                       # creates the DHCP Administrators and DHCP Users local groups
Add-DhcpServerInDC -DnsName dhcp01.ad.example.com -IPAddress 10.0.0.20
Get-DhcpServerInDC
# clear the Server Manager post-install alert
Set-ItemProperty -Path registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\ServerManager\Roles\12 -Name ConfigurationState -Value 2
Restart-Service DHCPServer
```
Remove stale entries for decommissioned servers: `Remove-DhcpServerInDC -DnsName old-dhcp -IPAddress 10.0.0.9`.

## Rogue detection limits
Authorisation is a Windows DHCP server feature: it stops unauthorised Windows DHCP servers in the domain, not other DHCP implementations. Switch-level DHCP snooping (vendor documentation) covers those.

## Dynamic DNS registration credentials
If DHCP registers A/PTR records for clients, configure a dedicated standard user account for dynamic update credentials. A DHCP server installed on a domain controller inherits the DC's authority over secure records, and event 1056 warns when a DHCP server on a DC has no credentials:
```powershell
Set-DhcpServerDnsCredential -Credential (Get-Credential AD\svc-dhcpdns) -ComputerName dhcp01
Set-DhcpServerv4DnsSetting -ComputerName dhcp01 -DynamicUpdates OnClientRequest -DeleteDnsRROnLeaseExpiry $true
```
Members of `DnsUpdateProxy` do not secure the names they register, so do not use that group in zones that allow only secure updates. The same credentials can be set with `netsh dhcp server set dnscredentials`.

## Verify
- [ ] `Get-DhcpServerInDC` lists only live servers.
- [ ] Event 1044 (authorised to start, servicing clients) in the DHCP Server log; no 1046 (not authorised) or 1056 (no DNS credentials on a DC) events.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DhcpServer module) repositories, latest commit 2026-10-23. Confirmed: unauthorised servers in an AD domain do not lease addresses; the netsh command that creates the DHCP Administrators and DHCP Users groups (deployment article) and the `Add-DhcpServerSecurityGroup` cmdlet; Server Manager `ConfigurationState` registry value 2 (deployment article); `Add-DhcpServerInDC -DnsName -IPAddress`; DNS credential guidance, DnsUpdateProxy and the DC-inherits-authority statement (Dynamic Update article); events 1044, 1046 and 1056 (DHCP server events). Removed the Enterprise Admins requirement and the NetServices container path (the migration article says domain administrative rights), the rogue-device list and the snooping checklist item.

Method: documentation only; no commands were run.
