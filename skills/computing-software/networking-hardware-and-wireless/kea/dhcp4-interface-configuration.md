---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-interface-configuration
name: dhcp4-interface-configuration
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, interfaces-config, raw-sockets, listening]
level: practitioner
status: docs-checked
description: "Choose the interfaces and addresses kea-dhcp4 listens on with interfaces-config, plus the raw socket trade-off."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 interface configuration
kea-dhcp4 must be told which interfaces to listen on, under `Dhcp4/interfaces-config/interfaces`.

- `[ "*" ]` listens on all interfaces; the docs say it is usually better to list names, e.g. `[ "eth1", "eth3" ]`.
- Mixing `*` with names is meant only to temporarily override the list and listen everywhere.
- Append an address to pick one on a multi-address interface: `"eth1/10.0.0.1"`. Several addresses on one interface are separate entries (`eth1/10.0.0.1`, `eth1/10.0.0.2`). A bare interface name listens on all its addresses.

To answer directly connected clients that have no address yet, the server injects the client hardware address at the link layer, using raw sockets and building the IP/UDP stack itself. The downside the docs name: incoming and outgoing packets bypass firewalls such as iptables.

## Checked

2026-11-08. Read dhcp4-srv.rst (Kea ARM source, master branch) sections Interface Configuration in full (wildcard, names, address forms, raw versus UDP sockets). Confirmed every claim. Nothing removed.

Method: documentation only; no commands were run.
