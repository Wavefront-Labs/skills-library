---
id: computing-software.systems-network-administration.network-design.spine-leaf-and-oversubscription
name: spine-leaf-and-oversubscription
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-topology, spine-leaf, clos, oversubscription, oversubscription-ratio, ecmp, east-west-traffic, leaf-uplinks, data-center-design, border-leaf, super-spine]
level: practitioner
status: verified
description: "Design a spine-leaf fabric and size it: oversubscription ratio maths, leaf/spine port counts, ECMP behaviour, border leaves, when to add a super-spine and campus uplink ratios."
sources:
  - https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/white-paper-c11-737022.html
  - https://datatracker.ietf.org/doc/html/rfc7938
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spine-leaf and oversubscription

## The topology
Every leaf connects to every spine; spines never connect to each other; leaves never connect to
each other (except MLAG peer links). Any server-to-server path is leaf-spine-leaf: equal hops,
predictable latency, scale by adding leaves (ports) or spines (bandwidth).
Underlay is routed (eBGP per RFC 7938, "Use of BGP for Routing in Large-Scale Data Centers", or OSPF/IS-IS) with ECMP across all spines; overlay
usually VXLAN EVPN (see vxlan-evpn-fabric-basics).

## Oversubscription ratio
Ratio = total downlink (server-facing) bandwidth / total uplink bandwidth on a switch.
Example leaf: 48 x 25G down = 1200G; 6 x 100G up = 600G -> **2:1** (recomputed). The DC targets in the table are common design practice, not a standard.
| Environment | Typical target |
|---|---|
| Storage, HPC/AI training | 1:1 (non-blocking) |
| General virtualised DC | 2:1 - 3:1 |
Campus tiers are normally oversubscribed more heavily than data-centre fabrics; set the target from measured peak utilisation rather than a quoted ratio.
Oversubscription only hurts when hosts actually send at once; measure peak utilisation and
microbursts before buying.

## Sizing
- Max leaves = ports per spine (one link per leaf per spine). 32-port 400G spines -> 32 leaves
  (fewer if border leaves/links consume ports).
- Spines = uplinks per leaf (one per spine) or half if using 2 links per spine.
- Need more leaves than one spine's ports? Add a **super-spine** tier (5-stage Clos) or use
  larger spines (chassis).
- Border leaves connect WAN/firewalls/internet; service leaves for load balancers; keep spines
  pure transit.

## ECMP realities
- Flows hash to one spine; elephant flows can collide on one uplink while others idle. Use more,
  smaller links or flowlet/adaptive load balancing where supported.
- Losing a spine removes 1/N of capacity: with 4 spines, 25%; design the ratio so N-1 still works.
- Uniform link speeds and counts keep ECMP even; mixed speeds need weighted ECMP.

## Verify
- [ ] Documented ratio per tier and the failure-case ratio (one spine down).
- [ ] Every leaf has equal-cost routes via all spines (the route table lists N next hops for each remote prefix).
- [ ] Port count plan leaves room for growth in leaves and spines.
