---
id: computing-software.systems-network-administration.windows-server.windows-dhcp-scopes-and-options
name: windows-dhcp-scopes-and-options
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, add-dhcpserverv4scope, dhcp-options, dhcp-scope, dhcp-reservations, exclusion-range, server-options]
level: practitioner
status: docs-checked
description: "Create and manage Windows DHCP scopes with PowerShell: ranges, exclusions, lease duration, server vs scope vs reservation options, reservations, activation and lease inspection."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/dhcp-scopes
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/dhcp-subnet-options
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/add-dhcpserverv4scope
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/set-dhcpserverv4optionvalue
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/set-dhcpserversetting
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/add-dhcpserverv4reservation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows DHCP scopes

## Create a scope
```powershell
Add-DhcpServerv4Scope -ComputerName dhcp01 -Name "HQ-Floor2" -StartRange 10.20.2.1 -EndRange 10.20.2.254 `
  -SubnetMask 255.255.255.0 -LeaseDuration 1.00:00:00 -State InActive
Add-DhcpServerv4ExclusionRange -ComputerName dhcp01 -ScopeId 10.20.2.0 -StartRange 10.20.2.1 -EndRange 10.20.2.20
Set-DhcpServerv4OptionValue -ComputerName dhcp01 -ScopeId 10.20.2.0 -Router 10.20.2.1
Set-DhcpServerv4Scope -ComputerName dhcp01 -ScopeId 10.20.2.0 -State Active
```
Create the scope inactive, configure it, then activate it. A domain-joined server must be authorised in AD before it leases addresses (`Add-DhcpServerInDC`).

## Option levels
`Set-DhcpServerv4OptionValue` sets the level from the parameters you give: none of `-ScopeId`/`-ReservedIP` is server level, `-ScopeId` is scope level, `-ReservedIP` is reservation level, and `-PolicyName` targets a policy.
| Level | Use for |
|---|---|
| Server | org-wide: DNS servers, DNS domain name |
| Scope | per subnet: router, maybe different DNS |
| Policy | per vendor/user class or MAC filter (see policies skill) |
| Reservation | per device |
```powershell
Set-DhcpServerv4OptionValue -ComputerName dhcp01 -DnsServer 10.0.0.10,10.0.0.11 -DnsDomain corp.example.com   # server level
Set-DhcpServerv4OptionValue -ComputerName dhcp01 -ScopeId 10.20.2.0 -OptionId 42 -Value 10.0.0.30             # NTP servers
Get-DhcpServerv4OptionValue -ComputerName dhcp01 -ScopeId 10.20.2.0 -All
```
The cmdlet has shortcut parameters `-Router`, `-DnsServer`, `-DnsDomain`, `-WinsServer` and `-Wpad`; other options use `-OptionId` with `-Value`.

## Reservations
```powershell
Add-DhcpServerv4Reservation -ComputerName dhcp01 -ScopeId 10.20.2.0 -IPAddress 10.20.2.50 -ClientId "00-15-5D-01-02-03" -Description "Printer 2F"
Get-DhcpServerv4Reservation -ComputerName dhcp01 -ScopeId 10.20.2.0
```
A reservation assigns an IP address to a specific client device based on its MAC address (`-ClientId`). Exclusion ranges are addresses the server is not allowed to lease.

## Leases and health
```powershell
Get-DhcpServerv4Lease -ComputerName dhcp01 -ScopeId 10.20.2.0 | Sort IPAddress | Select IPAddress, ClientId, HostName, AddressState, LeaseExpiryTime
Get-DhcpServerv4ScopeStatistics -ComputerName dhcp01 | Where-Object PercentageInUse -gt 80
Get-DhcpServerv4Statistics -ComputerName dhcp01
```
- `-LeaseDuration` uses the format `day.hrs:mins:secs`.
- Conflict detection: `Set-DhcpServerSetting -ConflictDetectionAttempts` takes 0 to 5 (default 0); use it when static IPs might overlap the range, preferably with exclusion ranges for every static address.
- Relays: a relay agent's GIADDR must fall inside an active scope range or the server treats it as a rogue relay.

## Verify
- [ ] New scope active with router, DNS and domain options; a client gets a lease with correct options (`ipconfig /all`).
- [ ] Scope utilisation monitored (`Get-DhcpServerv4ScopeStatistics` shows `PercentageInUse`).

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DhcpServer module) repositories, latest commit 2026-10-23. Confirmed: Add-DhcpServerv4Scope `-State`, `-LeaseDuration` (day.hrs:mins:secs), `-SubnetMask`; how Set-DhcpServerv4OptionValue chooses server, scope or reservation level and its shortcut parameters; reservations by MAC and exclusion semantics (scopes article); `ConflictDetectionAttempts` range 0 to 5 and default 0; GIADDR rogue-relay rule (subnet selection article). Removed the option-ID list, the 'most specific wins' precedence claim, lease-duration advice, the 85 percent threshold (docs example uses 80) and the router-helper wording that the checked pages do not support.

Method: documentation only; no commands were run.
