---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-route-reflector-and-solo
name: bgp-route-reflector-and-solo
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, route-reflector, cluster-id, ibgp, attribute-unchanged, next-hop-self]
level: practitioner
status: docs-checked
description: "Configure FRR BGP route reflection: route-reflector-client, cluster-id, allow-outbound-policy, and next-hop and attribute handling in iBGP."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP route reflector
- `neighbor PEER route-reflector-client` marks a reflector client.
- `bgp cluster-id A.B.C.D` sets the cluster ID for loop prevention; cluster-list length is also a late best-path tie-breaker.
- `bgp route-reflector allow-outbound-policy` lets outbound route-maps modify reflected routes (by default outbound route-map changes are not applied to reflected routes; once enabled it affects all reflected routes).
- `neighbor PEER solo` prevents routes being reflected back to the peer.
- `neighbor PEER next-hop-self [force]` rewrites next hop to the local address for eBGP-learned routes; `force` also covers iBGP-learned routes.
- `neighbor PEER attribute-unchanged [{as-path|next-hop|med}]` leaves the named attributes untouched in advertisements.
- `maximum-paths ibgp (1-128) [equal-cluster-length]` for iBGP ECMP.
- `neighbor PEER graceful-shutdown` adds the graceful-shutdown community and sets local-preference 0.

Show: `show [ip] bgp neighbors A.B.C.D advertised-routes` to see what a client receives.

## Checked
2026-11-09. Partial read of docs.frrouting.org bgp.html (one large page): the route reflector section (route-reflector-client, cluster-id), allow-outbound-policy, next-hop-self, attribute-unchanged, solo, maximum-paths ibgp, graceful-shutdown and the neighbor advertised-routes show commands. Removed: the router-bgp-mode statement, the cluster-id loop-prevention wording beyond the cluster description, and show bgp summary.
Method: documentation only; no commands were run.
