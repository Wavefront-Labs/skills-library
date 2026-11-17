---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.network-troubleshooting-fundamentals
name: network-troubleshooting-fundamentals
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, networking, ping, tracert, nslookup, ipconfig, dns, dhcp, osi-model, wifi-roaming, packet-loss, latency, vlan, subnet, default-gateway, mtu, traceroute]
level: practitioner
status: docs-checked
description: "Windows network diagnosis for helpdesk: ipconfig, ping, tracert, nslookup, Resolve-DnsName bottom-up, DHCP renew and DNS flush switches, Test-NetConnection port tests."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ipconfig
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ping
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/tracert
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/nslookup
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection
  - https://learn.microsoft.com/en-us/powershell/module/dnsclient/resolve-dnsname
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# network-troubleshooting-fundamentals

Goal: the command sequence for "can't reach X", working from the machine outwards (see
`systematic-problem-isolation` for the method), with what each Windows tool is documented to do.

## The sequence, bottom-up
1. **`ipconfig /all`** shows the full TCP/IP configuration of every adapter. Plain `ipconfig`
   shows IPv4/IPv6 addresses, subnet mask and default gateway. The tool is most useful on
   machines set to obtain an address automatically, because it shows what DHCP, APIPA or an
   alternate configuration supplied.
2. **`ping <GATEWAY_IP>`**, then **`ping <PUBLIC_IP>`**.
3. **`nslookup <HOSTNAME>`** or **`Resolve-DnsName <HOSTNAME>`** (PowerShell) tests name
   resolution.
4. **`tracert <HOSTNAME>`** traces the route to the destination; the last responding hop
   shows where a path stops.

## DHCP and DNS switches
- `ipconfig /release` sends a DHCPRELEASE and discards the address configuration (this
  disables TCP/IP on adapters set to obtain an address automatically); `ipconfig /renew`
  renews DHCP configuration. Both accept an adapter name.
- `ipconfig /displaydns` shows the resolver cache; `ipconfig /flushdns` clears it, which
  Microsoft lists as a DNS troubleshooting step.

## Sampling packet loss
`ping /n <COUNT>` sets the number of echo requests; the default is 4, so use a larger count
for a loss figure that means something.

## Port tests
`Test-NetConnection -ComputerName <HOST> -Port
<PORT>` tests a TCP port on the remote computer.

## Verify
- Re-run the exact test that originally failed after the fix, rather than relying on the
  user saying it works.

## Checked
2026-11-01. Confirmed against the Microsoft Learn pages in `sources`: ipconfig parameters and
remarks, ping `/n` and its default of 4, tracert, nslookup, Test-NetConnection `-Port`,
Resolve-DnsName. Removed (no page read): 169.254 APIPA behaviour, the 8.8.8.8 test address,
`nslookup` against a named server, Wi-Fi roaming and band advice, packet loss versus latency
theory, ICMP-deprioritising hops, VLAN and subnet patterns, proxy and PAC notes, and
Linux/macOS commands.
Method: documentation only; no commands were run.
