---
id: computing-software.systems-network-administration.cisco-networking.route-redistribution-with-tags
name: route-redistribution-with-tags
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, path-control, redistribution, route-redistribution, mutual-redistribution, route-tag, seed-metric, route-map, redistribute-ospf, redistribute-eigrp, redistribute-connected, routing-loop, distribute-list, two-point-redistribution]
level: advanced
status: draft
description: "Redistribute between OSPF, EIGRP, BGP and statics without loops: seed metrics, route-maps, tagging at each boundary and denying tagged routes back, plus verification."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/8606-redist.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_pi/configuration/xe-16/iri-xe-16-book/iri-ip-route-redist.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route redistribution with tags

## Seed metrics (otherwise routes are not advertised or get odd metrics)
| Into | Default seed | Set explicitly |
|---|---|---|
| OSPF | 20 (E2), 1 for BGP | `metric 20 metric-type 1` (E1 adds internal cost) |
| EIGRP | infinity (not advertised) except from another EIGRP AS/connected/static | `metric 10000 100 255 1 1500` (bw, delay, rel, load, mtu) or `default-metric` |
| BGP | IGP metric copied to MED | `route-map` set MED/local-pref |

Redistributing OSPF into anything does **not** include connected subnets of OSPF interfaces
unless they are OSPF routes on that router; add `redistribute connected` with a route-map if needed.

## Mutual redistribution at two points: the loop
With two routers both redistributing OSPF <-> EIGRP, a route from OSPF goes into EIGRP at R1,
comes back into OSPF at R2 as external, and may be preferred (AD/metric) over the original,
creating suboptimal paths or loops. Tag and filter:
```
route-map EIGRP-TO-OSPF deny 10
 match tag 110                     ! came from OSPF originally, don't send it back
route-map EIGRP-TO-OSPF permit 20
 set tag 90
!
route-map OSPF-TO-EIGRP deny 10
 match tag 90
route-map OSPF-TO-EIGRP permit 20
 set tag 110
!
router ospf 1
 redistribute eigrp 100 subnets route-map EIGRP-TO-OSPF
router eigrp 100
 redistribute ospf 1 metric 10000 100 255 1 1500 route-map OSPF-TO-EIGRP
```
Apply the same route-maps on both boundary routers. Tags survive across both protocols.

## Also consider
- Raise AD of external routes so the native protocol wins: `distance ospf external 175` or EIGRP
  external is already 170.
- Filter what you redistribute with prefix-lists (`match ip address prefix-list`) rather than
  redistributing everything; never redistribute a full BGP table into an IGP.
- `distribute-list prefix X in|out` filters what a router installs/advertises (OSPF only filters
  RIB installation inbound, not LSAs).

## Verify
```
show ip route 10.60.0.0 255.255.0.0     ! "Route tag 90", source protocol
show ip ospf database external | i Link State ID|Tag
show ip eigrp topology 10.60.0.0/16     ! external data: originating protocol, tag
show route-map EIGRP-TO-OSPF            ! policy routing matches counts
```
- [ ] No prefix appears as external in its home protocol on the boundary routers.
- [ ] Failing one boundary router leaves reachability via the other with no loops (traceroute).
