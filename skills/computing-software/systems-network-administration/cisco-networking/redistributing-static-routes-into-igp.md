---
id: computing-software.systems-network-administration.cisco-networking.redistributing-static-routes-into-igp
name: redistributing-static-routes-into-igp
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, redistribute-static, static-routing, route-redistribution, ospf, eigrp, route-map, metric-type]
level: practitioner
status: draft
description: "Redistribute static routes into OSPF or EIGRP safely: subnets keyword, seed metrics, route-map filtering, tags and the default route special case."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/8606-redist.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/configuration/xe-16/iro-xe-16-book.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Redistributing static routes into an IGP

## OSPF
```
ip prefix-list STATIC-TO-OSPF seq 10 permit 10.80.0.0/16 le 24
route-map STATIC-TO-OSPF permit 10
 match ip address prefix-list STATIC-TO-OSPF
 set metric 20
 set metric-type type-1
 set tag 100
router ospf 1
 redistribute static subnets route-map STATIC-TO-OSPF
```
- Classic IOS needs `subnets` or only classful networks are redistributed (IOS XE 15.x+ assumes
  it on many releases, but write it).
- Default seed metric 20, type E2. Use E1 when there are several exit points and internal cost matters.
- The router becomes an ASBR (type 5 LSAs; type 7 in an NSSA).

## EIGRP
```
router eigrp CORP
 address-family ipv4 unicast autonomous-system 100
  topology base
   redistribute static route-map STATIC-TO-EIGRP
   default-metric 1000000 10 255 1 1500
```
EIGRP needs a seed metric (`default-metric` or `metric` in the route-map) for static routes
pointing to a next hop. Statics pointing only to an interface are treated as connected and
redistributed with that interface's metric.

## Default route
`redistribute static` does **not** advertise 0.0.0.0/0 in OSPF. Use
`default-information originate [always] [route-map]`. EIGRP will redistribute a static default.

## Gotchas
- Always filter. A blanket `redistribute static` advertises every lab and Null0 route.
- Null0 summary statics redistributed into the IGP attract traffic; usually intended, check it.
- Two routers redistributing the same static: the IGP picks by metric; use tags so they do not
  redistribute each other's copies back.
- Floating statics redistribute only while installed in the RIB.

## Verify
```
show ip ospf database external 10.80.0.0
show ip route 10.80.0.0         ! on another router: O E1/E2 or D EX with your tag
show ip eigrp topology 10.80.0.0/16
```
