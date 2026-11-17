---
id: computing-software.systems-network-administration.dns-dhcp.windows-dhcpv6-scopes
name: windows-dhcpv6-scopes
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, windows-dhcp, windows-dhcpv6, dhcpv6, dhcpserver-powershell, ipv6]
level: practitioner
status: docs-checked
description: "Create Windows DHCPv6 scopes and set scope or server options (DNS servers, search list, info refresh time) with the DhcpServer PowerShell cmdlets."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/add-dhcpserverv6scope
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/set-dhcpserverv6optionvalue
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows DHCPv6 scopes

## Create a scope
```powershell
Add-DhcpServerv6Scope -ComputerName dhcp1 -Prefix 2001:db8:30:: -Name "VLAN30" -PreferredLifeTime 8.00:00:00 -ValidLifeTime 12.00:00:00
```
- `-Prefix` is the IPv6 prefix of the scope; `-Name` and `-Description` label it.
- Documented defaults: preferred lifetime 8 days, valid lifetime 12 days, renewal time T1 4 days, rebind time T2 6.4 days, preference 0 (allowed 0 through 255). The preferred lifetime must be the same as or less than the valid lifetime.
- T1: the client renews by unicast to the server that gave the lease; T2: it then multicasts to any DHCP server.

## Options
```powershell
Set-DhcpServerv6OptionValue -ComputerName dhcp1 -Prefix 2001:db8:30:: -DnsServer 2001:db8::53 -DomainSearchList corp.example.com
Set-DhcpServerv6OptionValue -ComputerName dhcp1 -DnsServer 2001:db8::53 -DomainSearchList corp.example.com   # server level
```
- With `-Prefix` the option is set on that scope; without it, at server level.
- `-InfoRefreshTime` sets the upper bound of how long a client waits before refreshing information; it is used with stateless DHCPv6, where there are no leases to tell the client when to return.
- Other options can be set by `-OptionId` and `-Value`, optionally per `-VendorClass` or `-UserClass`.
- `-DnsServer` / option ID 23 values are validated unless validation is skipped.

## Router side
DHCPv6 depends on router advertisements (the managed/other-config flags) set on the router; configure them on your router platform from its own documentation. This skill does not cover that syntax.

## Verify
- [ ] The scope exists on the server with the intended lifetimes and clients obtain a DHCPv6 address or options (stateless).

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read the Add-DhcpServerv6Scope and Set-DhcpServerv6OptionValue Learn pages. Removed as not in those pages: the /64-only rule, exclusion ranges and reservations by DUID/IAID, Cisco commands, Windows failover and prefix-delegation limits, and the Android statement.
