---
id: computing-software.systems-network-administration.cisco-networking.ospf-stub-router-max-metric
name: ospf-stub-router-max-metric
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ospf, max-metric, stub-router, router-lsa, maintenance, graceful-drain, rfc6987, r-bit]
level: practitioner
status: docs-checked
description: "How OSPF stub router advertisement (RFC 6987) drains transit traffic before maintenance: MaxLinkMetric 0xffff on non-stub links, what stays reachable, limits."
sources:
  - https://www.rfc-editor.org/rfc/rfc6987
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPF stub router (max-metric) for maintenance

RFC 6987 lets a router tell the OSPF domain not to use it as a transit point while still routing to it. Typical uses:
the router is in critical condition (high CPU, not enough memory for all LSAs or the routing table), graceful
introduction or removal of a router, and administrative or traffic-engineering reasons.

## Mechanism
- Router X sends its router-LSA with the cost of every non-stub link (all link types other than type 3) set to
  MaxLinkMetric, the 16-bit all-ones value 0xffff (65535). Stub links keep their normal cost, so X's own connected
  prefixes stay reachable.
- This differs from flushing X's router-LSA: a flush would also remove the back link neighbours need for Dijkstra, and
  X would have no links to neighbours, so X's prefixes would not be reachable. The adjacency and topology view stay.
- It applies to OSPFv2 and OSPFv3.
- OSPFv3 also has the R-bit: clearing it states the router should not be used for transit, and consistently means no
  transit use, even when the router's path is the only one. MaxLinkMetric still permits the router's path when it is
  the only one available. Operators choose between them by that objective.

## Limits and caveats
- It helps only in networks with redundancy. If the stub router is the only path to a destination, traffic may still
  go through it.
- Mixed networks: routers running the intra-area Dijkstra of RFC 1247 discard link records with MaxLinkMetric, while
  RFC 1583 and later routers do not treat them as unreachable. With alternate paths both agree on avoiding the stub
  router with no loops; if the stub router's path is the only one, the old-style routers avoid it and newer routers
  still use it.
- It affects only OSPF route selection. Other protocols (for example BGP) need their own drain mechanism.

## Operating it
The IOS-XE configuration commands for this feature (including startup-time and wait-for-BGP variants) are not
covered here; the Cisco configuration page this skill formerly cited returned 404, so look them up in the OSPF
configuration guide for your release.

Process advice (judgement): record the undo step in the change plan, watch interface counters fall on the drained
router before starting work, and check neighbours' routing tables show paths avoiding it.

## Checked
Checked 2026-11-08 against RFC 6987 (introduction, section 2 solutions, section 3 MaxLinkMetric, section 4
deployment). Removed: all `max-metric router-lsa` syntax and options, the 600 s wait-for-bgp limit, show commands,
syslog alerting and IS-IS comparison claims, which are not in the RFC.
Method: documentation only; no commands were run.
