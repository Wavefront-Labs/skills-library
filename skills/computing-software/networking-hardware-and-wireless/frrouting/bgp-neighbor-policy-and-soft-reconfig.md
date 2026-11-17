---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-neighbor-policy-and-soft-reconfig
name: bgp-neighbor-policy-and-soft-reconfig
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, neighbor-route-map, prefix-list, filter-list, soft-reconfiguration, clear-bgp, maximum-prefix]
level: practitioner
status: docs-checked
description: "Apply route-maps, prefix-lists, distribute-lists and filter-lists to FRR BGP neighbors, use soft-reconfiguration inbound, clear bgp, and cap prefixes."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP neighbor policy and soft reconfiguration
Per-peer filters (each takes `in` or `out`): `neighbor PEER route-map NAME`, `prefix-list NAME`, `distribute-list NAME`, `filter-list NAME` (AS-path).

- `neighbor PEER soft-reconfiguration inbound` stores unmodified received routes so inbound policy can be re-applied without a reset, at memory cost. If both peers support route-refresh, `clear bgp PEER in` works without it; `maximum-prefix ... force` still needs it.
- `clear bgp ipv4|ipv6 [unicast] PEER soft|in|out` does soft reconfiguration; `clear bgp *` resets all peers; `clear bgp ipv4|ipv6 ASNUM` resets by AS; `clear bgp [ipv4|ipv6] [unicast] PEER|* message-stats` clears statistics; `... capabilities` resends capabilities (e.g. FQDN) without a reset.
- `neighbor PEER maximum-prefix NUMBER [force]` tears down the session when exceeded; `force` counts filtered prefixes and needs soft-reconfiguration inbound.
- `neighbor PEER maximum-prefix-out NUMBER` limits prefixes sent.
- `neighbor PEER sender-as-path-loop-detection` filters sender-side AS-path loops.
- `bgp dampening (1-45) (1-20000) (1-50000) (1-255)` (and neighbor variants) is documented as not recommended and not per-VRF; view with `show bgp ... dampening dampened-paths|flap-statistics|parameters`.
- `bgp route-reflector allow-outbound-policy` applies outbound policy to reflected routes.

Inspect what was received versus accepted: `show bgp [afi] [safi] neighbor [PEER] [routes|advertised-routes|received-routes] [<prefix>|detail] [json]`. `routes` is post-inbound-policy, `received-routes` is pre-policy, `filtered-routes` is also available.

With `bgp ebgp-requires-policy` (RFC 8212; on by default in the traditional config, off in the datacenter config), eBGP peers need both an inbound and an outbound filter or no routes are accepted or announced; changing it needs a session clear, and `(Policy)` shows in `show bgp summary`. The page advises a prefix-list over `maximum-prefix`, since tearing down the session is more destructive.

## Checked

2026-11-09. Read the FRR BGP page sections "Peer Filtering", `maximum-prefix`, `soft-reconfiguration inbound`, "Require policy on EBGP", "Route Flap Dampening", "Other BGP Commands" (clear bgp) and the `show bgp neighbor routes|received-routes` text via a local text copy; every command and range above matches. Added the route-refresh note and the ebgp-requires-policy detail.
Method: documentation only; no commands were run.
