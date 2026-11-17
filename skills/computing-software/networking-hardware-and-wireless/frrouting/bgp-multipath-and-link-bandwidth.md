---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-multipath-and-link-bandwidth
name: bgp-multipath-and-link-bandwidth
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, maximum-paths, multipath-relax, link-bandwidth, weighted-ecmp, extcommunity-bandwidth]
level: advanced
status: docs-checked
description: "Enable BGP ECMP in FRR with maximum-paths and multipath-relax, and do weighted ECMP using the link bandwidth extended community."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP multipath and link bandwidth
- `maximum-paths (1-128)` sets the eBGP ECMP maximum (also per AFI/SAFI); `maximum-paths ibgp (1-128) [equal-cluster-length]` sets iBGP.
- `bgp bestpath as-path multipath-relax` lets paths with equal AS_PATH length be multipath; by default the whole AS_PATH must match.
- `bgp bestpath peer-type multipath-relax` allows eBGP, iBGP or confederation paths to be multipath if otherwise equal.
- `use-underlays-nexthop-weight` (router bgp) signals underlay weights to zebra for recursive nexthops.

Weighted ECMP:
- `set extcommunity bandwidth <(1-25600) | cumulative | num-multipaths> [non-transitive]` sets link bandwidth in Mbps (transitive unless `non-transitive`). `num-multipaths` weights by number of multipaths (anycast). Attach it in an outbound route-map per peer or peer-group per AFI, or to the EVPN advertise route-map for type-5 injection.
- Receiver behaviour: `bgp bestpath bandwidth <ignore|skip-missing|default-weight-for-missing>`. Default: paths missing bandwidth revert to plain ECMP; `ignore` disables weighting; `skip-missing` drops paths without it; `default-weight-for-missing` gives weight 1.
- `neighbor PEER send-nexthop-characteristics` (NHC) default disabled; weighted ECMP with NNHN also needs `bgp bestpath bandwidth ignore`.
- Verify: `show bgp ipv4 unicast <prefix>` for the extended community, `show ip route <prefix>` for per-nexthop weights; debug with `debug bgp updates`, `debug bgp zebra`, `debug zebra kernel`.
- The link bandwidth community propagates to eBGP peers when transitive; the docs say it cannot be blocked on its own, only by disabling all extended communities on the peer (or not advertising the prefixes). An exit router advertising its eBGP link speed should use `non-transitive`.

## Checked

2026-11-09. Read the FRR BGP page (docs.frrouting.org/en/latest/bgp.html) in targeted sections via a local text copy: route selection commands (maximum-paths, multipath-relax), `use-underlays-nexthop-weight`, `send-nexthop-characteristics`, `set extcommunity bandwidth`, and the "Weighted ECMP using BGP link bandwidth" chapter with its show and debug examples. All commands and defaults above match. Added the propagation note from the same chapter.
Method: documentation only; no commands were run.
