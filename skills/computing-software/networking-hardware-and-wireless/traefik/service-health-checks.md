---
id: computing-software.networking-hardware-and-wireless.traefik.service-health-checks
name: service-health-checks
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, healthcheck, passivehealthcheck, unhealthyinterval, grpc, service]
level: practitioner
status: docs-checked
description: "Add active health checks and passive failure detection to Traefik services and propagate status through parent services."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/load-balancing/service.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# service health checks
The active `healthcheck` option removes unhealthy servers from the load balancing rotation. HTTP(S) servers are healthy while the check returns a status between `2XX` and `3XX`, or the configured `status`; gRPC servers are healthy while they return SERVING to gRPC health check v1 requests.

Options: `path` (required; relative URL), `scheme`, `mode` (`grpc` to use the gRPC protocol; default http), `hostname` (Host header value), `port`, `interval` (default 30s, for healthy targets), `unhealthyInterval` (for unhealthy targets; defaults to `interval`), `timeout` (default 5s), `headers`, `followRedirects` (default true), `method` (default GET) and `status` (expected code).

```yaml
http:
  services:
    my-service:
      loadBalancer:
        healthCheck:
          path: /health
          interval: 10s
          timeout: 3s
        passiveHealthCheck:
          failureWindow: 3s
          maxFailedAttempts: 3
        servers:
          - url: "http://10.0.0.11:8080"
```
`passiveHealthCheck` uses real traffic: when `maxFailedAttempts` (default 1) consecutive failures happen within `failureWindow` (default 10s), Traefik stops routing to that server. The server is considered healthy again after the failure window has passed.

Gotcha: to propagate status changes (for example all servers of a service are down) upwards, HealthCheck must also be enabled on the parent services (weighted, mirroring, failover).

## Checked
2026-11-03. Confirmed against the Traefik HTTP service reference page (docs/content/reference/routing-configuration/http/load-balancing/service.md): health check and passive health check options, defaults, healthy-status rules, parent propagation. Removed: "all servers unhealthy gives 503" (not on the page) and the invented Verify step.
Method: documentation only; no commands were run.
