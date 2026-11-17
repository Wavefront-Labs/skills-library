---
id: computing-software.systems-network-administration.cisco-networking.local-and-connected-routes
name: local-and-connected-routes
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, routing-table, local-route, connected-route, show-ip-route, cef-receive, secondary-address]
level: practitioner
status: draft
description: "Read connected (C) and local (L) /32 routes in the IOS routing table, how they map to CEF receive entries, and the faults they reveal."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/8651-21.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_pi/configuration/xe-16/iri-xe-16-book.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Local /32 and connected routes

## What you see
```
R1# show ip route connected
      10.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
C        10.1.12.0/30 is directly connected, GigabitEthernet0/0
L        10.1.12.1/32 is directly connected, GigabitEthernet0/0
```
- **C** = the subnet of an interface that is up/up with an address. AD 0.
- **L** (IOS 15+/IOS XE) = the interface's own address as a /32 host route. It lets the router
  identify packets addressed to itself; in CEF it is a `receive` entry.

```
show ip cef 10.1.12.1           ! "receive for GigabitEthernet0/0"
show ip route 10.1.12.1         ! Known via "connected", distance 0, metric 0 (connected, via interface)
```

## What they tell you
- Missing C route: interface is down/down, up/down (keepalive, encapsulation, line protocol), or
  the address is on a shutdown interface. `show ip interface brief`.
- C route present but hosts unreachable: L2 problem (VLAN, trunk, ARP) not routing.
- Secondary addresses (`ip address x y secondary`) produce extra C/L pairs.
- Overlapping subnets on two interfaces are rejected (`% 10.1.12.0 overlaps with GigabitEthernet0/1`)
  unless in different VRFs.
- `ip unnumbered` interfaces have no C route of their own; they borrow the loopback's.

## Redistribution
`redistribute connected` advertises C routes, never L /32s. Use a route-map with
`match interface` to limit which connected subnets leak into an IGP/BGP.
OSPF/EIGRP `network` statements or `ip ospf area` on an interface advertise its C subnet without redistribution.

## IPv6
`show ipv6 route` shows `C` prefixes and `L` /128 entries for each global and the link-local is
not in the RIB (link-local is per-interface).

## Verify
- [ ] Every up/up L3 interface has one C and one L entry.
- [ ] No unexpected secondary subnets (`show run | i secondary`).
