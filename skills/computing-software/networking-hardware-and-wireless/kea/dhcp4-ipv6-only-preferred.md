---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-ipv6-only-preferred
name: dhcp4-ipv6-only-preferred
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, v6-only-preferred, rfc-8925, ipv6-only]
level: practitioner
status: docs-checked
description: "Signal IPv6-only preferred support (RFC 8925) from kea-dhcp4 with the v6-only-preferred option and its V6ONLY_WAIT value."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 IPv6-only preferred networks
RFC 8925 defines a DHCPv4 option telling compatible dual-stack hosts that the network offers IPv6 connectivity so they may forgo an IPv4 address and shut down their IPv4 stack.

In Kea this is the `v6-only-preferred` option. Its content is a 32-bit unsigned integer: how long, in seconds, the device should disable its IPv4 stack. This implements the RFC's V6ONLY_WAIT timer.

Set it like any option; it is returned only if the client requests option 108 in its parameter request list. When it is configured in a subnet or shared network and the client requests it, the server offers the address 0.0.0.0 and returns the option. The value can be specified at pool, subnet, shared-network or global level, or via host reservations, following the usual option inheritance.

## Checked

2026-11-08. Read dhcp4-srv.rst (Kea ARM source, master branch) sections IPv6-Only Preferred Networks and Support for IPv6-Only Preferred Option (partial read, those sections in full). Confirmed the 32-bit seconds value, the V6ONLY_WAIT mapping and option levels. Corrected: the draft said there is no special processing, but the docs say that when the option is configured in a subnet or shared network and the client requests it, the server offers 0.0.0.0 and returns the option; also added that the option is sent only when requested.

Method: documentation only; no commands were run.
