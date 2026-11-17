---
id: computing-software.systems-network-administration.windows-server.ipv6-configuration-and-disabledcomponents
name: ipv6-configuration-and-disabledcomponents
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, network-adapters, ipv6-windows, disabledcomponents, prefer-ipv4, dual-stack]
level: advanced
status: docs-checked
description: "Configure IPv6 on Windows Server properly: why not to unbind it, DisabledComponents values (prefer IPv4 over IPv6), static IPv6 addressing and verification."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/new-netipaddress
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/set-netipv6protocol
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/get-netprefixpolicy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6 on Windows Server and DisabledComponents

IPv6 is a mandatory part of Windows Server 2008 and later. Microsoft does not recommend disabling IPv6, its
components, or unbinding it from interfaces: Windows is tested with IPv6 bound and functional, and some components
may not work without it. By default Windows prefers IPv6 global unicast addresses over IPv4. If you want IPv4
preferred, use **Prefer IPv4 over IPv6** (DisabledComponents 0x20) instead.

## DisabledComponents
`HKLM\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters\DisabledComponents` (DWORD, 0x00 default, 0xFF maximum,
restart needed). Microsoft notes that values other than 0 or 32 make the Routing and Remote Access service fail:
| Value | Effect |
|---|---|
| 0x20 (32) | prefer IPv4 over IPv6 in the prefix policy (the recommended option) |
| 0x10 | disable IPv6 on all non-tunnel interfaces |
| 0x01 | disable IPv6 on all tunnel interfaces |
| 0x11 | disable non-tunnel interfaces (except loopback) and tunnel interfaces |
| 0xFF | disable IPv6 (loopback still works, so `ping ::1` succeeds); not recommended |

The value is a bitmask: bit 0 tunnel, 1 6to4, 2 ISATAP, 3 Teredo, 4 native (also PPP), 5 prefer IPv4 in the default
prefix policy, 6 CP, 7 IP-TLS. The setting does not change the adapter binding check box.
```powershell
New-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters' -Name DisabledComponents -PropertyType DWord -Value 0x20 -Force
Get-NetPrefixPolicy        # after restart ::ffff:0:0/96 has higher precedence than ::/0
```
Setting 0xFFFFFFFF instead of 0xFF delays startup by five seconds; the correct value to disable is 0xFF.

## Static IPv6
```powershell
New-NetIPAddress -InterfaceAlias Ethernet -IPAddress 2001:db8:10::13 -PrefixLength 64 -DefaultGateway 2001:db8:10::1
Set-DnsClientServerAddress -InterfaceAlias Ethernet -ServerAddresses 2001:db8:10::11,10.0.10.11
Set-NetIPv6Protocol -RandomizeIdentifiers Disabled      # stable interface IDs for servers
Set-NetIPInterface -InterfaceAlias Ethernet -AddressFamily IPv6 -RouterDiscovery Disabled   # if no RA wanted
```

## Verify
- [ ] `Get-NetIPAddress -AddressFamily IPv6` shows expected addresses; `Test-NetConnection -ComputerName <host> -Port 445` works over both stacks.
- [ ] `ping -6` and `ping -4` to a DC succeed; nobody unticked IPv6 in adapter bindings (`Get-NetAdapterBinding -ComponentID ms_tcpip6`).

## Checked

2026-10-27. Documentation release: Support Articles 'Guidance for configuring IPv6 in Windows for advanced users' (dated 2026-02-12) and the NetTCPIP cmdlet references (Windows Server 2022 docset). Confirmed: DisabledComponents location, values and bit meanings, RRAS warning for values other than 0 or 32, 0xFF versus 0xFFFFFFFF delay, prefix policy precedence check, IPv6 default preference, the recommendation not to disable or unbind, and the cmdlet parameters -RandomizeIdentifiers and -RouterDiscovery. Removed the list of affected products and the AAAA/reverse zone note as unconfirmed.

Method: documentation only; no commands were run.
