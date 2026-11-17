---
id: computing-software.networking-hardware-and-wireless.bind9.cache-prefetch-and-serve-stale
name: cache-prefetch-and-serve-stale
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, prefetch, serve-stale, max-cache-ttl]
level: advanced
status: docs-checked
description: "Tune the BIND 9 cache: max-cache-ttl, max-ncache-ttl, prefetch, and stale answers with stale-answer-enable."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cache prefetch and serve stale
Cache limits: `max-cache-ttl` (default 1 week), `max-ncache-ttl` (default 3 hours), `max-cache-size`.

`prefetch` refreshes a cached record when a query hits it with a remaining TTL at or below the trigger. The trigger is 1 to 10 seconds (default 2; 0 disables). An optional second value is the eligibility TTL, the smallest original TTL for which prefetch applies (default 9).

Stale answers are returned from expired cache when a zone's name servers are not answering. `stale-answer-enable` also needs `stale-cache-enable`; the default is not to serve stale. Settings:

- `stale-answer-enable yes`
- `stale-cache-enable yes`
- `stale-answer-ttl` (default 30)
- `stale-refresh-time` (default 30)

`rndc serve-stale` switches the behaviour at runtime.

## Checked

2026-11-04. Read the BIND 9 Administrator Reference Manual (reference) entries for max-cache-ttl, max-ncache-ttl, prefetch, stale-answer-enable, stale-cache-enable, stale-answer-ttl, stale-refresh-time and rndc serve-stale; defaults and the stale-cache-enable requirement confirmed. Nothing was removed.

Method: documentation only; no commands were run.
