---
id: computing-software.cloud-infrastructure-engineering.istio.istio-circuit-breaking
name: istio-circuit-breaking
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, circuit-breaking, connection-pool, destinationrule]
level: practitioner
status: docs-checked
description: "Limit connections and pending requests with DestinationRule connectionPool, and verify overflow counters on the client sidecar."
sources: ["https://istio.io/latest/docs/tasks/traffic-management/circuit-breaking/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Circuit breaking is configured in a DestinationRule `trafficPolicy.connectionPool`, enforced by the client side proxy.

```yaml
trafficPolicy:
  connectionPool:
    tcp: {maxConnections: 1}
    http: {http1MaxPendingRequests: 1, maxRequestsPerConnection: 1}
```

Drive load with a sidecar-injected client such as fortio (the task uses `fortio load -c 3 -qps 0 -n 30` against a limit of 1).

Gotchas: if Istio has mutual TLS enabled, add `tls.mode: ISTIO_MUTUAL` to the DestinationRule's traffic policy, otherwise requests generate 503 errors. The proxy allows some leeway: with two concurrent connections against a limit of 1 most requests still succeeded (17 of 20 in the task), and only at 3 connections did most fail.

Verify: `kubectl exec <client> -c istio-proxy -- pilot-agent request GET stats | grep httpbin | grep pending` and read `upstream_rq_pending_overflow`, which the task describes as the count of calls flagged for circuit breaking.

## Checked

2026-11-03. Confirmed against the Istio Circuit Breaking task: the connectionPool fields, the `ISTIO_MUTUAL` note, the fortio load commands and results, and the `pilot-agent request GET stats` check of `upstream_rq_pending_overflow`. Removed: unsourced advice on deriving limits and alerting, and the claim that server pods need sidecars.
Method: documentation only; no commands were run.
