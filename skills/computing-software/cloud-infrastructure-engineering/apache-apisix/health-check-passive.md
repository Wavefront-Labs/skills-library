---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.health-check-passive
name: health-check-passive
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, health-check, passive-health-check, upstream, checks, circuit-breaking]
level: practitioner
status: docs-checked
description: "Configure passive upstream health checks in APISIX: checks.passive statuses and failure thresholds, their defaults, and why to pair them with active checks."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/tutorials/health-check.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passive health checks

Set under `upstream.checks.passive`; they judge real traffic instead of probing. Defaults:
- `type`: `http` (also `https`, `tcp`).
- `healthy.http_statuses`: 200-208, 226 and 300-308; `healthy.successes`: 5.
- `unhealthy.http_statuses`: `[429, 500, 503]`.
- `unhealthy.http_failures`: 5; `unhealthy.tcp_failures`: 2; `unhealthy.timeouts`: 7.

```json
"checks": {
  "passive": {
    "healthy": { "http_statuses": [200, 201], "successes": 3 },
    "unhealthy": { "http_statuses": [500], "http_failures": 3, "tcp_failures": 3 }
  }
}
```

Limits:
- Unhealthy nodes cannot receive requests, so a passive check alone cannot re-mark a node healthy; combining it with an active check is usually necessary.
- It cannot detect failures before they happen; some requests may fail first.
- Health checking starts only when the upstream is hit by a request; an unused upstream is never checked.

## Checked

2026-11-04: read the Health Check tutorial; the passive defaults table (type http, healthy statuses and successes 5, unhealthy statuses [429, 500, 503], http_failures 5, tcp_failures 2, timeouts 7), the example block and the limits match. Reworded the two limit lines to the page's wording.

Method: documentation only; no commands were run.
