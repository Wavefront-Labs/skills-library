---
id: computing-software.networking-hardware-and-wireless.frrouting.static-routes-configuration
name: static-routes-configuration
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, staticd, ip-route, ipv6-route, blackhole, reject, nexthop-vrf, source-specific, srv6]
level: practitioner
status: docs-checked
description: "Configure FRR staticd IPv4 and IPv6 static routes: gateway, interface, blackhole, reject, tag, distance, metric, VRF, source-specific and SRv6 options, and show static routes."
sources:
  - https://docs.frrouting.org/en/latest/static.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static routes configuration
Forms:
- `ip route NETWORK GATEWAY [tag TAG] [DISTANCE] [metric METRIC] [weight WEIGHT] [table TABLENO] [nexthop-vrf VRFNAME] [vrf VRFNAME]`
- `ip route NETWORK IFNAME ...` (interface-only creates a connected route)
- `ip route NETWORK GATEWAY IFNAME ... [onlink]`
- `ip route NETWORK (Null0|blackhole|reject) ...` (no `weight`); blackhole drops silently, `reject` returns ICMP Destination Unreachable.
- `ipv6 route NETWORK [from SRCPREFIX] ...` with the same variants; gateway must be IPv6. `from` makes a source-specific route (Linux only; destination longest-prefix match takes priority).
- SRv6: `ip route A.B.C.D <A.B.C.D|nexthop> segments U::U/Y::Y/Z::Z [encap-behavior H_Encaps|H_Encaps_Red] [encap-source S::S]`; the page says the Linux kernel supports `encap-source` since version 7.1 and that older kernels silently ignore it.
- `ip route NETWORK GATEWAY color COLOR` uses a Zebra-configured SR-TE policy.

Option ranges: TAG 1-4294967295; DISTANCE 1-255, default 1; METRIC 0-4294967295, default 0; WEIGHT 1-65535. `table` works only with namespace-based VRFs; `nexthop-vrf` (leaked route) is not supported with them. `vrf VRFNAME` installs in that VRF, or use `vrf NAME` ... `exit-vrf`.

Keywords `vrf`, `table`, `label`, `tag`, `color`, `segments` and `nexthop-vrf` cannot be interface names.

`show static routes [vrf NAME] [json]` shows staticd's view, not the RIB; inactive reasons include nexthop VRF unknown, no route to nexthop, interface missing or down, BFD session down, or rejected by zebra for a lower-distance route. Use `show ip route` for the RIB.

## Checked

2026-11-08. Read the whole FRR STATIC page: route forms, option ranges and defaults, table and nexthop-vrf limits, reserved keywords, source-specific routes, SRv6 segments, encap-behavior and encap-source, show static routes and inactive reasons. Reworded the encap-source kernel statement to what the page says.
Method: docs-only read of cited pages, 2026-11-08
