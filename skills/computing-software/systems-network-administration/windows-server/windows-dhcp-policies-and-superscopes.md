---
id: computing-software.systems-network-administration.windows-server.windows-dhcp-policies-and-superscopes
name: windows-dhcp-policies-and-superscopes
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, dhcp-policies, superscope, vendor-class, user-class, mac-filtering, multinet]
level: practitioner
status: docs-checked
description: "Use Windows DHCP policies to hand out options or ranges by vendor class, user class, MAC or FQDN, plus superscopes for multinets: conditions, processing order and PXE examples."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/add-dhcpserverv4policy
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/add-dhcpserverv4policyiprange
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/add-dhcpserverv4superscope
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/add-dhcpserverv4class
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/set-dhcpserverv4optionvalue
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# DHCP policies and superscopes

## Policies
Policies assign IP ranges and/or options to clients matching conditions. A policy is created at the server level or, with `-ScopeId`, at the scope level; the name must be unique at its level and it needs at least one condition.

Condition parameters: `-VendorClass`, `-UserClass`, `-MacAddress` (wildcards such as `00155D*`), `-ClientId`, `-Fqdn`, `-RelayAgent`, `-CircuitId`, `-RemoteId`, `-SubscriberId`. `-Condition` combines them with AND or OR; operators include EQ and NE.

### Example: policy by vendor class
```powershell
Add-DhcpServerv4Policy -ComputerName dhcp01 -ScopeId 10.20.2.0 -Name "PrinterPolicy" -Condition OR -VendorClass EQ,"HP Printer","Xerox Printer"
Set-DhcpServerv4OptionValue -ComputerName dhcp01 -ScopeId 10.20.2.0 -PolicyName "PrinterPolicy" -OptionId 66 -Value "tftp.example.com"
```
Use `-Type Vendor` classes (`Add-DhcpServerv4Class -Name ... -Type Vendor -Data ...`) when the client's class string is not already defined.


### Example: separate range for IP phones by MAC prefix
```powershell
Add-DhcpServerv4Policy -ComputerName dhcp01 -ScopeId 10.20.2.0 -Name "Phones" -Condition OR -MacAddress EQ,"001565*"
Add-DhcpServerv4PolicyIPRange -ComputerName dhcp01 -ScopeId 10.20.2.0 -Name "Phones" -StartRange 10.20.2.200 -EndRange 10.20.2.240
Set-DhcpServerv4OptionValue -ComputerName dhcp01 -ScopeId 10.20.2.0 -PolicyName "Phones" -OptionId 66 -Value "tftp.voice.example.com"
```

### Processing order
- `-ProcessingOrder` sets the order in which policies are evaluated.
- Policies in a failover relationship are scope settings: replicate them (`Invoke-DhcpServerv4FailoverReplication`).
- A MAC address is not a security control; use 802.1X/NAC for access control.

## Superscopes (multinets)
A superscope groups scopes. `Add-DhcpServerv4Superscope` adds one or more IPv4 scopes to a superscope and creates the superscope if it does not exist; a scope already in another superscope is moved only with `-Force`. Typical use is several subnets on the same physical network segment (for example a second subnet added when the first /24 ran out).
```powershell
Add-DhcpServerv4Superscope -ComputerName dhcp01 -SuperscopeName "Floor2-Multinet" -ScopeId 10.20.2.0,10.20.12.0
Get-DhcpServerv4Superscope -ComputerName dhcp01
Get-DhcpServerv4SuperscopeStatistics -ComputerName dhcp01
```
- The router interface on that segment needs addresses in every member subnet.

## Verify
- [ ] A matching test client lands in the policy range and receives option 66.
- [ ] `Get-DhcpServerv4SuperscopeStatistics` shows the member scopes.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DhcpServer module) repositories, latest commit 2026-10-23. Confirmed: Add-DhcpServerv4Policy: server- vs scope-level creation, name uniqueness, condition parameters, `-Condition` OR/AND, MAC wildcard and vendor class examples, `-ProcessingOrder`; Add-DhcpServerv4PolicyIPRange, Add-DhcpServerv4Class (`-Type`, `-Data`) and Add-DhcpServerv4Superscope parameters and `-Force` behaviour; `Set-DhcpServerv4OptionValue -PolicyName`. Removed the PXE UEFI/BIOS example (class strings and boot file names are not in the checked pages), the option numbers for conditions, the precedence rules between policy levels and the range-selection behaviour, none of which the checked pages state.

Method: documentation only; no commands were run.
