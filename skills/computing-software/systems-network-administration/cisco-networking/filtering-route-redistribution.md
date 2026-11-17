---
id: computing-software.systems-network-administration.cisco-networking.filtering-route-redistribution
name: filtering-route-redistribution
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, redistribution-filtering, route-redistribution, route-map, prefix-list, distribute-list-out, route-tag]
level: practitioner
status: draft
description: "Filter what gets redistributed between IGPs and BGP with route-maps, prefix-lists, tags and distribute-list out, and verify nothing leaks."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/8606-redist.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_pi/configuration/xe-16/iri-xe-16-book/iri-route-map.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Filtering redistribution

## Always use a route-map on redistribute
```
ip prefix-list EIGRP-TO-OSPF seq 10 permit 10.60.0.0/16 le 24
ip prefix-list EIGRP-TO-OSPF seq 20 permit 10.61.0.0/16 le 24
route-map EIGRP-TO-OSPF deny 5
 match tag 110                     ! came from OSPF originally; never send it back
route-map EIGRP-TO-OSPF permit 10
 match ip address prefix-list EIGRP-TO-OSPF
 set tag 90
router ospf 1
 redistribute eigrp 100 subnets route-map EIGRP-TO-OSPF
```
Anything not permitted by the route-map is not redistributed (implicit deny).

## Tools and where they act
| Tool | Effect |
|---|---|
| route-map on `redistribute` | selects/marks routes entering the protocol (best place) |
| `distribute-list ... out <protocol>` under OSPF | filters which redistributed routes from that protocol become type-5 LSAs |
| `distribute-list in` under OSPF | filters RIB install only; LSAs still flood |
| `summary-address` (OSPF ASBR) | aggregates externals; `not-advertise` suppresses a range |
| BGP: prefix-lists on `redistribute`/`network` | keep RFC 1918/IGP infrastructure out of eBGP |

## Match options
`match ip address prefix-list`, `match tag`, `match interface` (connected), `match route-type
external type-2`, `match metric`, `match source-protocol` (IOS XE).

## Gotchas
- Prefix-lists over ACLs: ACLs ignore mask length.
- Redistribute connected without a route-map leaks transit links and loopbacks you did not mean to.
- BGP into IGP without a filter = full table in your IGP. Always filter and set `maximum-prefix`.

## Verify
```
show ip ospf database external | include Link State ID
show route-map EIGRP-TO-OSPF        ! review sequences and match clauses
show ip route | include E2|EX
```
- [ ] Only intended prefixes appear as externals on a router far from the ASBR.
