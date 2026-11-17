---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.healthchecks-threshold
name: healthchecks-threshold
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, healthchecks-threshold, manual-healthy, upstream-503, upstreams, health-checks]
level: advanced
status: docs-checked
description: "Kong Upstream healthchecks.threshold (minimum healthy weight percent, 503 below it) and manually marking a Target healthy via the Admin API in traditional mode."
sources:
  - https://developer.konghq.com/gateway/traffic-control/health-checks-circuit-breakers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upstream threshold and manual healthy

`healthchecks.threshold` is the minimum percentage of total Target weight that must be available. If available capacity drops below it the whole Upstream is unhealthy and Kong returns `503 Service Unavailable`.

Docs example: `threshold=55` with five Targets at `weight=100`. Losing two leaves 60% capacity, still healthy. Losing a third leaves 40%, so the Upstream is unhealthy.

## Manually re-enabling a Target

Traditional mode only (not Konnect or hybrid):

```bash
curl -i -X PUT http://localhost:8001/upstreams/example-upstream/targets/10.1.2.3:1234/healthy
```

This broadcasts to the whole cluster and resets health counters on all workers, so traffic can route to the Target again.

Passive checks never re-enable Targets by themselves, which is why this call exists.

In DB-less mode, setting Target health with `POST` still works even though other entity writes return 405.

In hybrid mode, edit the Upstream in the Konnect UI instead (enable Active Health Checks).

## Checked

2026-11-04. Confirmed against the Health checks and circuit breakers page: the threshold meaning, 503 response, the threshold=55 example, the PUT `/healthy` path, cluster broadcast, traditional-only scope, and (with the DB-less mode page) POST health still working in DB-less. Removed the stated default of 0, which the page defers to the Upstream schema.
Method: documentation only; no commands were run.
