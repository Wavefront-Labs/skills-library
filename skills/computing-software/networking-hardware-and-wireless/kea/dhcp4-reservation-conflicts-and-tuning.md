---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-reservation-conflicts-and-tuning
name: dhcp4-reservation-conflicts-and-tuning
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, reservations-in-subnet, reservations-out-of-pool, reservations-global, conflicts]
level: advanced
status: docs-checked
description: "Resolve DHCPv4 reservation and lease conflicts, and tune the reservations-in-subnet, -out-of-pool and -global checks in kea-dhcp4."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 reservation conflicts and tuning
Conflict: Host A holds 192.0.2.10 from the pool, then the address is reserved for Host B. The server cannot hand it to B at once, since B would detect it in use and send DHCPDECLINE, so B temporarily gets a different pool address. When A renews, the server sends DHCPNAK; A reverts to discovery and gets another address, freeing 192.0.2.10. When B later renews, it too gets DHCPNAK (its temporary lease is kept in case the NAK is lost), then receives its reserved address.

Flags that select which reservation types a subnet allows:
- `reservations-in-subnet`: in-pool reservations; the default, safest and slowest since all checks run. Does not check global reservations.
- `reservations-out-of-pool`: assumes reservations are outside pools and skips in-pool checks. Do not use if any reservation is in-pool; Kea does not sanity-check. Default false.
- `reservations-global`: search global reservations. Default false; not sanity-checked.

Setting all flags to false disables reservation support; any defined reservations are ignored. Precedence runs global (lowest), subnet, shared network, shared-network subnet (highest). Reservations are mutually exclusive: only the highest-priority one applies.

## Checked

2026-11-08. Read dhcp4-srv.rst (Kea ARM source, master branch) sections Conflicts in DHCPv4 Reservations and Fine-Tuning DHCPv4 Host Reservation (partial read, those sections in full). Confirmed the conflict sequence, the three flags with defaults, the all-false case and precedence order. Nothing removed.

Method: documentation only; no commands were run.
