---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-route-origination
name: bgp-route-origination
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, network, redistribute, aggregate-address, summary-only, default-originate, table-map]
level: practitioner
status: docs-checked
description: "Originate routes in FRR BGP with network, redistribute, aggregate-address (summary-only, as-set, suppress-map) and neighbor default-originate, and filter to zebra with table-map."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP route origination
- `network A.B.C.D/M` announces a prefix; bgpd does not require it in the IGP table, but see `bgp network import-check`.
- `redistribute <protocol> [metric (0-4294967295)] [route-map WORD]` for babel, connected, eigrp, isis, kernel, openfabric, ospf, ospf6, rip, ripng, sharp, static. `redistribute table (1-65535)` imports via the default table; `table-direct` skips that step.
- `aggregate-address A.B.C.D/M` options: `route-map NAME`, `origin <egp|igp|incomplete>`, `as-set`, `summary-only`, `matching-MED-only`, `suppress-map NAME`, `upa [drop] [max-routes N]`. A more specific prefix must exist in the BGP table (not only the RIB). `summary-only` suppresses more-specifics to all neighbors; `suppress-map` does so only for routes the map matches.
- `neighbor PEER default-originate [route-map WORD]`: bgpd does not announce the default route to a peer unless this is configured; with a route-map the default is originated only when the route-map conditions are met. `bgp default-originate timer (0-65535)` sets the scan period (default 5 s; 0 disables).
- `bgp reject-as-sets` rejects AS_SET and AS_CONFED_SET routes.
- `table-map ROUTE-MAP-NAME` filters routes sent from BGP to zebra; set operations are limited to metric and next hop.
- `distance bgp (1-255) (1-255) (1-255)` sets external, internal and local distances.
- Inspect: `show bgp <ipv4|ipv6> unicast redistribute [json]`, `show bgp ... aggregate-address [prefix] [json]`; `debug bgp aggregate [prefix P]`.

## Checked

2026-11-04. Confirmed against the FRR BGP page: network and import-check, redistribute forms including table and table-direct, aggregate-address options and the more-specific-in-BGP-table requirement, default-originate timer, reject-as-sets, table-map, distance bgp, show and debug commands. Removed the route-map set-only and existing-default sentences, which the page does not state.
Method: documentation only; no commands were run.
