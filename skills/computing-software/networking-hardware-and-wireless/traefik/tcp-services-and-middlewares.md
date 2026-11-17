---
id: computing-software.networking-hardware-and-wireless.traefik.tcp-services-and-middlewares
name: tcp-services-and-middlewares
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, tcp-service, inflightconn, ipallowlist, tcp-healthcheck, tcp-middleware]
level: practitioner
status: docs-checked
description: "Define TCP load balancer services with send and expect health checks and protect them with inFlightConn and ipAllowList middlewares."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/tcp/service.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/tcp/middlewares/inflightconn.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/tcp/middlewares/ipallowlist.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tcp services and middlewares
A TCP service is a `loadBalancer` of `servers` with `address` values (host:port). Its `healthCheck` takes `send`, `expect`, `interval` and `timeout`, and it can use a named `serversTransport`.

```yaml
tcp:
  services:
    my-service:
      loadBalancer:
        servers:
          - address: "10.0.0.20:6379"
        healthCheck:
          send: "PING"
          expect: "PONG"
          interval: "10s"
          timeout: "3s"
  middlewares:
    limit-conns:
      inFlightConn:
        amount: 10
```
`inFlightConn` caps simultaneous connections per source IP. The TCP `ipAllowList` middleware takes a `sourceRange` list of IPs or CIDRs.

Gotchas: `inFlightConn` closes the connection if there are already `amount` connections open (`amount` is required and has no useful default of 0). The health check `send` and `expect` strings in the example suit a Redis-like backend; set them to match your protocol.

## Checked
2026-11-03. Confirmed against the Traefik TCP service, inFlightConn and ipAllowList reference pages: server `address`, `healthCheck` fields (`send`, `expect`, `interval`, `timeout`), `serversTransport`, `inFlightConn.amount` and `sourceRange`. Removed: the exactly-one-kind claim, the probe warning and the connection-count Verify step.
Method: documentation only; no commands were run.


