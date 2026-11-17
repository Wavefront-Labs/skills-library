---
id: computing-software.it-support-helpdesk.remote-support-tools.vpn-mtu-and-fragmentation-problems
name: vpn-mtu-and-fragmentation-problems
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, vpn-mtu, mtu, mss-clamping, fragmentation, pmtud, vpn]
level: practitioner
status: draft
description: "Spot and fix MTU problems over VPN tunnels: the symptoms, DF-bit ping tests on each OS, interface MTU changes, MSS clamping and why blocked ICMP breaks path MTU discovery."
sources:
  - "https://datatracker.ietf.org/doc/html/rfc4459"
  - "https://datatracker.ietf.org/doc/html/rfc1191"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vpn-mtu-and-fragmentation-problems

## Symptoms
VPN connects, ping works, small pages load, but: large downloads stall, SMB copies hang,
RDP freezes on a full screen, some HTTPS sites never finish loading. Works on one network
(e.g. office) and fails on another (PPPoE broadband, mobile, hotel).

## Find the largest packet that passes
Add 28 bytes (IP + ICMP headers) to the payload size that works to get the path MTU.
| OS | Command |
|---|---|
| Windows | `ping -f -l 1472 server.internal` (lower until it stops saying "Packet needs to be fragmented") |
| Linux | `ping -M do -s 1472 server.internal` |
| macOS | `ping -D -s 1472 server.internal` |

Test inside the tunnel to an internal host, and outside to the VPN gateway.

## Typical overheads
Ethernet 1500; PPPoE 1492; IPsec ESP with NAT-T removes roughly 50-80 bytes; WireGuard
defaults to 1420; SSL VPNs vary. Stacked tunnels (VPN over hotspot over PPPoE) add up.

## Fixes
- Best: the VPN gateway clamps TCP MSS (e.g. to 1360) so endpoints never send oversize
  segments. Raise with the network team when many users hit it.
- Per client (Windows):
```cmd
netsh interface ipv4 show subinterfaces
netsh interface ipv4 set subinterface "VPN Adapter Name" mtu=1400 store=persistent
```
- Vendor clients often have an MTU setting in the gateway profile; change it there rather
  than locally.

## Why it happens
Path MTU discovery depends on ICMP "fragmentation needed" messages getting back. Firewalls
that drop all ICMP create a black hole: big packets vanish silently.

## Gotchas
- UDP apps (video calls) fragment differently and may work while TCP stalls.
- Setting MTU too low costs throughput; find the real value instead of guessing 1200.

## Verify
DF-bit ping at the chosen size passes inside the tunnel, a large file copy and full-screen
RDP session complete, and the change is recorded against the network or profile.
