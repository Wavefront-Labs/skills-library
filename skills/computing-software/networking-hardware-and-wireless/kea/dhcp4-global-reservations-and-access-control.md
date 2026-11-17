---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-global-reservations-and-access-control
name: dhcp4-global-reservations-and-access-control
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, global-reservations, known-class, access-control]
level: advanced
status: docs-checked
description: "Use global reservations for roaming clients, and empty reservations to put hosts in the KNOWN class for basic access control in kea-dhcp4."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 global reservations and KNOWN-class access control
Global reservations sit at the top level and are used in every subnet that enables them with `reservations-global`. Useful for roaming clients (mobile networks) needing a hostname or options wherever they are. An address from a global reservation must be feasible for the selected subnet; otherwise it is ignored and an address is allocated dynamically. In a shared network the first in-range sibling subnet is used. Before release 2.3.5 this check was not performed.

Access control: a reservation containing only an identifier makes the host belong to the built-in KNOWN class; others do not. In the docs example a class named KNOWN carries the `routers` option, global reservations list only MAC addresses, and `reservations-global` is true, so only known clients get a default router while everyone still gets an address.

```json
"client-classes": [ { "name": "KNOWN", "option-data": [
  { "name": "routers", "data": "192.0.2.250" } ] } ],
"reservations": [ { "hw-address": "aa:bb:cc:dd:ee:fe" } ],
"reservations-global": true
```

## Checked

2026-11-08. Read dhcp4-srv.rst (Kea ARM source, master branch) sections Global Reservations in DHCPv4 and Host Reservations as Basic Access Control (partial read, those sections in full). Confirmed feasibility check, the Kea 2.3.5 note, shared-network sibling rule, KNOWN class example. Nothing removed.

Method: documentation only; no commands were run.
