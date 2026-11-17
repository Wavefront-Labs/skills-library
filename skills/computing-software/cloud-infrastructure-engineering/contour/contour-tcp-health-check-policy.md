---
id: computing-software.cloud-infrastructure-engineering.contour.contour-tcp-health-check-policy
name: contour-tcp-health-check-policy
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [tcpproxy, healthcheckpolicy, tcp-health-check, connect-only]
level: practitioner
status: docs-checked
description: "HTTPProxy TCP health checking under tcpproxy: connect-only checks, interval, timeout and threshold settings and defaults."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/health-checks.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy TCP health checks

For `tcpproxy` services, Envoy sends a connect-only health check to each endpoint. Place `healthCheckPolicy` directly under `tcpproxy`:

```yaml
spec:
  virtualhost:
    fqdn: health.bar.com
  tcpproxy:
    healthCheckPolicy:
      intervalSeconds: 5
      timeoutSeconds: 2
      unhealthyThresholdCount: 3
      healthyThresholdCount: 5
    services:
    - name: s1-health
      port: 80
    - name: s2-health
      port: 80
```

Parameters:
- `intervalSeconds`: seconds between checks, default 5.
- `timeoutSeconds`: wait for a response; reaching it is a failure; default 2.
- `unhealthyThresholdCount`: failed checks before a host is marked unhealthy; default 3.
- `healthyThresholdCount`: successful checks before marked healthy; during startup one success is enough.

There is no `path`, `host` or `expectedStatuses` for TCP: a successful TCP connect is healthy. These checks are implemented by Envoy and are separate from Kubernetes readiness or liveness probes.

## Checked

2026-11-04. Confirmed against the Contour upstream health checks page (config/health-checks.md): the fields, defaults, flags and behaviours stated above. Removed: the claim that a pod can be Ready yet removed from rotation (not stated).

Method: documentation only; no commands were run.
