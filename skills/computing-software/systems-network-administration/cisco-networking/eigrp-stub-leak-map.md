---
id: computing-software.systems-network-administration.cisco-networking.eigrp-stub-leak-map
name: eigrp-stub-leak-map
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, eigrp, leak-map, eigrp-stub, route-filtering, distribute-list, dual-homed-branch]
level: practitioner
status: draft
description: "Use EIGRP stub leak-maps to advertise selected learned routes from a stub router, and filter EIGRP routes with distribute-lists and route-maps."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_eigrp/configuration/xe-16/ire-xe-16-book/ire-eigrp-stub-rtg.html
  - https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/200807-EIGRP-Stub-Leak-Map.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EIGRP stub leak-maps and route filtering

## Why leak-maps
A stub router advertises only its own connected/summary routes by default and never learned
routes. In a dual-router branch (R1 and R2 both stub, each with one WAN link), R1 will not tell
the hub about the LAN behind R2 when R2's WAN fails. A leak-map lets a stub advertise chosen
learned routes.

```
ip prefix-list BRANCH-LANS seq 10 permit 10.60.0.0/16 le 24
route-map LEAK permit 10
 match ip address prefix-list BRANCH-LANS
router eigrp CORP
 address-family ipv4 unicast autonomous-system 100
  eigrp stub connected summary leak-map LEAK
```
Leaked routes are still not used as transit by the hub in normal operation because the hub
prefers the direct path; they only matter when it is the only path.

## Filtering EIGRP generally
```
router eigrp CORP
 address-family ipv4 unicast autonomous-system 100
  topology base
   distribute-list prefix DENY-LAB in GigabitEthernet0/0
   distribute-list route-map OUT-FILTER out
```
- Inbound filters stop routes entering the topology table from that neighbour.
- Outbound filters stop advertisement; use summaries (`summary-address` under af-interface) to cut queries.
- Offset-lists adjust metric instead of dropping.

## Gotchas
- Changing stub or distribute-lists resets or re-syncs neighbours on many releases; do it in a window.
- Leaking a default or the hub's routes back defeats the stub's query protection.

## Verify
```
show ip eigrp neighbors detail     ! "Stub Peer Advertising (CONNECTED SUMMARY) Routes"; leak-map shown
show ip route 10.60.2.0            ! on the hub, during an R2 WAN failure
```
