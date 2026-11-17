---
id: computing-software.systems-network-administration.cisco-networking.ospf-network-types
name: ospf-network-types
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ospf, ospf-network-type, ospf-point-to-point, broadcast, non-broadcast, point-to-multipoint, hello-timer, dead-interval, rfc2328]
level: practitioner
status: docs-checked
description: "OSPF network types per RFC 2328 and Cisco's interface doc: DR election, adjacency rules, hello/dead timers, neighbour discovery, ip ospf network, and mismatches."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/13689-17.html
  - https://www.rfc-editor.org/rfc/rfc2328
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPF network types

The network type decides whether a Designated Router is elected, how neighbours are discovered and which adjacencies
form. RFC 2328 defines point-to-point, broadcast, NBMA, Point-to-MultiPoint and virtual-link networks; over a
non-broadcast network OSPF runs in one of two modes, NBMA (simulates a broadcast network) or Point-to-MultiPoint
(treats it as a collection of point-to-point links).

| Type | DR/BDR | Adjacencies (RFC 2328 10.4) | Neighbour discovery |
|---|---|---|---|
| broadcast | elected | every router with the DR and BDR | Hello packets multicast; dynamic discovery |
| point-to-point | none | always adjacent | Hello; a received Network Mask is ignored |
| NBMA | elected | every router with the DR and BDR | configured list of neighbours; Hellos sent to each eligible router in turn |
| Point-to-MultiPoint | none (DR eligibility undefined) | always adjacent | Hellos to directly reachable neighbours, found by e.g. Inverse ARP or configured |

- Multicast addresses: AllSPFRouters 224.0.0.5 (all OSPF routers; Hello packets always use it where multicast is
  available) and AllDRouters 224.0.0.6 (DR and BDR only). OSPF is IP protocol 89.
- Router priority matters only on broadcast and NBMA networks; priority 0 makes a router ineligible to be DR.
- NBMA: a PollInterval (RFC sample 2 minutes, much larger than HelloInterval) governs Hellos to a dead neighbour.
- In its router-LSA, a P2MP interface contributes a /32 stub link to the router's own address (cost 0) plus one
  point-to-point link per fully adjacent neighbour (RFC 12.4.1.4). Hence the /32 host routes seen on P2MP.

## Timers
RFC 2328 says HelloInterval and RouterDeadInterval must be identical for all routers on a common network, with the dead
interval some multiple of Hello (say 4). The RFC's sample HelloInterval is 10 s on a LAN and 30 s on an X.25 PDN.
Cisco's interface document states the IOS defaults: Hello 10 s on broadcast and point-to-point, 30 s on NBMA; Dead is
four times Hello; the Wait timer equals the Dead interval (the RFC: the Wait Timer runs for RouterDeadInterval before
the interface leaves Waiting and selects a DR). Cisco also says the network type must match on both routers for them
to become neighbours.

## Mismatch behaviour
A received Hello whose Network Mask, HelloInterval or RouterDeadInterval differs from the receiving interface is
dropped (RFC 2328 10.5), except that the mask is ignored on point-to-point and virtual links. A Hello with a different
E-bit than the area's external-routing capability is dropped as well. So pairing broadcast with NBMA (10 vs 30 s)
leaves the neighbour unseen unless timers are set equal. Where timers happen to agree but types differ, one side
expects a DR and the other does not; that is why Cisco says to keep the type identical. This detail of exact symptoms
was not found in the cited pages beyond that statement, so verify per platform.

## Setting the type on IOS
The Cisco page documents the interface command
`ip ospf network {broadcast | non-broadcast | {point-to-multipoint [non-broadcast] | point-to-point}}`
to change from the medium's default. Reason for point-to-point on a two-router Ethernet link: it needs no DR election,
and so avoids the Waiting period (RouterDeadInterval) before a DR is chosen.

## Verify
- [ ] Both ends report the same network type, Hello and Dead.
- [ ] State shows DR/BDR/DROTHER on broadcast and NBMA, point-to-point state otherwise (Cisco doc lists these states).
- [ ] Adjacency count equals what 10.4 predicts for the type.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read RFC 2328 section 1.2 definitions (network kinds), 7.1, 9.5/Wait
Timer, 10.4, 10.5, 12.4.1.4, appendix A.1 (multicast addresses) and C.3-C.6, and the Cisco show ip ospf interface
document (network type, state, priority, timers, and the ip ospf network syntax). Removed as unconfirmed: per-medium
default types (Frame Relay, GRE, HDLC), /31 addressing claim, `no switchport` example, the specific broadcast-vs-
point-to-point symptom narrative, show-command sample output, and the 120 s dead value for NBMA.
