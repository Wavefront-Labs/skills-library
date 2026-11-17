---
id: computing-software.web-development.fastify.production-recommendations
name: production-recommendations
category: computing-software
field: web-development
product: fastify
tags: [fastify, production, reverse-proxy, performance, capacity]
level: practitioner
status: docs-checked
description: "Production guidance: put a reverse proxy in front, avoid slow patterns, plan vCPU capacity, and run multiple instances."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Recommendations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use a reverse proxy (HAProxy, nginx, cloud load balancer). Exposing Node.js directly to the Internet for many domains, ports and TLS adds complexity and blocks horizontal scaling. The proxy handles TLS termination, HTTP-to-HTTPS redirect, multiple domains and static files.

Nginx forwards identity headers:

```nginx
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

Set `trustProxy` to the nginx address so Fastify uses them. HAProxy's `option http-server-close` can alleviate unexpected connection resets in Node.

Common performance degraders:
- RegExp routes and routes with many params; prefer static/simple parametric routes.
- Version constraints; async custom constraints as last resort.
- Generic middleware instead of plugins/hooks.
- Missing response schemas (slow JSON serialization).
- Ajv `allErrors: true` (also eases DoS on untrusted input).

Capacity: measure with k6 or autocannon. Rule of thumb: 2 vCPU per instance gives lowest latency (second vCPU for GC and libuv); fewer vCPU per instance maximizes throughput; 1 vCPU is fine; reports exist of 100m-200m vCPU working for API gateways.

Multiple Fastify instances in one process is fine, for example a metrics server on a separate port when a proxy or firewall is not an option; each instance only costs its traffic and memory.

Gotcha: Fastify listens on `127.0.0.1` by default, and a Kubernetes `readinessProbe` uses the pod IP, so it cannot reach the app; listen on `0.0.0.0` or set a custom hostname in `readinessProbe.httpGet`.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Recommendations.md) and confirmed. Removed or corrected: the Kubernetes gotcha now states the documented cause; the invented autocannon Verify step.

Method: documentation only; no commands were run.
