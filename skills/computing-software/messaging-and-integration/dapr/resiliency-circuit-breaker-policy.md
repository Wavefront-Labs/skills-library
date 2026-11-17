---
id: computing-software.messaging-and-integration.dapr.resiliency-circuit-breaker-policy
name: resiliency-circuit-breaker-policy
category: computing-software
field: messaging-and-integration
product: dapr
tags: [resiliency, circuit-breaker, trip, cel, half-open, maxrequests, timeout]
level: advanced
status: docs-checked
description: "Configure Dapr circuit breakers: maxRequests, interval, timeout and the CEL trip expression, with open, half-open and closed states and per-target scoping of breakers."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/resiliency/policies/circuit-breakers.md
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/resiliency/resiliency-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Circuit breakers stop sending traffic to a target that keeps failing, so it can recover instead of being flooded. After enough failures the breaker trips (open); after a wait it goes half-open and lets a few requests through; successful requests close it again.

```yaml
spec:
  policies:
    circuitBreakers:
      pubsubCB:
        maxRequests: 1
        interval: 8s
        timeout: 45s
        trip: consecutiveFailures > 8
```

Options:

- `maxRequests`: requests allowed while half-open; default `1`.
- `interval`: cyclical period after which the internal counts clear; `0s` means never; default `0s`.
- `timeout`: how long the breaker stays open before switching to half-open; default `60s`.
- `trip`: a Common Expression Language (CEL) expression evaluated by the breaker; when true the breaker opens. Default `consecutiveFailures > 5`; other possible values are `requests` and `totalFailures` (total, not necessarily consecutive, failed attempts), for example `requests > 5 and totalFailures >3`.

Scoping (from the resiliency overview): breakers are created per app instance for apps (a tripped route is removed from load balancing for the `timeout`), per actor type, id or both for actors (`circuitBreakerScope: both` with `circuitBreakerCacheSize: 5000`), and per component configuration for components, where a trip blocks all interaction with that component for the `timeout`. Counters live as long as the sidecar runs and are not persisted.

Attach with `circuitBreaker: <name>` in the target.

## Checked

2026-11-04. Policy YAML, option defaults and state behaviour confirmed on the Circuit breaker resiliency policies page; scoping from the overview example.

Method: documentation only; no commands were run.
