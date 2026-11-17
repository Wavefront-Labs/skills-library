---
id: computing-software.cloud-infrastructure-engineering.istio.istio-load-balancing-algorithms
name: istio-load-balancing-algorithms
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, istio-load-balancing, consistent-hash, least-request]
level: practitioner
status: docs-checked
description: "Choose ROUND_ROBIN, LEAST_REQUEST or consistent hash in a DestinationRule, and understand how hashing affects traffic splits."
sources: ["https://istio.io/latest/docs/reference/config/networking/destination-rule/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The DestinationRule reference says to prefer `LEAST_REQUEST` as a drop-in replacement for `ROUND_ROBIN`, and marks `LEAST_CONN` deprecated. Session affinity uses consistent hashing.

```yaml
trafficPolicy:
  loadBalancer:
    consistentHash:
      httpHeaderName: x-user-id
```

Alternatives: `httpCookie`, `useSourceIp: true` (hash on the source IP, for TCP and HTTP) and `httpQueryParameterName`.

Gotchas: the reference warns that consistent hashing depends on every proxy having a consistent view of endpoints, which is not the case when locality load balancing is enabled; the two only work together when all proxies are in the same locality or a higher-level load balancer handles locality affinity. The reference calls `ROUND_ROBIN` generally unsafe when endpoint weighting is used.

Verify: send requests with different `x-user-id` values and confirm each value consistently reaches one pod (`kubectl logs` per pod).

## Checked

2026-11-03. Confirmed in the DestinationRule reference: `LEAST_REQUEST` and `ROUND_ROBIN` guidance, `LEAST_CONN` deprecated, the consistent hash options `httpCookie`, `useSourceIp` and `httpQueryParameterName`, and the locality warning. Removed: the claim that `LEAST_REQUEST` is the default in recent releases, the weight-override, cardinality, NAT and scaling-reshuffle remarks and the replica advice (not on the page).

Method: documentation only; no commands were run.
