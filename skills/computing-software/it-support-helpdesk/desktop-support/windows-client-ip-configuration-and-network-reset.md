---
id: computing-software.it-support-helpdesk.desktop-support.windows-client-ip-configuration-and-network-reset
name: windows-client-ip-configuration-and-network-reset
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, static-ip-configuration, network-profile, ipv6-client, netsh-winsock-reset, network-reset, dns-configuration]
level: practitioner
status: docs-checked
description: "Configure Windows client networking: static IP and DNS, public vs private network profiles and discovery, IPv6 behaviour, and when to use winsock and full network reset."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/nettcpip/new-netipaddress"
  - "https://learn.microsoft.com/en-us/powershell/module/netconnection/set-netconnectionprofile"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netsh-winsock"
  - "https://support.microsoft.com/en-us/windows/experience/connectivity-networking/fix-wi-fi-connection-issues-in-windows"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# windows-client-ip-configuration-and-network-reset

## Static IP and DNS
Most clients should use DHCP. When static is needed:
```powershell
Get-NetAdapter
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 192.168.10.50 -PrefixLength 24 -DefaultGateway 192.168.10.1
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 192.168.10.10,192.168.10.11
# back to DHCP
Set-NetIPInterface -InterfaceAlias "Ethernet" -Dhcp Enabled
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ResetServerAddresses
Remove-NetRoute -InterfaceAlias "Ethernet" -DestinationPrefix 0.0.0.0/0 -Confirm:$false
```
Document static assignments to avoid conflicts. The addresses above are
examples.

## Network profiles
- **Public**: for networks in public places; the PC is hidden from other
  devices and cannot be used for printer and file sharing. **Private** and
  **Domain** are the other categories.
- `Get-NetConnectionProfile`; change with
  `Set-NetConnectionProfile -InterfaceAlias "Wi-Fi" -NetworkCategory Private`.
- `Set-NetConnectionProfile` cannot set DomainAuthenticated; the system sets it
  automatically when the network is authenticated to a domain controller.
  A domain PC showing Public or Private on the office network has not
  authenticated to a DC; check connectivity and DNS to the DC.

## IPv6 on clients
- Microsoft does not recommend disabling IPv6 or unbinding it from
  interfaces; some Windows components might not function. To prefer IPv4
  instead, set `DisabledComponents` to `0x20` ("Prefer IPv4 over IPv6") under
  `HKLM\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters` (REG_DWORD),
  then restart. Back up the key first.
- The `DisabledComponents` value does not change the checkbox state on the
  adapter's Networking tab; that is expected.

## Reset ladder
1. `ipconfig /release`, `ipconfig /renew`, `ipconfig /flushdns`.
2. Disable and enable the adapter; uninstall the adapter driver in Device
   Manager and restart so Windows reinstalls it (have the driver available).
3. `netsh winsock reset` (resets the Winsock catalog to a clean state,
   removing custom LSPs) and `netsh int ip reset` (elevated), then restart.
4. **Network reset** (Settings, Network and internet, Advanced network
   settings, Network reset on Windows 11; Status, Network reset on Windows 10):
   removes and reinstalls network adapters with default settings. You may
   need to reinstall VPN clients and Hyper-V virtual switches, and known
   networks can revert to the public profile. Microsoft says to try it last.

## Verify
`ipconfig /all` shows the intended address, gateway and DNS;
`Get-NetConnectionProfile` shows the right category; name resolution and the
failing app work.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn NetTCPIP, DnsClient and NetConnection cmdlet pages, IPv6 configuration article, netsh winsock page, and Microsoft Support Wi-Fi/Ethernet troubleshooting pages that describe Network reset, as published October 2026. Confirmed: parameters of New-NetIPAddress, Set-DnsClientServerAddress and Set-NetConnectionProfile, Public category description, DomainAuthenticated cannot be set manually, IPv6 not recommended to disable and DisabledComponents 0x20 prefer-IPv4, netsh winsock reset behaviour, Network reset paths, effects and last-resort advice. Removed: 8.8.8.8 secondary-DNS claim, NlaSvc restart advice, SLAAC and rogue router notes, IPAM remark, router-advertisement claims.

Method: documentation only; no commands were run.
