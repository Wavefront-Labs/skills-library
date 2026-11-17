---
id: computing-software.systems-network-administration.windows-server.server-ip-configuration-powershell
name: server-ip-configuration-powershell
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, netadapter, server-networking, new-netipaddress, set-dnsclientserveraddress, nettcpip, interface-metric, rename-netadapter, set-dnsclient, register-dns, ipv6]
level: practitioner
status: docs-checked
description: "Configure server networking with NetTCPIP/NetAdapter cmdlets: rename NICs, static IPv4, DNS servers and suffix, interface metrics, DNS registration and IPv6 decisions."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/new-netipaddress
  - https://learn.microsoft.com/en-us/powershell/module/dnsclient/set-dnsclientserveraddress
  - https://learn.microsoft.com/en-us/powershell/module/dnsclient/set-dnsclient
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/connectivity-issues-multiple-default-gateways
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/automatic-metric-for-ipv4-routes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server IP configuration with PowerShell

```powershell
Get-NetAdapter | Select Name,InterfaceDescription,ifIndex,Status,MacAddress,LinkSpeed
Rename-NetAdapter -Name 'Ethernet0' -NewName 'LAN'
Set-NetIPInterface -InterfaceAlias 'LAN' -Dhcp Disabled
New-NetIPAddress -InterfaceAlias 'LAN' -IPAddress 10.0.10.25 -PrefixLength 24 -DefaultGateway 10.0.10.1
Set-DnsClientServerAddress -InterfaceAlias 'LAN' -ServerAddresses 10.0.0.10,10.0.0.11
Set-DnsClient -InterfaceAlias 'LAN' -ConnectionSpecificSuffix 'ad.example.com' -RegisterThisConnectionsAddress $true
Get-NetIPConfiguration -Detailed
```

## Changing an existing address
To change an address, remove the old address and default route first so `New-NetIPAddress` can set the new ones:
```powershell
Remove-NetIPAddress -InterfaceAlias 'LAN' -IPAddress 10.0.10.24 -Confirm:$false
Remove-NetRoute -InterfaceAlias 'LAN' -DestinationPrefix 0.0.0.0/0 -Confirm:$false
```
Doing this remotely drops your session; use PowerShell Direct, the console, or a scheduled
one-shot script with a rollback timer.

## Multi-homed servers
- Microsoft advises against default gateways across disjoint networks. Give only the primary/production NIC a
  gateway; other NICs (backup, storage, cluster) get none, with static routes for their remote subnets.
- Disable DNS registration on non-production NICs (`-RegisterThisConnectionsAddress $false`)
  or clients resolve the server to a backup-network IP.
- Interface metric decides which route wins when several tie; by default Windows derives it from link speed
  (Automatic Metric). Set one with `Set-NetIPInterface -InterfaceAlias LAN -InterfaceMetric 10`.

## IPv6
Microsoft does not recommend disabling or unbinding IPv6 on Windows Server; Windows is tested with it bound.
To prefer IPv4, set `DisabledComponents = 0x20` (see the ipv6-configuration-and-disabledcomponents skill).

## Verify
- [ ] `Get-NetIPConfiguration` shows one default gateway and the right DNS servers.
- [ ] `Resolve-DnsName <server>` returns only the production IP.
- [ ] `ipconfig /registerdns` completes and the DNS zone shows only the intended record.

## Checked

2026-10-27. Documentation release: NetTCPIP, DnsClient and NetAdapter cmdlet references (Windows Server 2022 docset), Support Articles on multiple default gateways and Automatic Metric, and the IPv6 configuration article. Confirmed: parameters used in the examples (-Dhcp, -InterfaceMetric, -RegisterThisConnectionsAddress, -ConnectionSpecificSuffix), default gateway guidance, automatic metric, IPv6 guidance. Removed the claim that New-NetIPAddress fails on an existing address and the event 8018 check as unconfirmed.

Method: documentation only; no commands were run.
