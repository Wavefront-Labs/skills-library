---
id: computing-software.systems-network-administration.cisco-networking.route-flapping-diagnosis
name: route-flapping-diagnosis
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, route-flapping, route-churn, routing-table, spf, bgp-dampening, ospf-spf, troubleshooting]
level: practitioner
status: draft
description: "Find the source of route churn on IOS: route age, SPF/DUAL/BGP counters, debug with ACL scope, and fixes from carrier-delay to dampening."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/13684-12.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/configuration/xe-16/irg-xe-16-book/configuring-bgp-route-dampening.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Diagnosing route flapping and churn

## Spot it
```
show ip route 10.20.0.0           ! "Last update from 10.0.0.2 00:00:12 ago" keeps resetting
show ip route | include 00:00:    ! routes younger than a minute
show ip route summary             ! compare over time
show ip cef switching statistics  ! CEF adjacency churn on some platforms
```

## Per protocol
| Protocol | Counter | Command |
|---|---|---|
| OSPF | SPF runs and LSA changes | `show ip ospf statistics`, `show ip ospf | i SPF`, `show ip ospf database database-summary` (LSA ages near 0) |
| EIGRP | queries/SIA, neighbour resets | `show ip eigrp neighbors` (Uptime, Q Cnt), `show ip eigrp events` |
| BGP | prefix withdrawals | `show ip bgp neighbors x | i Prefixes|flap`, `show ip bgp flap-statistics` |

OSPF: find the LSA that keeps changing:
```
show ip ospf database router | include Advertising|LS age|Seq
show ip ospf database router adv-router 10.255.0.7     ! sequence number climbing fast = source
```

## Scoped debugging
```
access-list 99 permit 10.20.0.0 0.0.255.255
debug ip routing 99          ! only RIB changes for that prefix
terminal monitor
```

## Typical causes and fixes
- Physical flap (dirty optic, bad cable): `show interfaces | i reset|carrier`, logs `%LINK-3-UPDOWN`.
  Fix the layer 1 issue; `carrier-delay msec 0`/`dampening` on the interface to stop propagation.
- Neighbour flaps from timers/MTU/unidirectional link: BFD + UDLD; match MTU.
- Redistribution loops (mutual redistribution): routes alternate between protocols; tag and filter.
- Duplicate router IDs in OSPF: constant LSA re-origination, log `%OSPF-4-DUP_RTRID_NBR`.
- Recursive-routing loops on tunnels (`%TUN-5-RECURDOWN`): tunnel destination learned via the tunnel.
- BGP: `bgp dampening` on eBGP edges for unstable customer routes (not on iBGP/RR).
- OSPF: SPF throttle (`timers throttle spf 50 200 5000`) to limit CPU impact while you fix the cause.

## Verify
- [ ] Route age keeps increasing over 15+ minutes.
- [ ] SPF/withdraw counters flat.
