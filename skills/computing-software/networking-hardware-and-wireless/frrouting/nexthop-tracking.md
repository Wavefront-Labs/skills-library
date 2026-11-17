---
id: computing-software.networking-hardware-and-wireless.frrouting.nexthop-tracking
name: nexthop-tracking
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, zebra, nht, nexthop-tracking, resolve-via-default, pbr-nexthop-resolve]
level: advanced
status: docs-checked
description: "Control FRR nexthop tracking: resolve-via-default per VRF, view NHT state and route-map attachments, and resolve PBR nexthops to MAC and interface."
sources:
  - https://docs.frrouting.org/en/latest/zebra.html
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nexthop tracking
- `ip nht resolve-via-default` allows IPv4 nexthop resolution via the default route; `ipv6 nht resolve-via-default` is the IPv6 equivalent. Per VRF (use the VRF subnode); enabled by default for the traditional profile.
- `show ip nht [vrf NAME] [A.B.C.D|X:X::X:X] [mrib] [json]` shows NHT status; `vrf all` covers all VRFs; `mrib` shows multicast RIB resolution. `show ip import-check` is a deprecated alias.
- `show ip nht route-map [vrf <NAME|all>] [json]` shows the route-map attached for NHT notifications per protocol.
- `pbr nexthop-resolve` resolves PBR nexthops to SMAC, DMAC and outgoing interface via neighbor tracking; needed by some dataplanes (DPDK PBR flows also need it).
- BGP: if a peer is reached via the default route and not in the RIB, `neighbor PEER ebgp-multihop` also needs `ip nht resolve-via-default`.
- Debug: `debug zebra nht [detailed]`, `debug bgp nht`.

BGP-side views: `show bgp nexthop detail`, `show [ip] bgp nexthop [A.B.C.D|X:X::X:X] [detail] [json]` and `show [ip] bgp import-check-table [detail] [json]` (table used for network-statement existence checks).

## Checked

2026-11-08. Read the FRR zebra page (resolve-via-default, show ip nht and route-map forms, pbr nexthop-resolve, DPDK note, debug) and the BGP page (ebgp-multihop with resolve-via-default, show bgp nexthop, import-check-table, debug bgp nht). Nothing changed.
Method: docs-only read of cited pages, 2026-11-08
