---
id: computing-software.systems-network-administration.cisco-networking.ospf-summarization-area-range
name: ospf-summarization-area-range
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ospf, area-range, ospf-summarization, summary-address, abr, asbr, null0, route-summarization]
level: practitioner
status: draft
description: "Summarise OSPF routes at the ABR with area range and at the ASBR with summary-address, with Null0 discard routes and the not-advertise filtering trick."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/7039-1.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/ospf-a1.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OSPF summarisation

OSPF can only summarise where LSAs are generated: at an **ABR** for inter-area (type 3) and at
an **ASBR** for external (type 5/7) routes. You cannot summarise inside an area.

## Inter-area at the ABR
```
router ospf 1
 area 10 range 10.10.0.0 255.255.0.0          ! one type 3 for area 10's /24s
 area 10 range 10.10.99.0 255.255.255.0 not-advertise   ! hide a prefix from other areas
```
- The summary is advertised only while at least one component route exists in area 10.
- The ABR installs `10.10.0.0/16 is a summary, Null0` (discard route) to stop loops for
  unused space inside the range. Leave it unless it hides a more specific you need.
- Metric of the summary = lowest (classic) or highest (RFC 1583 off) component cost;
  set `area 10 range ... cost 50` for deterministic path choice.

## External at the ASBR
```
router ospf 1
 summary-address 172.16.0.0 255.255.240.0
 redistribute static subnets
```
For an NSSA, summarise on the ABR translating type 7->5 with `summary-address` there too.

## Design rules
- Address each area from a contiguous block so one range covers it; this is the payoff of
  planning (see subnetting skills).
- Summaries hide failures: if a component subnet dies, traffic still follows the summary to
  the ABR and is dropped at Null0. Fine for most, wrong for anycast/active-standby designs.
- Two ABRs advertising the same range give redundancy; mismatched ranges cause asymmetric
  routing.

## Verify
```
show ip ospf summary-address
show ip route 10.10.0.0 255.255.0.0 longer-prefixes   ! on a backbone router: one O IA /16
show ip route | include Null0                         ! on the ABR: discard route present
```
- [ ] Backbone routers see one summary per area; LSDB type-3 count dropped accordingly.
