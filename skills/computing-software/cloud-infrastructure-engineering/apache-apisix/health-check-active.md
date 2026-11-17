---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.health-check-active
name: health-check-active
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, health-check, active-health-check, upstream, checks, probe]
level: practitioner
status: docs-checked
description: "Configure active upstream health checks in APISIX: checks.active type, http_path, intervals, thresholds and their defaults, and when probing starts."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/tutorials/health-check.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active health checks

Set under `upstream.checks.active`. Defaults:
- `type`: `http` (also `https`, `tcp`); `timeout`: 1 second; `concurrency`: 10.
- `http_method`: `GET`; `http_path`: `/`; `req_headers`: `[]`.
- `host`/`port`: the node's own; `https_verify_certificate`: true.
- `healthy.interval` 1; `healthy.http_statuses` `[200, 302]`; `healthy.successes` 2.
- `unhealthy.interval` 1; `unhealthy.http_statuses` `[429, 404, 500, 501, 502, 503, 504, 505]`.
- `unhealthy.http_failures` 5; `unhealthy.tcp_failures` 2; `unhealthy.timeouts` 3.

```json
"checks": {
  "active": {
    "timeout": 5,
    "http_path": "/status",
    "host": "foo.com",
    "healthy": { "interval": 2, "successes": 1 },
    "unhealthy": { "interval": 1, "http_failures": 2 },
    "req_headers": ["User-Agent: curl/7.29.0"]
  }
}
```

Notes:
- Checks start only after a request reaches the upstream; an unused upstream is not checked.
- If no healthy node exists, APISIX still forwards to the upstream.
- Status is available at `GET /v1/healthcheck` on the Control API.

## Checked

2026-11-04. Confirmed against the APISIX health check tutorial: every active-check default in the attribute table, the example, probing starting only after a request hits the upstream, continued forwarding with no healthy node, the Control API path. Nothing removed.

Method: documentation only; no commands were run.
