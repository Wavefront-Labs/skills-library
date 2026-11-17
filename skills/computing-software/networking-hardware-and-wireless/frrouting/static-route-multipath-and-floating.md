---
id: computing-software.networking-hardware-and-wireless.frrouting.static-route-multipath-and-floating
name: static-route-multipath-and-floating
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, staticd, ecmp, floating-static, backup-route, bfd, weight]
level: practitioner
status: docs-checked
description: "Build ECMP and floating backup static routes in FRR staticd by reusing the prefix with different nexthops, distance and metric, and remove or tie them to BFD."
sources:
  - https://docs.frrouting.org/en/latest/static.html
  - https://docs.frrouting.org/en/latest/bfd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static route multipath and floating
- ECMP: enter the same NETWORK again with different nexthops. Nexthops sharing the same (distance, metric) form one ECMP path group.
- Floating: nexthops with different (distance, metric) form separate groups. Only the best group (lowest distance, then lowest metric) is selected; others are promoted when it fails.
- Reconfiguring a nexthop with a new distance or metric moves it out of its old group. A nexthop appears in at most one group per prefix.
- Tags are per path group; if nexthops in one group have different tags the RIB uses the maximum.
- `weight` (1-65535) sets multipath traffic share. The kernel supports 8-bit weights for multipath static routes; zebra uses nexthop groups, which support 16-bit weights on kernel 6.12+.
- `no ip route NETWORK NEXTHOP` removes by nexthop identity (gateway, interface or blackhole type); distance and metric arguments are ignored.

BFD-tracked statics (from the BFD page): `ip route A.B.C.D/M A.B.C.D bfd [multi-hop|source A.B.C.D|profile BFDPROF]` and `ipv6 route X:X::X:X/M [from X:X::X:X/M] X:X::X:X bfd [multi-hop|source X:X::X:X|profile BFDPROF]`. The route is installed in the RIB only while the session is up. `show bfd static route [json]` lists monitored routes; uninstalled monitored routes no longer appear in `show ip route`.

## Checked

2026-11-08. Read the FRR STATIC page (path groups by distance and metric, ECMP, floating, nexthop uniqueness, tag maximum, weight, removal by nexthop identity) and the BFD page (monitored static routes). Removed the unstated claim about default weight in show output.
Method: docs-only read of cited pages, 2026-11-08
