---
id: computing-software.networking-hardware-and-wireless.frrouting.zebra-interface-configuration
name: zebra-interface-configuration
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, zebra, interface, ip-address, link-detect, bandwidth, link-params, te]
level: practitioner
status: docs-checked
description: "Configure FRR interfaces in zebra: addresses, point-to-point peers, VRF binding, bandwidth, link-detect and the traffic-engineering link-params block."
sources:
  - https://docs.frrouting.org/en/latest/zebra.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zebra interface configuration
Zebra discovers OS objects at startup, then reads its config. The configuration context mirrors `zebra.conf`, so `show running-config` reflects only that file; objects configured outside zebra (for example with iproute2) do not appear, and zebra cannot delete them.

Interface commands: `interface IFNAME [vrf VRF]` (identifies the VRF; does not create it), `shutdown`, `ip address ADDRESS/PREFIX`, `ipv6 address ADDRESS/PREFIX`, `ip address LOCAL-ADDR peer PEER-ADDR/PREFIX` (IPv4 point-to-point; LOCAL-ADDR has no mask), `description`, `mpls <enable|disable>` (Linux only), `multicast <enable|disable>`, `bandwidth (1-1000000)` (Mbit/s, used for OSPF cost only), `link-detect` (enabled by default, Linux only).

Link parameters (`link-params`; TE must be enabled at the OSPF or IS-IS router level; full RSVP-TE is not supported): `metric`, `max-bw`, `max-rsv-bw`, `unrsv-bw (0-7) BANDWIDTH`, `admin-grp 0x(0-FFFFFFFF)`, `affinity AFFINITY-MAP-NAME`, `affinity-mode [extended|standard|both]`, `delay (0-16777215) [min | max]` (microseconds), `delay-variation`, `packet-loss PERCENTAGE`, `res-bw`, `ava-bw`, `use-bw`, `neighbor A.B.C.D as (0-65535)` (OSPF inter-AS). BANDWIDTH is an IEEE float in bytes per second. `affinity` cannot be combined with `admin-grp` on one interface; the default mode is extended (RFC 7308), which is currently IS-IS only.

## Checked

2026-11-08. Read the FRR zebra page: configuration-context behaviour, interface commands, bandwidth and link-detect, link-params and TE parameters, affinity and admin-grp rules. Nothing changed.
Method: docs-only read of cited pages, 2026-11-08
