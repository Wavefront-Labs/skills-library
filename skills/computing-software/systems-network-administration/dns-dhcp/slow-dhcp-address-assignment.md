---
id: computing-software.systems-network-administration.dns-dhcp.slow-dhcp-address-assignment
name: slow-dhcp-address-assignment
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, slow-dhcp, ping-check, conflict-detection, spanning-tree, troubleshooting]
level: practitioner
status: docs-checked
description: "Find why DHCP takes seconds to complete: STP port delays, server ping checks, relay latency, conflict detection, client-side ARP probes and timers."
sources:
  - https://www.rfc-editor.org/rfc/rfc2131
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/set-dhcpserversetting
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#ping-check
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slow address assignment

Measure first: capture on the client port and time Discover -> Offer -> Request -> ACK, then the
client's own probes.

## Where time goes
| Gap | Cause | Fix |
|-----|-------|-----|
| No Discover for many seconds after link up | spanning tree not yet forwarding on the access port | configure the port as an edge/PortFast port |
| Discover repeated, first unanswered | port not forwarding yet, snooping drop, relay ARP | portfast, check relay |
| Discover -> Offer slow | server conflict check before offering | Windows `ConflictDetectionAttempts` (0 to 5, default 0); Kea ping_check hook settings |
| Offer -> ACK slow | server under load, database writes (lease file fsync), HA partner waits | check server CPU/disk, HA latency |
| ACK -> usable | client address conflict detection: RFC 5227 sends 3 probes spaced 1-2 s after an initial wait of up to 1 s, then announces | expected delay of several seconds; very long = conflicts |
| Long delay only on Wi-Fi | 802.1X/roaming before DHCP, broadcast rate issues | check EAP timing |

## Server settings
```powershell
Get-DhcpServerSetting | Select ConflictDetectionAttempts
Set-DhcpServerSetting -ConflictDetectionAttempts 0
```
Kea's `libdhcp_ping_check.so` hook pings a candidate address before offering it. Its `min-ping-requests`
(default 1) sets how many unanswered echo requests are sent, and `ping-cltt-secs` (default 60) how long
after the original lease's client last transaction time a returning client's address is re-checked.
Keep both low if Offers are slow.

## Client side
- A client that remembers a valid lease can go straight to a Request (INIT-REBOOT, RFC 2131), skipping
  Discover and Offer.

## Verify
- [ ] Capture shows Discover within 1 s of link up and DORA completing in under 1 s, with no unanswered Discovers.

## Checked
2026-10-28. Confirmed against the Set-DhcpServerSetting reference (`ConflictDetectionAttempts` 0 through 5, default 0), RFC 5227 constants (PROBE_WAIT 1 s, PROBE_NUM 3, PROBE_MIN 1 s, PROBE_MAX 2 s, ANNOUNCE_WAIT 2 s), the Kea hooks reference (`libdhcp_ping_check.so`, `min-ping-requests` default 1, `ping-cltt-secs` default 60) and RFC 2131 (INIT-REBOOT). Removed as unconfirmed: Cisco IOS ping figures and command, dhclient initial delay, Windows Fast Startup note, 30 s STP figure, Kea `ping-timeout` and version claim.
Method: documentation only; no commands were run.
