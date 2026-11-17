---
id: computing-software.systems-network-administration.windows-server.windows-firewall-rules-and-profiles
name: windows-firewall-rules-and-profiles
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-firewall, netsecurity-module, new-netfirewallrule, firewall-profiles, get-netfirewallrule, network-category, inbound-rules]
level: practitioner
status: docs-checked
description: "Manage Windows Defender Firewall with NetSecurity cmdlets: profiles and network category, scoped inbound rules, remote address filters, auditing effective rules."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/netsecurity/new-netfirewallrule
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/configure-with-command-line
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall rules and profiles with NetSecurity cmdlets

## Profiles
Domain, Private, Public.
```powershell
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

## Scoped rules
```powershell
New-NetFirewallRule -DisplayName 'SQL 1433 from app tier' -Direction Inbound -Protocol TCP -LocalPort 1433 `
  -RemoteAddress 10.20.0.0/24 -Profile Domain -Action Allow -Group 'SQL'
New-NetFirewallRule -DisplayName 'Block SMB from users' -Direction Inbound -Protocol TCP -LocalPort 445 `
  -RemoteAddress 10.50.0.0/16 -Action Block
Set-NetFirewallRule -DisplayGroup 'Windows Firewall Remote Management' -Enabled True
```
- `-RemoteAddress` keywords include LocalSubnet, DNS, DHCP, DefaultGateway, Internet and Intranet.

## Audit what is actually allowed
```powershell
Get-NetFirewallRule -PolicyStore ActiveStore    # currently active policy
```
Port and address conditions are read with `Get-NetFirewallPortFilter` and `Get-NetFirewallAddressFilter`.

## Remote management
The NetSecurity cmdlets accept `-CimSession`.

## Verify
- [ ] All NICs on expected profile; inbound default Block.
- [ ] Connections from allowed and denied subnets behave as designed.

## Checked

2026-10-28. Confirmed against: New-NetFirewallRule reference (parameters, RemoteAddress keywords, ActiveStore, PortFilter/AddressFilter, CimSession) and the Windows Firewall configure-with-command-line page (Set-NetFirewallProfile, Set-NetFirewallRule -DisplayGroup). Removed (not confirmable from the cited pages): NLA/profile detection explanation, Get-NetFirewallProfile and NlaSvc restart, block-over-allow precedence, -Service, Get-NetFirewallRule filtering parameters, Test-NetConnection check.

Method: documentation only; no commands were run.
