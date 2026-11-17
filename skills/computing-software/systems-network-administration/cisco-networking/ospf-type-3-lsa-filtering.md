---
id: computing-software.systems-network-administration.cisco-networking.ospf-type-3-lsa-filtering
name: ospf-type-3-lsa-filtering
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ospf, lsa-filtering, type-3-lsa, summary-lsa, abr, area-range, donotadvertise, rfc2328]
level: practitioner
status: docs-checked
description: "Where OSPF routes can be hidden: ABR summary-LSA origination and Advertise/DoNotAdvertise area ranges per RFC 2328, and why local RIB filtering leaves the LSDB unchanged."
sources:
  - https://www.rfc-editor.org/rfc/rfc2328#section-12.4.3
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPF type 3 LSA filtering and summarisation (RFC 2328 12.4.3)

Within an area every router holds an identical link-state database (section 3), so OSPF cannot hide a prefix from one
router in an area. Information can be controlled only where LSAs are originated: type 3 and 4 summary-LSAs at area
border routers (ABRs), and AS-external-LSAs at AS boundary routers. Vendor knobs (area ranges, prefix filters on
inter-area LSAs, distribute lists) should be mapped onto these facts; their syntax is not given here because the Cisco
configuration page was a 404 when checked.

## What an ABR advertises into area A (section 12.4.3)
For each routing-table entry the ABR originates a summary-LSA unless:
- the route's area is area A itself, or its next hops are in area A (a split-horizon rule);
- the cost is LSInfinity or more;
- the destination is an ASBR and the entry is not the preferred path (type 4 only; never into stub areas).

Otherwise: an inter-area route to a network yields a type 3 summary-LSA with the routing-table cost.

## Address ranges: summarise or suppress
Each area has a configured list of ranges, each an address and mask with status Advertise or DoNotAdvertise.
- At most one type 3 LSA is originated per range, so component networks are condensed.
- Advertise: one type 3 with the range's address and a cost equal to the largest cost of any component network.
- DoNotAdvertise: the type 3 is suppressed and the components stay hidden from other areas.
- A network in no configured range gets its own type 3 with its routing-table cost (so the default is no summarisation).
- Ranges apply to intra-area routes. Backbone ranges must be ignored when originating summaries into transit areas:
  backbone networks are not condensed or suppressed there.
- If a destination becomes unreachable or no longer advertisable, the ABR flushes the LSA by setting age to MaxAge.

## Consequences for filtering
- Suppress at the source area's ABR with DoNotAdvertise to hide an area's internal prefixes from every other area.
- Intra-area routes cannot be hidden from other routers of their own area.
- With several ABRs, every one must apply the same range or filter, otherwise the other ABR still originates it.
- Anything applied only to a router's own routing table after SPF does not change what its LSDB holds or floods
  (a consequence of the identical-database rule, not a statement from the RFC): neighbours still install the route and
  may send traffic that the filtering router then drops.
- External routes are controlled at the ASBR that originates them. Type 5 LSAs are not flooded into stub areas, which
  receive a default summary-LSA from the ABR instead.
- Dropping a prefix that is the only path for some routers makes it unreachable for them; check dependants first.

## Verify
- [ ] The prefix is absent from the summary LSAs in the target area on every router there (via your platform's
      database display).
- [ ] The same configuration exists on every ABR of the source area.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read RFC 2328 section 3 introduction (area databases), 12.4.3
(summary-LSA origination, address ranges, Advertise/DoNotAdvertise, transit-area exception, flushing) and 12.4.3.1.
Removed as unconfirmed: the Cisco page (404) and every IOS command (`filter-list`, `area range not-advertise`,
`distribute-list in`, `summary-address`), the show commands and the claim about prefix-list implicit deny.
