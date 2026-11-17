---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.healthchecks-active
name: healthchecks-active
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, active-health-checks, http-path, healthy-interval, upstreams, health-checks]
level: practitioner
status: docs-checked
description: "Kong Upstream active health checks: probe type, http_path, timeout, concurrency, healthy and unhealthy thresholds and statuses, all defaults, and how to disable."
sources:
  - https://developer.konghq.com/gateway/traffic-control/health-checks-circuit-breakers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active health checks

Health checks are disabled by default. Active checks send periodic probes to each Target and can disable and re-enable Targets automatically. They do not apply to Services using `tcp` or `tls`. Each Kong node tracks Target health separately.

Defaults under `healthchecks.active`:

| Field | Default |
|---|---|
| `type` | `http` (`https`, `tcp` allowed) |
| `http_path` | `/` |
| `timeout` | `1` second |
| `concurrency` | `10` |
| `healthy.interval` | `0` (disabled) |
| `healthy.successes` | `0` |
| `healthy.http_statuses` | `200, 302` |
| `unhealthy.interval` | `0` (disabled) |
| `unhealthy.http_failures` / `tcp_failures` / `timeouts` | `0` |
| `unhealthy.http_statuses` | `429, 404, 500, 501, 502, 503, 504, 505` |
| `https_verify_certificate` | `true` (HTTPS only) |

Also `https_sni` for HTTPS probes.

A Target turns unhealthy when its failure or timeout counter reaches the threshold, and healthy when `successes` reaches its threshold.

Disable by setting both `healthy.interval` and `unhealthy.interval` to `0`; a positive interval enables probing for healthy or unhealthy Targets respectively.

## Checked

2026-11-04. Confirmed against the Health checks and circuit breakers page: every default in the table, probe types, `https_sni`, TLS verification, tcp/tls exclusion, per-node health and the disable instruction. Removed the JSON example attributed to the docs, which is not on the page.
Method: documentation only; no commands were run.
