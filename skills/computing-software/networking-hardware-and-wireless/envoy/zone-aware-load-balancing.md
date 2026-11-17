---
id: computing-software.networking-hardware-and-wireless.envoy.zone-aware-load-balancing
name: zone-aware-load-balancing
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, zone-aware, locality, local-zone, cross-zone, min-cluster-size, routing-enabled]
level: practitioner
status: docs-checked
description: "Keep traffic in the local zone with Envoy zone aware routing, and know its preconditions around panic mode, cluster size and subsets."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/load_balancing/zone_aware.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zone aware load balancing
Zone aware routing is best-effort routing of requests from an originating cluster to hosts in the same zone in the upstream cluster, while keeping roughly the same requests per second per upstream host. Preconditions in the docs:
- neither the originating nor the upstream cluster is in panic mode;
- zone aware routing is enabled (`zone_aware_lb_config` routing enabled, which is a runtime-controlled percentage);
- the upstream cluster has enough hosts (`min_cluster_size`).

Envoy decides between local-zone routing and cross-zone spill based on the healthy host percentages in the local zone of the originating and upstream clusters. If the local upstream zone can absorb all of the originating zone's traffic it sends it all local; otherwise it routes the residual across zones in proportion to capacity.

```yaml
common_lb_config:
  zone_aware_lb_config:
    routing_enabled: { value: 100.0 }
    min_cluster_size: 6
```

Needs: the local zone must be known (`--service-zone` on the originating Envoy) and endpoints must carry locality. Subsets are compatible, but they can easily violate the minimum-hosts condition. Gotcha: when the upstream cluster has fewer hosts than `min_cluster_size`, zone aware routing is not used. Verify with the cluster `lb_zone_*` stats, for example `lb_zone_routing_all_directly` and `lb_zone_routing_cross_zone`.

## Checked

2026-11-03. Confirmed against: zone_aware.rst, cluster_stats.rst (lb_zone_* counters) and cluster.proto (routing_enabled, min_cluster_size). Removed or corrected: the 'silently does nothing' wording and the version hedge.

Method: documentation only; no commands were run.
