---
id: computing-software.systems-network-administration.cisco-networking.ospf-lsa-types-and-lsdb
name: ospf-lsa-types-and-lsdb
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ospf, lsa-types, lsdb, ospf-database, abr, asbr, type-5-lsa, nssa, type-7-lsa, rfc2328, rfc3101]
level: practitioner
status: docs-checked
description: "OSPF LSA types 1-5 and 7 per RFC 2328 and 3101: who originates each, flooding scope, stub and NSSA filtering, LSA timers, and how an external route is resolved via the ASBR."
sources:
  - https://www.rfc-editor.org/rfc/rfc2328
  - https://www.rfc-editor.org/rfc/rfc3101
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPF LSA types and the LSDB

Protocol-level reference from RFC 2328 (OSPFv2) and RFC 3101 (NSSA). Vendor show commands are not listed; use your
platform's database-display commands with the type names below.

| Type | RFC name | Originated by | Flooding scope |
|---|---|---|---|
| 1 | Router-LSA | every router | single area; describes the router's interfaces in that area |
| 2 | Network-LSA | the Designated Router, for broadcast and NBMA networks | single area; lists the routers on the network |
| 3 | Summary-LSA (networks) | area border router | one area at a time; an inter-area route to a network |
| 4 | Summary-LSA (AS boundary routers) | area border router | one area at a time; a route to an ASBR |
| 5 | AS-external-LSA | AS boundary router | whole AS, except stub areas |
| 7 | Type-7 LSA (RFC 3101) | AS boundary router inside an NSSA | that NSSA only |

RFC 2328 section 12.1.3: every LSA type it defines except type 5 is flooded throughout a single area only. Type 5
eligible interfaces are all interfaces except virtual links and those attaching to stub areas (section 13.3).

## Area types and what they filter
- Stub (RFC 2328 12.4.3.1): type 5 is not flooded in, and type 4 summary-LSAs are never originated into the area. The
  ABR originates a default summary-LSA (Link State ID = DefaultDestination, 0.0.0.0) instead. An ABR may originate all,
  or only a subset, of the type 3 LSAs into a stub area; fewer LSAs shrinks the database but can give sub-optimal
  inter-area routing.
- NSSA (RFC 3101): type 5 is not flooded in or originated there. External routes enter as type 7 LSAs, identical to type
  5 except: type field 7, flooded only within the NSSA, and a P (propagate) bit. When P is set, an NSSA border router
  may translate the type 7 into a type 5 for the rest of the AS; translated LSAs must have the forwarding address set.
  Which border router translates is configurable; with none configured, one is elected.
- An NSSA border router should originate a type 7 default (0.0.0.0/0) into the NSSA. A type 7 default from a border
  router is never translated to type 5; one from an internal ASBR may be.
- The N bit in the Options field must match or the adjacency will not form (RFC 3101 section 2.1: the N-bit and E-bit in the Hello options must agree, and a set N-bit requires a clear E-bit).

## How an external route is installed (RFC 2328 16.4)
1. Skip LSAs whose cost is LSInfinity (0xffffff), whose age is MaxAge, or that this router originated itself.
2. Find the routing-table entry for the originating ASBR; if the ASBR is unreachable the LSA is ignored. This is why a
   type 5 with no reachable ASBR (no type 1 or type 4 path to it) installs nothing.
3. Forwarding address 0.0.0.0 means traffic goes to the ASBR itself. Non-zero: look it up in the routing table; it must
   resolve to an intra-area or inter-area path, else the LSA is ignored.
4. The path is type 1 external (cost = distance to ASBR/forwarding address + external metric) or type 2 external (see
   `computing-software.systems-network-administration.cisco-networking.ospf-external-e1-e2-routes`).

## Architectural constants (RFC 2328 appendix B)
| Constant | Value |
|---|---|
| LSRefreshTime | 30 minutes: re-origination of an unchanged self-originated LSA |
| MinLSInterval | 5 seconds between originations of one LSA |
| MinLSArrival | 1 second; faster new instances of the same LSA are discarded |
| MaxAge | 1 hour; a MaxAge LSA is reflooded to flush it and not used in route calculation |
| CheckAge | 5 minutes: checksum verification of LSAs in the database |
| MaxAgeDiff | 15 minutes |

An LSA is identified by LS type, Link State ID and Advertising Router. Premature aging (setting an LSA to MaxAge) is how
a router withdraws an LSA.

## Tracing a missing prefix (method)
1. Origin area: does the originating router's type 1 (and the DR's type 2) list the link?
2. Does the ABR originate the type 3 into your area (and is it not suppressed by a stub/filter)?
3. For an external prefix: is the type 5 (or type 7 in an NSSA, or the translated type 5) present, and can you resolve
   the ASBR and forwarding address as above?
4. An LSA that exists but is not installed is almost always one of: unreachable ASBR, unresolvable forwarding address,
   LSInfinity or MaxAge, or a self-originated LSA.

## Verify
- [ ] The database is identical (same checksums and sequence numbers) on every router in an area.
- [ ] Stub areas hold no type 4 or 5; NSSAs hold type 7 and no type 5.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read RFC 2328 Table 9/15 and 12.1.3, 12.4.3.1, 13.3 (eligible
interfaces), 16.4 (external route calculation) and appendix B (constants), and RFC 3101 sections 2.1-2.3 and its type 7
differences list. The Cisco 13689-17 page cited earlier is about `show ip ospf interface`, not the LSDB, and was
dropped. Removed as unconfirmed: all `show ip ospf database` command lines, SPF-count and "redistribution leak"
health-check heuristics, the "totally stubby" description (not defined in RFC 2328), and the O IA / O E1/E2 code
mapping.
