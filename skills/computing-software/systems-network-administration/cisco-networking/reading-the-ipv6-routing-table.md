---
id: computing-software.systems-network-administration.cisco-networking.reading-the-ipv6-routing-table
name: reading-the-ipv6-routing-table
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ipv6, show-ipv6-route, ipv6-routing-table, link-local-next-hop, ipv6-cef, ospfv3]
level: practitioner
status: draft
description: "Read show ipv6 route output on IOS: route codes, link-local next hops with exit interfaces, local /128s, ND-learned and default routes, plus CEF checks."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipv6/command/ipv6-cr-book/ipv6-s4.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipv6_basic/configuration/xe-16/ip6b-xe-16-book.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading the IPv6 routing table

## Example
```
R1# show ipv6 route
IPv6 Routing Table - default - 9 entries
Codes: C - Connected, L - Local, S - Static, U - Per-user Static route, O - OSPF Intra,
       OI - OSPF Inter, OE2 - OSPF ext 2, D - EIGRP, B - BGP, ND - ND Default, NDp - ND Prefix ...
S   ::/0 [1/0]
     via 2001:DB8:0:12::2
C   2001:DB8:0:12::/64 [0/0]
     via GigabitEthernet0/0, directly connected
L   2001:DB8:0:12::1/128 [0/0]
     via GigabitEthernet0/0, receive
O   2001:DB8:10::/64 [110/2]
     via FE80::2, GigabitEthernet0/0
L   FF00::/8 [0/0]
     via Null0, receive
```

## Points that trip people
- **Dynamic routes use link-local next hops** (`FE80::2, Gi0/0`). The interface is part of the
  next hop because link-locals are not unique across links.
- A static route to a link-local next hop must name the interface:
  `ipv6 route 2001:DB8:99::/48 Gi0/0 FE80::2`.
- `L` /128 per global address, plus `FF00::/8 via Null0` (multicast receive) by default.
- `ND`/`NDp` entries appear when the router itself learned a default route or prefix from RAs
  (`ipv6 address autoconfig default`).
- `ipv6 unicast-routing` must be on, or the box acts as a host (no routing, no RAs sent).
- Link-local addresses never appear as C/L entries.

## Useful commands
```
show ipv6 route summary
show ipv6 route 2001:DB8:10::5             ! longest match for one destination
show ipv6 cef 2001:DB8:10::5 detail
show ipv6 neighbors Gi0/0                   ! next-hop resolution (REACH/STALE/INCMP)
show ipv6 interface brief
```

## Verify
- [ ] Default route present (static or ND) and its next-hop neighbour in REACH/STALE.
- [ ] `show ipv6 cef <dest>` matches the RIB next hop.
