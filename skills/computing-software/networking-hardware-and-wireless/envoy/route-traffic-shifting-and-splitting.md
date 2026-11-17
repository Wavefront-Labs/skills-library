---
id: computing-software.networking-hardware-and-wireless.envoy.route-traffic-shifting-and-splitting
name: route-traffic-shifting-and-splitting
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, traffic-shifting, traffic-splitting, runtime-fraction, weighted-clusters, canary, blue-green]
level: practitioner
status: docs-checked
description: "Shift or split traffic between clusters with runtime_fraction routes or weighted_clusters for canaries and A/B tests."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_conn_man/traffic_splitting.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# route traffic shifting and splitting
Envoy's router can split traffic for a route across two or more clusters. Two uses: gradual version upgrades (shifting) and A/B or multivariate testing (splitting).

Shifting uses the route match `runtime_fraction`. Order two routes so that the first matches only a fraction of traffic and the second catches the rest:

```yaml
routes:
- match:
    prefix: /
    runtime_fraction:
      default_value: { numerator: 50, denominator: HUNDRED }
      runtime_key: routing.traffic_shift.helloworld
  route: { cluster: helloworld_v2 }
- match: { prefix: / }
  route: { cluster: helloworld_v1 }
```
Changing the runtime key (for example through the admin `runtime_modify` endpoint or an RTDS layer) moves the percentage without redeploying config. For fixed A/B splits the docs use `weighted_clusters` on a single route with per-cluster `weight` values (and an optional `runtime_key_prefix` to adjust them at runtime).

Gotcha: Envoy uses first-match route selection, and a route with `runtime_fraction` is matched only for that fraction of requests, so the catch-all route must come after it. The `weighted_clusters` weights must sum to more than 0; the `total_weight` field is deprecated.

## Checked
2026-11-03. Confirmed against traffic_splitting.rst. Removed or corrected: the upstream_rq_total verify step.
Method: documentation only; no commands were run.
