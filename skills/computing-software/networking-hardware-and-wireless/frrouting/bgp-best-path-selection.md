---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-best-path-selection
name: bgp-best-path-selection
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, best-path, med, deterministic-med, compare-routerid, always-compare-med, aigp]
level: advanced
status: docs-checked
description: "FRR BGP best-path selection order and the bgp bestpath, MED and deterministic-med options that change it, plus show bgp bestpath."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP best-path selection
Order of steps per the docs: admin distance, weight, local preference, local route, AS path length, origin, MED, external (eBGP over iBGP), IGP cost, multipath, already-selected external, router-ID, cluster-list length, peer address.

Options:
- `bgp bestpath as-path confed` counts confederation path sets and sequences.
- `bgp bestpath compare-routerid` breaks ties on router-ID and skips the already-selected eBGP preference check.
- `bgp bestpath med missing-as-worst` treats a missing MED as worst.
- `bgp always-compare-med` compares MED across different neighbouring ASes.
- `bgp deterministic-med` makes selection deterministic with MED; not set by default and scales poorly with many paths per destination.
- `bgp bestpath aigp` evaluates AIGP between paths that both carry it (disabled by default); `neighbor PEER aigp` sends and receives it on eBGP (implicit on for iBGP).
- `bgp bestpath use-imported-attributes` compares the imported path's attributes for VRF-leaked routes (disabled by default).
- `neighbor PEER weight WEIGHT` sets a default weight for the neighbor's routes.

MED is compared only between routes received from the same AS unless `bgp always-compare-med` is set.

Verify with `show bgp [<view|vrf> VIEWVRFNAME] bestpath [json]`, `show bgp <afi> <safi> neighbors WORD bestpath-routes [detail]`, and `debug bgp bestpath <prefix>`.

## Checked
2026-11-09. Partial read of docs.frrouting.org bgp.html (one large page): the Route Selection concepts list, the bgp bestpath options, deterministic-med, neighbor aigp and weight, bestpath-routes and debug bgp bestpath. Removed: the route-map set weight and set local-preference claim (not on this page). Fixed: the bestpath-routes syntax.
Method: documentation only; no commands were run.
