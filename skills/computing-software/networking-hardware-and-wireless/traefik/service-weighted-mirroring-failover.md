---
id: computing-software.networking-hardware-and-wireless.traefik.service-weighted-mirroring-failover
name: service-weighted-mirroring-failover
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, weighted-service, mirroring, failover, canary, service]
level: practitioner
status: docs-checked
description: "Build weighted, mirroring and failover services (file and CRD providers) for canaries, shadow traffic and fallback backends."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/load-balancing/service.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# service weighted mirroring failover
Advanced service types compose other services (not servers). Each referenced service must be defined; for the examples below `appv1` and `appv2` are ordinary `loadBalancer` services.

`weighted` splits traffic by weight; unlike `wrr` it operates on services. `mirroring` copies requests to other services: `service` is the main one, `mirrors` lists `name` and `percent` (default 0, so no traffic is mirrored until set). The whole request is buffered in memory by default; `mirrorBody: false` omits the body (default true), `maxBodySize` (default -1, unlimited) skips mirroring bodies that are larger, and `streamBody: true` streams instead of buffering (a mirror more than 1 MiB behind is aborted; no effect when `mirrorBody` is false, cannot be combined with `maxBodySize`). `failover` forwards to a fallback when the main service is unavailable, triggered by health checks or by the `errors.status` list (single codes `"500"` or ranges `"500-504"`).

```yaml
http:
  services:
    app:
      weighted:
        services:
          - name: appv1
            weight: 3
          - name: appv2
            weight: 1
    mirrored-api:
      mirroring:
        service: appv1
        mirrors:
          - name: appv2
            percent: 10
    appv1:
      loadBalancer:
        servers:
          - url: "http://private-ip-server-1/"
    appv2:
      loadBalancer:
        servers:
          - url: "http://private-ip-server-2/"
```
Providers: `weighted` and `mirroring` are documented for the File provider and Kubernetes IngressRoute; `failover` for the File and Kubernetes CRD providers.

Gotcha: failover relies on the health check system, so HealthCheck must be enabled and working on the main service. It is not required on the failover service itself, only to propagate upwards when both main and fallback are down.

## Checked
2026-11-03. Confirmed against the Traefik HTTP service reference page (docs/content/reference/routing-configuration/http/load-balancing/service.md): weighted, mirroring and failover semantics, option defaults, supported providers, failover health check requirement. Removed: "mirrored responses are discarded" and the payments warning (not on the page), the "confirm against your version" hedge, and the Verify step.
Method: documentation only; no commands were run.
