---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-ratelimit
name: middleware-ratelimit
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, ratelimit, rate-limiting, token-bucket, sourcecriterion, redis, middleware]
level: practitioner
status: docs-checked
description: "Throttle requests per source with the rateLimit middleware: average, period, burst, sourceCriterion and optional Redis for distributed limits."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/ratelimit.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware ratelimit
`rateLimit` implements a token bucket. `average` and `period` define the rate at which the bucket refills (average divided by period; `period` defaults to 1s; `average: 0`, the default, means no rate limiting). `burst` (default 1) is the maximum number of requests allowed to go through at the very same moment.

```yaml
http:
  middlewares:
    api-limit:
      rateLimit:
        average: 100
        period: 1s
        burst: 50
        sourceCriterion:
          ipStrategy:
            depth: 1
```
`sourceCriterion` groups requests by source: `requestHost`, `requestHeaderName`, or `ipStrategy` (`depth`, `excludedIPs`, `ipv6Subnet`). Setting several strategies is an error; with none set, the request's remote address is used. A `redis` block (`endpoints` default `localhost:6379`, plus `username`, `password`, `db`, `poolSize`, `minIdleConns`, `maxActiveConns`, `readTimeout`, `writeTimeout`, `dialTimeout` and `tls`) enables distributed limiting across Traefik instances; without it, storage is in memory and per instance.

Gotchas: `ipStrategy.depth` counts from the right of `X-Forwarded-For`. The previous network hop is not yet in that header when the middleware runs, so it cannot be relied on. `excludedIPs` does not exempt IPs from limiting; it only helps choose the client IP, and is ignored when `depth` is set. `ipv6Subnet` groups IPv6 clients into subnets so a new address does not bypass the limit.

## Checked
2026-11-03. Confirmed against the Traefik ratelimit reference page (docs/content/reference/routing-configuration/http/middlewares/ratelimit.md): token bucket, average/period/burst defaults and meanings, sourceCriterion options and default, redis options and defaults, in-memory fallback, depth, excludedIPs and ipv6Subnet behaviour. Removed: the invented "429" load-test Verify step and the claim that burst is "beyond the rate".
Method: documentation only; no commands were run.
