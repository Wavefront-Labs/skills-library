---
id: computing-software.systems-network-administration.dns-dhcp.dhcp-lease-lifecycle-and-t1-t2-timers
name: dhcp-lease-lifecycle-and-t1-t2-timers
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, lease-renewal, t1-t2, lease-time, rebinding, dhcpv6, renew-timer, rebind-timer]
level: practitioner
status: verified
description: "Choose DHCP lease times and understand renewal: T1 renew (50%), T2 rebind (87.5%), expiry behaviour, DHCPv6 equivalents, and tuning Kea and Windows per network type."
sources:
  - https://www.rfc-editor.org/rfc/rfc2131
  - https://www.rfc-editor.org/rfc/rfc8415
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
  - https://www.rfc-editor.org/rfc/rfc9915
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCP lease lifecycle and T1/T2

## The lifecycle (RFC 2131)
1. **BOUND** after DORA, with lease time L.
2. **T1 (default 0.5 L) -> RENEWING:** client unicasts DHCPREQUEST to the server that
   granted the lease. ACK resets the clock.
3. **T2 (default 0.875 L) -> REBINDING:** no answer from the original server; client
   **broadcasts** DHCPREQUEST to any server (failover partner, another server).
4. **Expiry:** client must stop using the address and restart DISCOVER. Active connections drop.
Servers can send explicit option 58 (T1) and 59 (T2).

DHCPv6 (RFC 9915, which obsoletes RFC 8415): T1/T2 per IA in Reply; Renew to the same server, Rebind to all; addresses
have preferred/valid lifetimes.

## Choosing lease times
| Network | Lease | Why |
|---|---|---|
| Guest Wi-Fi, events | 1-4 h | many transient clients, small pools |
| Corporate wired/Wi-Fi | 8 h - 1 day | covers a working day; pool sized for devices + churn |
| Servers / infra with reservations | days | rarely changes |
| Renumbering coming | shorten to 1 h a few days before | clients move quickly |

Short leases increase DHCP load and the number of DDNS updates; long leases with a small
pool exhaust it with departed devices.

## Server settings
Kea:
```json
"valid-lifetime": 28800, "renew-timer": 14400, "rebind-timer": 25200
```
Kea does not send T1/T2 by default (clients then use the RFC 2131 defaults). Send fixed values with
`renew-timer` and `rebind-timer` (as above: 50 % and 87.5 % of 28800 s), or set
`"calculate-tee-times": true` (default false) to derive them from `t1-percent` (default 0.50) and
`t2-percent` (default 0.875). If explicit values are also configured they win, and inheriting them
from the global scope disables the calculation for every subnet below it (Kea ARM).

## Diagnose
- Clients losing addresses at ~T2/expiry: server unreachable by unicast (firewall blocks UDP 67
  from clients to server across routers), so only broadcast rebinding to the relay works.
- Capture: `dhcp.option.dhcp == 3` (REQUEST) with a non-zero `dhcp.ip.client` (ciaddr) = renew/rebind; time
  between them shows T1/T2 (the old `bootp.*` field names do not exist in Wireshark 4.4).

## Verify
- [ ] Leases renew at T1 by unicast (seen in server logs/capture); pool utilisation stays below ~80% at peak.
