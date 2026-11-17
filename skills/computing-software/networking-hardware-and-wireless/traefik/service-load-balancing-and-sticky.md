---
id: computing-software.networking-hardware-and-wireless.traefik.service-load-balancing-and-sticky
name: service-load-balancing-and-sticky
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, service, loadbalancer, wrr, p2c, hrw, leasttime, sticky]
level: practitioner
status: docs-checked
description: "Configure an HTTP service with strategy wrr, p2c, hrw or leasttime, weights, sticky cookies and passHostHeader."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/load-balancing/service.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# service load balancing and sticky
An HTTP service holds a `loadBalancer` with `servers`. Strategies: `wrr` (weighted round robin, default), `p2c` (power of two choices), `hrw` (highest random weight) and `leasttime`. Each server has `url`, optional `weight` and `preservePath`.

```yaml
http:
  services:
    app-svc:
      loadBalancer:
        strategy: wrr
        passHostHeader: true
        sticky:
          cookie:
            name: sticky-cookie
        servers:
          - url: "http://10.0.0.11:8080"
            weight: 2
          - url: "http://10.0.0.12:8080"
```
Other fields: `serversTransport` (named TLS and timeouts profile) and `responseForwarding.flushInterval`.

Gotchas: `sticky` sets a Set-Cookie header on the initial response so the client knows which server handled it. `p2c` selects two random servers and uses the one with fewer active connections, `hrw` uses consistent hashing based on client IP, and `leasttime` favours the lowest response time combined with the fewest active connections. `flushInterval` defaults to 100ms, a negative value flushes after each write, and streaming responses are flushed immediately. `passHostHeader` defaults to true, and `serversTransport` defaults to `default@internal`.

## Checked
2026-11-03. Confirmed against the Traefik HTTP service (load balancing) reference page: strategies and default, server fields, `sticky`, `passHostHeader`, `serversTransport`, `responseForwarding.flushInterval`. Removed: the claim that sticky cookies are lost on unhealthy servers, the version hedge and the cookie-jar Verify step.
Method: documentation only; no commands were run.


