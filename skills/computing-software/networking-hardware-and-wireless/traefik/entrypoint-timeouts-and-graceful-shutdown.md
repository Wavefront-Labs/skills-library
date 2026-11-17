---
id: computing-software.networking-hardware-and-wireless.traefik.entrypoint-timeouts-and-graceful-shutdown
name: entrypoint-timeouts-and-graceful-shutdown
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, respondingtimeouts, gracetimeout, keepalive, transport, entrypoints]
level: practitioner
status: docs-checked
description: "Tune entrypoint respondingTimeouts, graceful shutdown lifeCycle and keep-alive limits in Traefik."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/entrypoints.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# entrypoint timeouts and graceful shutdown
Entrypoint `transport` settings control connection lifetime. `transport.respondingTimeouts` holds `readTimeout`, `writeTimeout` and `idleTimeout`. `transport.lifeCycle` holds `graceTimeOut` (how long to let in-flight requests finish at shutdown) and `requestAcceptGraceTimeout` (how long to keep accepting after a stop signal, so a load balancer can deregister). `transport.keepAliveMaxRequests` and `transport.keepAliveMaxTime` recycle long-lived connections.

```yaml
entryPoints:
  web:
    address: ":80"
    transport:
      respondingTimeouts:
        readTimeout: 60s
        idleTimeout: 180s
      lifeCycle:
        requestAcceptGraceTimeout: 5s
        graceTimeOut: 30s
```
Gotchas: defaults are `readTimeout` 60s, `writeTimeout` 0s (none), `idleTimeout` 180s, `graceTimeOut` 10s and `requestAcceptGraceTimeout` 0s. Zero means no timeout, and the responding timeouts have no effect on UDP entrypoints. `readTimeout` covers reading the entire request including the body. A router can override them with its own `respondingTimeouts`; its `readTimeout` must not be longer than its `writeTimeout`, or the router is disabled with an error. During `graceTimeOut` no new requests are accepted.

## Checked
2026-11-03. Confirmed against the Traefik entrypoints reference page and the HTTP router reference page: `transport.respondingTimeouts`, `transport.lifeCycle`, `keepAliveMaxRequests`, `keepAliveMaxTime`, their defaults, and the router `respondingTimeouts` rules. Removed: the Kubernetes `terminationGracePeriodSeconds` advice and the slow-request and SIGTERM Verify step.
Method: documentation only; no commands were run.


