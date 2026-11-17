---
id: computing-software.networking-hardware-and-wireless.traefik.router-options-and-multilayer-routing
name: router-options-and-multilayer-routing
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, router, parentrefs, multi-layer-routing, tls, respondingtimeouts]
level: practitioner
status: docs-checked
description: "Use router options (entryPoints, middlewares, tls, observability, timeouts) and parentRefs multi-layer routing in Traefik."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/routing/router.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/routing/multi-layer-routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# router options and multilayer routing
A router connects a matching request to a service. Options: `entryPoints` (default: all), `rule`, `priority`, `middlewares`, `service`, `tls` (`certResolver`, `options`, `domains`), `observability` (`traceVerbosity` of minimal or detailed) and `respondingTimeouts` (`readTimeout` must not exceed `writeTimeout`).

```yaml
http:
  routers:
    app:
      entryPoints: [websecure]
      rule: "Host(`app.example.com`)"
      middlewares: [secured]
      service: app-svc
      tls:
        certResolver: myresolver
        options: modern
```
Multi-layer routing uses `parentRefs`: a child router references its parent routers. A request matches the parent router first, the parent's middlewares (for example ForwardAuth) run, and the modified request is then evaluated by the child routers.

Gotchas: middlewares are applied in the order they are declared. A router `respondingTimeouts` value replaces the entrypoint one, longer or shorter, and only one router per branch of a multi-layer tree can define it, otherwise the router is disabled with an error. A router `readTimeout` longer than the entrypoint's weakens its protection against slow clients for the whole entrypoint.

## Checked
2026-11-03. Confirmed against the Traefik HTTP router and multi-layer routing reference pages: router options, `entryPoints` default, middleware order, `respondingTimeouts` rules and the `parentRefs` flow. Removed: the `@` router-name claim (confirmed only for TCP elsewhere), the default-certificate claim, the version hedge and the API Verify step.
Method: documentation only; no commands were run.


