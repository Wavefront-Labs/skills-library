---
id: computing-software.systems-network-administration.cisco-networking.ipv6-static-routes
name: ipv6-static-routes
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ipv6, static-route, static-routing, ipv6-static-route, ipv6-route, link-local, ipv6-default-route, ipv6-unicast-routing, floating-static-route]
level: practitioner
status: draft
description: "Configure IPv6 static routes on IOS: global vs link-local next hops (interface required), default ::/0, floating backups and the ipv6 unicast-routing prerequisite."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_pi/configuration/xe-16/iri-xe-16-book/ip6-route-static-xe.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IPv6 static routes

## Prerequisite
```
ipv6 unicast-routing        ! without it the router is an IPv6 host: no forwarding, no RAs
```

## Forms
```
ipv6 route ::/0 2001:db8:ffff::1                               ! default via global next hop
ipv6 route 2001:db8:60::/48 GigabitEthernet0/1 FE80::2          ! link-local next hop: interface required
ipv6 route 2001:db8:60:5::10/128 GigabitEthernet0/1 FE80::2     ! host route
ipv6 route 2001:db8::/32 Null0                                  ! summary sink
ipv6 route ::/0 2001:db8:eeee::1 200                            ! floating backup (AD 200)
```
Link-local next hops are only unique per link, so IOS **requires the exit interface** with them;
`ipv6 route ::/0 FE80::2` alone is rejected.

## Why link-local next hops
Routing protocols (OSPFv3, EIGRPv6, BGP over link-local) use link-local next hops; using them
in statics survives global renumbering of the link. Make them predictable:
```
interface GigabitEthernet0/1
 ipv6 address FE80::1 link-local
 ipv6 address 2001:db8:ffff::2/64
```

## Checks
```
show ipv6 route static
show ipv6 route 2001:db8:60:5::10
show ipv6 neighbors GigabitEthernet0/1       ! next hop resolved (REACH/STALE)
ping 2001:db8:60:5::10 source GigabitEthernet0/2
traceroute ipv6 2001:db8:60:5::10
```

## Gotchas
- Exit-interface-only on Ethernet (`ipv6 route ::/0 Gi0/1`) relies on the destination being
  on-link: traffic fails unless the upstream answers ND for every destination.
- Tracking works the same as IPv4: `ipv6 route ::/0 2001:db8:ffff::1 track 10` with an IP SLA
  `icmp-echo` IPv6 target.
- ICMPv6 must not be blanket-filtered (ND, PMTUD); IPv6 ACLs include implicit ND permits only
  before the final deny.

## Verify
- [ ] `show ipv6 route ::/0` points at the intended next hop and interface.
- [ ] Neighbour entry for the next hop is REACH/STALE, not INCMP.
- [ ] Pings to remote prefixes succeed from a LAN-sourced interface.
