---
id: computing-software.networking-hardware-and-wireless.frrouting.zebra-route-maps-and-source-address
name: zebra-route-maps-and-source-address
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, zebra, ip-protocol-route-map, set-src, route-map-delay-timer, kernel-routes]
level: advanced
status: docs-checked
description: "Filter or modify routes before zebra installs them with ip protocol route-map, set the kernel preferred source address with set src, and tune the route-map delay timer."
sources:
  - https://docs.frrouting.org/en/latest/zebra.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zebra route-maps and source address
`ip protocol PROTOCOL route-map ROUTEMAP` applies a route-map to routes from a protocol before zebra installs them. PROTOCOL: any, babel, bgp, eigrp, isis, nhrp, openfabric, ospf, ospf6, rip, sharp, static, ripng, table, vnc. Can be set per VRF. The IPv6 form is `ipv6 protocol ospf6 route-map RM6`.

`set src ADDRESS` in a route-map sets the preferred source address on installed kernel routes. The address must exist on an interface when the route is installed, or the kernel rejects it.

Documented example:
```
ip prefix-list ANY permit 0.0.0.0/0 le 32
route-map RM1 permit 10
 match ip address prefix-list ANY
 set src 10.0.0.1
ip protocol rip route-map RM1
```

`zebra route-map delay-timer (0-600)` delays route-map processing (default 5 seconds).

The page lists `show ip protocol` among zebra's show commands without describing its output.

## Checked

2026-11-08. Read the FRR zebra page: ip protocol route-map and protocol list, per-VRF use, set src and the interface-address requirement, both examples, delay-timer range and default. Removed the unstated description of show ip protocol output.
Method: docs-only read of cited pages, 2026-11-08
