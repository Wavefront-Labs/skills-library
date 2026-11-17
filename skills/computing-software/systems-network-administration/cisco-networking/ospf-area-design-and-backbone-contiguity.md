---
id: computing-software.systems-network-administration.cisco-networking.ospf-area-design-and-backbone-contiguity
name: ospf-area-design-and-backbone-contiguity
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ospf, ospf-area-design, ospf-multi-area, area-0, backbone-area, abr, virtual-link, summarization, rfc2328]
level: practitioner
status: docs-checked
description: "OSPF area design rules from RFC 2328: backbone contiguity, ABR roles, address ranges, stub restrictions, and how partitions behave and are repaired with virtual links."
sources:
  - https://datatracker.ietf.org/doc/html/rfc2328
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPF area design and backbone contiguity

Source of truth is RFC 2328 section 3 ("Splitting the AS into Areas"). Platform-specific commands and sizing folklore
are intentionally excluded.

## Rules the RFC states
- An area is a group of contiguous networks and hosts, plus the routers attached to them. Each area has its own
  link-state database and its own SPF; its topology is invisible outside, which cuts routing traffic and protects
  intra-area routing from outside information.
- Routers in the same area have identical databases for that area. A router in several areas (an ABR) keeps one
  database per area and runs one copy of the algorithm per area.
- The backbone is area 0 (0.0.0.0). It always contains all ABRs and carries routing information between non-backbone
  areas. It MUST be contiguous, but not necessarily physically: virtual links can maintain connectivity.
- Inter-area routing is a star with the backbone as hub: intra-area path to an ABR, a backbone path, then an
  intra-area path to the destination. Each ABR summarises its cost to networks outside the area.
- Virtual links join two backbone routers that share a common non-backbone area, belong to the backbone, and cannot be
  configured through stub areas. Their cost is the intra-area distance between the routers.
- Router classes: internal, area border, backbone (any router with an interface in area 0) and AS boundary routers;
  the AS boundary role is independent of the others.
- Stub restrictions: no virtual links through a stub area, and AS boundary routers cannot be placed inside one.
- Address ranges (summarisation) are configured per area on the ABR, one summary per range (see
  `computing-software.systems-network-administration.cisco-networking.ospf-type-3-lsa-filtering`).

## Design guidance that follows
1. Keep area 0 redundant so a single failure cannot partition it: parts of the AS become unreachable if it does.
2. Align each area with a contiguous address block so a range can condense it. The RFC (3.7) warns that an address
   range must not be split across components of a partitioned area.
3. Use ranges on every ABR of the area, identically.
4. A stub area suits a site with a simple exit; if the site has its own ASBR it cannot be stub (see the NSSA material in
   `computing-software.systems-network-administration.cisco-networking.ospf-lsa-types-and-lsdb`).

## Partitions (section 3.7)
- OSPF does not repair area partitions: each component becomes a separate area and the backbone routes between them.
  Destinations that were intra-area then need inter-area routing.
- A backbone partition makes parts of the AS unreachable. It can be repaired by configuring virtual links (section 15).
  Best fix is restoring a physical backbone link; a virtual link is the repair mechanism, not a permanent design.

## Verify
- [ ] Every non-backbone area has an ABR with an area 0 interface.
- [ ] Removing any single area 0 link or router leaves area 0 connected (check the topology graph).
- [ ] Address ranges on the ABRs of an area are identical.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read RFC 2328 sections 3 introduction, 3.1, 3.2, 3.3, 3.6 stub
restrictions and 3.7 (partitions), and appendix C.4 on virtual links. The Cisco 7039-1 page is a topic index and was
dropped. Removed as unconfirmed: the claim Cisco ABRs need an active area 0 adjacency to originate summaries, router
count sizing guidance, GRE-tunnel backbone repair, anti-pattern list, all IOS lines and show commands.
