---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-shared-networks
name: dhcp4-shared-networks
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, shared-networks, subnets, classification]
level: advanced
status: docs-checked
description: "Group several IPv4 subnets on one physical link with shared-networks in kea-dhcp4: naming, interface rules, inheritance, classes and reservations."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 shared networks
Use shared networks when more than one logical subnet sits on one link, for example a network that has run out of addresses or cable modems and end devices on separate subnets.

- Define under `shared-networks`; each has a unique `name` (used in logs and internally) and a `subnet4` list. Plain subnets can coexist with shared networks.
- Parameters set at shared-network scope apply to all its subnets and can be overridden per subnet (for example `valid-lifetime`, `option-data`).
- Define shared networks only when needed: the extra logic lowers performance. A network with one subnet or none is allowed for testing only.
- All subnets in a shared network must use the same `interface` value (a configuration error otherwise); simplest is to set it once at shared-network level.
- Classes: a subnet with `client-classes` is usable only by clients in at least one of them; a subnet with none is open to all. A common mistake is assuming a classed subnet is preferred. If set on the shared network, clients must be in the class to use any of it.
- Reservations are allowed per subnet; with shared networks defined the server also checks reservations across the sibling subnets.
- When a subnet in a shared network is selected, the whole shared network is selected.

## Checked

2026-11-08. Read dhcp4-srv.rst (Kea ARM source, master branch) sections Shared Networks in DHCPv4 (naming, parameter inheritance, interface and relay rules, classification, reservations) and the subnet-selection note (partial read of the page, those sections in full). Confirmed every claim. Nothing removed.

Method: documentation only; no commands were run.
