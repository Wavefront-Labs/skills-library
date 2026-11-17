---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.ip-address-conflicts
name: ip-address-conflicts
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, networking, network-troubleshooting, ip-conflict, duplicate-ip, arp, static-ip, dhcp-reservation, event-4199, comptia-a-plus]
level: intro
status: draft
description: "Find and fix duplicate IP address conflicts: Windows conflict warnings and event 4199, arp -a to find the other MAC, static vs DHCP overlap, reservations, and printer/IoT culprits."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/arp"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/troubleshoot-dhcp-guidance"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ip-address-conflicts

Goal: find the second device using the address and remove the overlap
permanently (A+ 220-1201 5.7: IP conflict).

## Symptoms
- Windows notification "Windows has detected an IP address conflict";
  System log **Event 4199** (Tcpip) naming the conflicting MAC.
- Intermittent connectivity on two devices that "take turns".
- Printer or device going offline when a laptop arrives.

## Find the other device
```cmd
arp -a | findstr 10.1.2.50        :: MAC currently associated with the IP
```
- Event 4199 gives the other device's MAC; look up the vendor (OUI) — HP/
  Brother = printer, Raspberry Pi/IoT, VM hypervisor MAC.
- DHCP server lease table and switch MAC address table (network team) find
  the port.
- `ping -a 10.1.2.50` may return a hostname.

## Causes
| Cause | Fix |
|---|---|
| Static IP set inside the DHCP pool | move static devices outside the pool, or convert to **DHCP reservation** |
| Two devices given the same static address | correct one; keep an IP register |
| Device restored/cloned with static config | reconfigure |
| Rogue DHCP (home router) | remove; enable DHCP snooping |
| Long-offline device returning to a reused lease | DHCP conflict detection setting (server pings before leasing) |

## Fix on the client
Release/renew to get a fresh address (`ipconfig /release` +
`/renew`); set static devices properly; for printers, use the device's
panel or web UI.

## Gotchas
- Fixing the client while the static device remains = it recurs when the
  lease cycles.
- IPv6 duplicate address detection is separate; conflicts are rare there.

## Verify
No new Event 4199 entries, `arp -a` maps the IP to one MAC consistently,
and the reservation/static plan is documented.
