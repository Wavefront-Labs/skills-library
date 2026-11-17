---
id: computing-software.networking-hardware-and-wireless.frrouting.zebra-rib-show-commands
name: zebra-rib-show-commands
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, zebra, show-ip-route, rib, router-id, vrf, json-brief, debug-zebra]
level: practitioner
status: docs-checked
description: "Inspect the FRR zebra RIB: show ip route filters, failed installs, VRF and table views, interface and neighbor tables, router-id commands and zebra debug options."
sources:
  - https://docs.frrouting.org/en/latest/zebra.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zebra RIB show commands
`show [ip|ipv6] route [vrf NAME|all|table TABLENO] [A.B.C.D|A.B.C.D/M|X:X::X:X|X:X::X:X/M] [nexthop-group [summary [ecmp-count <gt|lt|eq> (1-256)]]] [failed] [json [brief]]`
- `failed` shows only routes that failed kernel installation.
- `json brief` gives minimal fields per route; `vrf all json brief` keys by VRF name.
- `show [ip|ipv6] route summary [vrf VRF] [table TABLENO] [prefix]`; counts can exceed FIB totals.
- `show ip route vrf VRF tables` lists tables; `table TABLENO` works only with `-w`.

Other views: `show interface [NAME] [{vrf VRF|brief}] [json]`, `show ip neighbor`, `show ipv6 neighbor`, `show neighbor` (both), `show pbr rule`, `show zebra`, `show zebra client [summary|json]`, `show zebra router table summary`.

Router ID: `[ip] router-id A.B.C.D` (per-VRF allowed in the VRF subnode; the `vrf NAME` suffix form is deprecated), `ipv6 router-id X:X::X:X`, `show [ip] router-id [vrf NAME]`, `show ipv6 router-id [vrf NAME]`.

VRF: `vrf VRF` enters VRF configuration; zebra does not create Linux VRFs. The default backend is Linux VRF (table-based) and needs a default blackhole route with high metric in the VRF table; `-w` maps a network namespace to a VRF.

Debug: `debug zebra events|kernel|rib [detailed]|nht [detailed]|dplane [detailed]|mpls [detailed]|nexthop [detail]|packet [<recv|send>] [detail]`.

## Checked

2026-11-08. Read the FRR zebra page: show route forms and options, failed and json brief, summary, VRF backends and table views, interface and neighbor show commands, router-id commands, debug commands. Nothing changed.
Method: docs-only read of cited pages, 2026-11-08
