---
id: computing-software.cloud-infrastructure-engineering.contour.contour-http-health-check-policy
name: contour-http-health-check-policy
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [healthcheckpolicy, active-health-check, expectedstatuses, healthport, intervalseconds, unhealthythresholdcount]
level: practitioner
status: docs-checked
description: "HTTPProxy active HTTP health checks per route: path, host, interval/timeout/threshold defaults, 503 immediate eviction, expectedStatuses half-open ranges, healthPort."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/health-checks.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy HTTP health checks

Envoy performs active health checks per route, independent of Kubernetes probes.

```yaml
routes:
- conditions: [{prefix: /}]
  healthCheckPolicy:
    path: /healthy
    intervalSeconds: 5
    timeoutSeconds: 2
    unhealthyThresholdCount: 3
    healthyThresholdCount: 5
    expectedStatuses:
    - {start: 200, end: 201}
    - {start: 250, end: 300}
  services:
  - {name: s1-health, port: 80, healthPort: 8998}
  - {name: s2-health, port: 80}
```

Fields:
- `path`: endpoint probed; 200 means healthy by default.
- `host`: Host header sent; empty gives `contour-envoy-healthcheck`.
- `intervalSeconds` default 5; `timeoutSeconds` default 2; `unhealthyThresholdCount` default 3.
- `healthyThresholdCount`: successes needed to mark healthy; at startup a single success suffices.
- A backend returning 503 is marked unhealthy immediately, ignoring the unhealthy threshold, so an app can drain itself.
- `expectedStatuses`: half-open ranges (start inclusive, end exclusive) within 100 to 600. When set, 200 must be listed explicitly if it should still count as healthy (above: 200 and 250-299 are healthy).
- `services[].healthPort`: probe a different port than the routing port (the example probes 8998 on `s1-health` while traffic goes to port 80).

## Checked

2026-11-04. Confirmed against the Contour upstream health checks page (config/health-checks.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
