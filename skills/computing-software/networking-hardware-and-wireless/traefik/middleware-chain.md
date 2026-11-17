---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-chain
name: middleware-chain
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, chain, middleware-order, composition, reuse, middleware]
level: practitioner
status: docs-checked
description: "Compose reusable middleware stacks with the chain middleware and remember the same-namespace rule."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/chain.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware chain
`chain` combines several middlewares into one reusable unit that routers reference by name. Its single option is `middlewares`, a required list of middleware names, which must be in the same namespace as the `chain` middleware.

```yaml
http:
  routers:
    router1:
      service: service1
      middlewares:
        - secured
      rule: "Host(`mydomain`)"
  middlewares:
    secured:
      chain:
        middlewares:
          - https-only
          - known-ips
          - auth-users
    auth-users:
      basicAuth:
        users:
          - "test:$apr1$H6uskkkW$IgXLP6ewTrSuBkTrqE8wj/"
    https-only:
      redirectScheme:
        scheme: https
    known-ips:
      ipAllowList:
        sourceRange:
          - "192.168.1.7"
          - "127.0.0.1/32"
```
On Kubernetes the chain lists `- name: <middleware>` entries under `spec.chain.middlewares`.

## Checked
2026-11-03. Confirmed against the Traefik chain reference page (docs/content/reference/routing-configuration/http/middlewares/chain.md): the example, the single required `middlewares` option and the same-namespace rule. Removed: the `@provider` cross-provider claim, the ordering and circuit-breaker gotchas, the `/api/http/routers` Verify step (none on the page), and the overview page source (not read).
Method: documentation only; no commands were run.
