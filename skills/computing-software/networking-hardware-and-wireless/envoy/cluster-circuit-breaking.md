---
id: computing-software.networking-hardware-and-wireless.envoy.cluster-circuit-breaking
name: cluster-circuit-breaking
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, circuit-breaker, max-connections, max-pending-requests, max-requests, retry-budget, overflow-counters]
level: practitioner
status: docs-checked
description: "Configure per-cluster Envoy circuit breakers (connections, pending, requests, retries, connection pools) and read the matching overflow counters."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/circuit_breaking.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/upstream/cluster_manager/cluster_circuit_breakers.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cluster circuit breaking
Envoy enforces fully distributed (uncoordinated, per-proxy) circuit breaking at the network level so applications do not each need their own. Limits per cluster and priority:
- maximum connections (overflow counter `upstream_cx_overflow`), counting active and draining connections
- maximum pending requests (`upstream_rq_pending_overflow`)
- maximum requests (`upstream_rq_active_overflow`)
- maximum active retries (`upstream_rq_retry_overflow`); retry budgets are recommended instead
- maximum concurrent connection pools

```yaml
circuit_breakers:
  thresholds:
  - priority: DEFAULT
    max_requests: 75
    max_pending_requests: 35
    retry_budget:
      budget_percent: { value: 25.0 }
      min_retry_concurrency: 10
```
Gotchas: even when the connection breaker overflows, Envoy ensures a selected host has at least one connection, so `upstream_cx_active` can exceed the limit, up to the cluster maximum plus (endpoints x connection pools). For HTTP/2, with no max concurrent streams or max requests per connection set, all requests multiplex on one connection and the pending-request breaker only trips when no connection exists. The newer `upstream_rq_active_overflow` counter replaced incrementing `upstream_rq_pending_overflow` on that path unless the runtime flag `envoy.reloadable_features.skip_pending_overflow_count_on_active_rq` is false.

All thresholds can be overridden at runtime with keys named `circuit_breakers.<cluster_name>.<priority>.<setting>`. Verify with `GET /clusters` (lists circuit breaker settings per priority) and the overflow counters in `/stats`.

## Checked
2026-11-03. Confirmed against circuit_breaking.rst, cluster_circuit_breakers.rst and the admin /clusters entry. Removed or corrected: the claim that /clusters shows breaker state (it lists breaker settings).
Method: documentation only; no commands were run.
