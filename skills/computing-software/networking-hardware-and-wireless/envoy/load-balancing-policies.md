---
id: computing-software.networking-hardware-and-wireless.envoy.load-balancing-policies
name: load-balancing-policies
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, load-balancing, round-robin, least-request, ring-hash, maglev, random, client-side-weighted-round-robin]
level: practitioner
status: docs-checked
description: "Select an Envoy cluster load balancing policy (weighted round robin, least request, ring hash, Maglev, ORCA-based) and what unhealthy hosts mean."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/load_balancing/load_balancers.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# load balancing policies
Policies are pluggable and set per cluster via `lb_policy` or the load balancing policy extension. When a filter needs a connection, the cluster manager's policy picks the host. If no active health check is configured, all members are treated as healthy unless `health_status` says otherwise.

```yaml
clusters:
- name: backend
  lb_policy: LEAST_REQUEST
  least_request_lb_config: { choice_count: 2 }
```
(Policy names: ROUND_ROBIN, LEAST_REQUEST, RING_HASH, RANDOM, MAGLEV.)

From the docs:
- Weighted round robin: simple round robin; with endpoint `load_balancing_weight` set per locality, higher weights appear more often in the rotation.
- Client-side weighted round robin (`ClientSideWeightedRoundRobin` extension): weights come from ORCA load reports sent by upstreams, combining QPS, errors per second and utilisation, recomputed periodically from the most recent report.
- Ring hash and Maglev give consistent hashing for session affinity based on route `hash_policy`.

Gotcha: ring hash hashes some property of the request to pick a host, so the route needs a `hash_policy` saying which property. Slow start works with round robin, least request and client-side WRR. Verify distribution from per-host `rq_total` in `GET /clusters`.

## Checked

2026-11-03. Confirmed against: load_balancers.rst and cluster.proto (policy enum, least_request_lb_config choice_count, ORCA weights). Removed or corrected: the unsupported claim that missing hash_policy falls back to random-like selection and the version hedge.

Method: documentation only; no commands were run.
