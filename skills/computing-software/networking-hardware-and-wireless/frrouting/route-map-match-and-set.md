---
id: computing-software.networking-hardware-and-wireless.frrouting.route-map-match-and-set
name: route-map-match-and-set
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, route-map, match, set, local-preference, next-hop, metric, tag]
level: practitioner
status: docs-checked
description: "Write FRR route-map entries with permit or deny and sequence, using match clauses (address, next-hop, as-path, community, tag) and set actions (metric, local-pref, next-hop)."
sources:
  - https://docs.frrouting.org/en/latest/routemap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route-map match and set
`route-map NAME (permit|deny) ORDER`. An entry with no match conditions always matches.

Match examples: `match ip address ACCESS_LIST`, `match ip address prefix-list PL`, `match ip address prefix-len 0-32` (Zebra), the `ipv6` equivalents, `match ip next-hop ...`, `match as-path AS_PATH`, `match metric METRIC`, `match tag <untagged|(1-4294967295)>`, `match local-preference METRIC`, `match community COMMUNITY_LIST [<exact-match|any>]`, `match source-protocol PROTOCOL_NAME` (Zebra and BGP), `match source-instance NUMBER` (0-255), `match evpn route-type`, `match evpn vni NUMBER`, `match vpn dataplane <mpls|srv6|vxlan>`. BGP-specific: `match peer`, `match src-peer`, `match ip next-hop address IPV4_ADDR`.

Set examples: `set tag`, `set ip next-hop IPV4_ADDRESS|peer-address|unchanged`, `set ipv6 next-hop peer-address|prefer-global|global ADDR|local ADDR`, `set local-preference LOCAL_PREF` (also `+`/`-`), `set distance (1-255)`, `set weight WEIGHT`, `set metric <[+|-](1-4294967295)|rtt|+rtt|-rtt|igp|aigp>`, `set min-metric`, `set max-metric`, `set as-path prepend|exclude`, `set community`, `set origin <egp|igp|incomplete>`, `set table (1-4294967295)`, `set sr-te color (1-4294967295)`.

Example:
```
route-map test permit 10
 match ip address 10
 set local-preference 200
```

For a route reflector to apply a route-map to reflected routes, set `bgp route-reflector allow-outbound-policy` in `router bgp`.

## Checked

2026-11-04. Confirmed against the FRR Route Maps page: entry semantics, every match and set command listed, option ranges and the route-reflector allow-outbound-policy note. Nothing changed.
Method: documentation only; no commands were run.
