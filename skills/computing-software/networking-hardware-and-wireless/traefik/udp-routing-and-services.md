---
id: computing-software.networking-hardware-and-wireless.traefik.udp-routing-and-services
name: udp-routing-and-services
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, udp, udp-router, loadbalancer, weighted, datagram]
level: practitioner
status: docs-checked
description: "Route UDP traffic with Traefik UDP routers and loadBalancer or weighted services; know there is no rule matching."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/udp/routing/router.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/udp/service.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/udp/routing/rules-priority.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# udp routing and services
UDP routing has far fewer features than HTTP or TCP. A UDP entrypoint is declared with an `/udp` address, a router links it to a service, and a UDP service is either a `loadBalancer` of `servers` (`address` is IP:port) or a `weighted` service; exactly one kind per service.

```yaml
entryPoints:
  dns:
    address: ":53/udp"
udp:
  routers:
    dns-router:
      entryPoints: [dns]
      service: dns-svc
  services:
    dns-svc:
      loadBalancer:
        servers:
          - address: "10.0.0.53:53"
```
Gotchas: UDP has no request, path or SNI to match on, so there is no rule and UDP routers are for now pretty much only load balancers. A UDP router without `entryPoints` is attached to all UDP entrypoints. The router keeps a session per client and backend with an inactivity timeout, configured through `entryPoints.<name>.udp.timeout`. A weighted service with a negative weight is disabled and the routers referencing it are not created.

## Checked
2026-11-03. Confirmed against the Traefik UDP router, service and rules pages: `/udp` entrypoint addresses, service kinds (loadBalancer or weighted, one per service), `address` as IP:port, the no-rules statement, sessions and timeout, and the negative-weight rule. Removed: the one-router-per-entrypoint claim, the claim about middlewares and the dig Verify step.
Method: documentation only; no commands were run.


