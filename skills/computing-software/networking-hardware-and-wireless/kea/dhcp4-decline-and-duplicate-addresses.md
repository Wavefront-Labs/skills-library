---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-decline-and-duplicate-addresses
name: dhcp4-decline-and-duplicate-addresses
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, dhcpdecline, decline-probation-period, declined-addresses]
level: practitioner
status: docs-checked
description: "How kea-dhcp4 handles DHCPDECLINE for duplicate addresses: probation period, statistics, hook point and recovery."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 DHCPDECLINE handling
A client that detects (by ARP or ICMP Echo) that an offered address is already in use sends DHCPDECLINE. The server checks the client was entitled to the address, then cleans up: related DNS entries are removed, the event is logged and hooks fire. The address is marked declined (used by an unknown entity, so not assignable) with a probation time. The default probation is 24 hours; afterwards the lease is recovered and can be assigned again. If the misconfigured device is not fixed, the cycle repeats.

Change the probation (seconds) at global level:

```json
"Dhcp4": { "decline-probation-period": 3600 }
```

Related items:
- Hook point `lease4_decline` is triggered once the DHCPDECLINE has been sanitized and the server is about to decline the lease.
- The `declined-addresses` statistic (global and per subnet) is increased after the hook returns.
- `assigned-addresses` is deliberately not decreased on DHCPDECLINE, so utilization (assigned over total) is not under-reported; it is decreased when the address is recovered.
- After probation the lease is recovered through standard expired-lease reclamation, with the `declined-addresses` statistics decreased and `reclaimed-declined-addresses` statistics updated.

## Checked

2026-11-08. Read dhcp4-srv.rst (Kea ARM source, master branch) sections Duplicate Addresses (DHCPDECLINE Support) in full. Confirmed the 24 hour default probation, decline-probation-period in seconds, lease4_decline, and the declined-addresses, reclaimed-declined-addresses and assigned-addresses statistics behaviour. Nothing removed.

Method: documentation only; no commands were run.
