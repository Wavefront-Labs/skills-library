---
id: computing-software.networking-hardware-and-wireless.traefik.api-and-dashboard-security
name: api-and-dashboard-security
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, api, dashboard, insecure, basepath, debug]
level: practitioner
status: docs-checked
description: "Expose the Traefik API and dashboard safely, avoiding api.insecure on public networks by routing api@internal behind auth."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/api-dashboard.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# api and dashboard security
Install options under `api`: `dashboard`, `debug`, `disableDashboardAd`, `basePath` (incompatible with `insecure`) and `insecure`. With `api.insecure: true` the API and dashboard are enabled on the entrypoint named `traefik` (port 8080 by default).

Safer pattern: leave `insecure` off and, as the reference describes, set up a router attached to the `api@internal` service with a middleware you define (`admin-auth` here).

```yaml
api:
  dashboard: true
http:
  routers:
    dashboard:
      rule: "Host(`traefik.example.com`)"
      service: api@internal
      middlewares: [admin-auth]
      entryPoints: [websecure]
      tls: {}
```
Gotchas: `api.debug` enables additional endpoints for debugging and profiling (`/debug/vars` and the `/debug/pprof/` set). The dashboard is at `/dashboard/` by default and the trailing slash is mandatory. All API endpoints are read with GET; `/api/rawdata` returns the dynamic configurations, errors, status and dependency relations.

## Checked
2026-11-03. Confirmed against the Traefik API and dashboard reference page: `api.dashboard`, `api.debug`, `api.disableDashboardAd`, `api.basePath` and `api.insecure` (basePath and insecure are incompatible), the `traefik` entrypoint, `api@internal` routing, the debug endpoints, the mandatory trailing slash and `/api/rawdata`. Removed: the unauthenticated 401 Verify step and the claims that insecure mode exposes the whole routing table to anyone.
Method: documentation only; no commands were run.


