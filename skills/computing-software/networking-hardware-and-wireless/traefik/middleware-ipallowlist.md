---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-ipallowlist
name: middleware-ipallowlist
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, ipallowlist, ip-filtering, sourcerange, ipstrategy, middleware]
level: practitioner
status: docs-checked
description: "Restrict access by client IP with ipAllowList, including rejectStatusCode and how ipStrategy depth and excludedIPs pick the client address."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/ipallowlist.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware ipallowlist
`ipAllowList` accepts requests only from listed IPs or CIDR ranges. Options: `sourceRange` (required), `rejectStatusCode` (default 403) and `ipStrategy` with `depth`, `excludedIPs` and `ipv6Subnet`.

```yaml
http:
  middlewares:
    test-ipallowlist:
      ipAllowList:
        sourceRange:
          - "127.0.0.1/32"
          - "192.168.1.7"
        rejectStatusCode: 404
```
Without an `ipStrategy`, `sourceRange` is matched against the remote address of the request. `depth` takes the IP at that position from the right of `X-Forwarded-For` (0 or less is ignored; a depth beyond the number of IPs gives an empty client IP). `excludedIPs` scans `X-Forwarded-For` and selects the first IP not in the list; it is ignored when `depth` is set. `ipv6Subnet` turns a selected IPv6 address into the first address of its subnet (valid range 1-128, otherwise middleware creation fails).

Gotcha: the previous network hop is not yet in `X-Forwarded-For` when this middleware runs, so it cannot be matched against `sourceRange`.

## Checked
2026-11-03. Confirmed against the Traefik ipAllowList reference page (docs/content/reference/routing-configuration/http/middlewares/ipallowlist.md): options, defaults, default remote-address matching, depth, excludedIPs, ipv6Subnet range and the X-Forwarded-For hop caveat. Removed: the claim that a missing strategy "blocks or allows everyone" behind a load balancer, the entrypoint forwardedHeaders advice (not on this page) and the generic Verify step.
Method: documentation only; no commands were run.
