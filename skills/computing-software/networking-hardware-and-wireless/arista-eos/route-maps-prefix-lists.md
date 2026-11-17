---
id: computing-software.networking-hardware-and-wireless.arista-eos.route-maps-prefix-lists
name: route-maps-prefix-lists
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, route-map, prefix-list, community-list, as-path-access-list]
level: practitioner
status: draft
description: "Write EOS route-maps with match/set, prefix-lists, communities and AS-path filters for BGP policy."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Route-maps and prefix-lists
Goal: control route advertisement and selection.

```
ip prefix-list PL-LOCAL seq 10 permit 192.0.2.0/24
route-map RM-OUT permit 10
   match ip address prefix-list PL-LOCAL
   set community 65101:100 additive
route-map RM-OUT deny 20
router bgp 65101
   neighbor 198.51.100.0 route-map RM-OUT out
   neighbor 198.51.100.0 route-map RM-IN in
```

```
show route-map RM-OUT
show ip prefix-list PL-LOCAL
show ip bgp neighbors 198.51.100.0 advertised-routes
```

- Route-map sequences are evaluated in order; `permit` applies sets and accepts; `deny` rejects; there is an implicit deny at the end.
- Communities need `send-community` to be sent to the neighbor.
- Apply changes with a soft reset: `clear ip bgp 198.51.100.0 soft`.

Gotcha: an empty or missing route-map referenced on a neighbor denies everything on that neighbor, which can drop a production session's routes silently. Create the route-map first.

Operational tip: version-control route-maps with the prefix lists they reference, and test with `show ip bgp ... route-map X` (confirm) or a lab peer before applying on production neighbors.

## Verify
- `show ip bgp neighbors ... advertised-routes` lists only the permitted prefixes with the community set.
