---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.healthchecks-passive
name: healthchecks-passive
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, passive-health-checks, circuit-breaker, unhealthy-statuses, upstreams, health-checks]
level: practitioner
status: docs-checked
description: "Kong passive health checks (circuit breakers): defaults for healthy and unhealthy statuses and counters, why they never re-enable a Target, and how to disable."
sources:
  - https://developer.konghq.com/gateway/traffic-control/health-checks-circuit-breakers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passive health checks

Passive checks watch proxied traffic and send no extra requests. They can mark Targets unhealthy but never re-enable them automatically; pair them with active checks, or re-enable manually.

Defaults under `healthchecks.passive`:

| Field | Default |
|---|---|
| `healthy.successes` | `0` (must be positive when passive checks are enabled) |
| `healthy.http_statuses` | `200` to `208`, `226`, `300` to `308` |
| `unhealthy.http_failures` | `0` |
| `unhealthy.tcp_failures` | `0` |
| `unhealthy.timeouts` | `0` |
| `unhealthy.http_statuses` | `429, 500, 503` |

Counter logic: a healthy status increments Successes and clears the other counters. TCP failures, timeouts and HTTP failures increment their own counter and clear Successes. A Target goes unhealthy when a failure counter reaches its threshold. Unhealthy Targets are skipped, not removed, and their database state is unchanged.

Disable passive checks by setting all counter thresholds to `0`.

## Checked

2026-11-04. Confirmed against the Health checks and circuit breakers page: the six defaults, counter logic, skipped-not-removed Targets, unchanged database state, no automatic re-enable and the disable instruction. Removed the JSON example attributed to the docs, which is not on the page.
Method: documentation only; no commands were run.
