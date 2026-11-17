---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-inflightreq
name: middleware-inflightreq
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, inflightreq, concurrency-limit, 429, sourcecriterion, middleware]
level: practitioner
status: docs-checked
description: "Cap concurrent in-flight requests per source with inFlightReq and a source criterion; excess requests receive 429."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/inflightreq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware inflightreq
`inFlightReq` limits simultaneous in-flight requests (concurrency, not rate). `amount` (default 0) is the maximum number allowed; when that many are already in progress for the same source, the middleware answers `429 Too Many Requests`.

`sourceCriterion` defines the source: `requestHost`, `requestHeaderName`, or `ipStrategy` (`depth`, `excludedIPs`, `ipv6Subnet`). Several strategies at once is an error. If none is set, the default is `requestHost`.

```yaml
http:
  middlewares:
    limit-concurrency:
      inFlightReq:
        amount: 10
        sourceCriterion:
          ipStrategy:
            depth: 2
```
Gotchas: `ipStrategy.depth` counts from the right of `X-Forwarded-For`; a depth beyond the number of IPs gives an empty client IP, and `excludedIPs` is ignored when `depth` is set. The previous network hop is not yet in `X-Forwarded-For` when this middleware runs, so it cannot be relied on. `ipv6Subnet` groups IPv6 addresses into subnets so a new address does not bypass the limit; middleware creation fails if it is 0 or below, or above 128.

## Checked
2026-11-03. Confirmed against the Traefik inFlightReq reference page (docs/content/reference/routing-configuration/http/middlewares/inflightreq.md): amount, 429, sourceCriterion options and default, depth, excludedIPs, ipv6Subnet. Fixed: the skill said the default limit is global per router; the default criterion is `requestHost`. Removed: WebSocket/SSE slot claim and the invented Verify step.
Method: documentation only; no commands were run.
