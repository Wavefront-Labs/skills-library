---
id: computing-software.database-administration.memcached.proxy-route-handlers
name: proxy-route-handlers
category: computing-software
field: database-administration
product: memcached
tags: [route-handlers, route-direct, route-failover, route-allsync, route-allfastest]
level: advanced
status: docs-checked
description: "Route handler reference: direct, null, allsync, allfastest, split, ttl, failover, random, ratelim and their options."
sources:
  - https://docs.memcached.org/features/proxy/reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

- `route_direct{child}`: one pool.
- `route_null{}`: empty response (get miss, set NOT_STORED, numerical, touch and delete NOT_FOUND).
- `route_allsync{children}`: all pools in parallel, waits for all; returns the first error else last result.
- `route_allfastest{children, miss, wait}`: first response wins; `miss=true` waits for a hit; `wait` seconds.
- `route_split{child_a, child_b}`: both, but only child_a's answer is returned.
- `route_ttl{ttl, child}`: rewrites TTL on set/add/cas/ms.
- `route_failover{children, failover_count, shuffle, miss, wait, local_zone}`: serial; `miss=true` treats misses as failures.
- `route_random{children}`.
- `route_ratelim{child, limit, fillrate, tickrate, global, fail_until_limit}`: experimental token bucket.
- `route_zfailover` is deprecated.

`children` takes a list of pool names or a `set_` name.

Pattern: reads from failover (shuffled), writes to all with allfastest or allsync for replication. Test each handler with a downed backend.

## Checked

Confirmed against the route handler reference: every handler and option listed (route_direct, route_null, route_allsync, route_allfastest, route_split, route_ttl, route_failover, route_random, route_ratelim, deprecated route_zfailover), the children argument forms, and the replication pattern against the examples page. Narrowed the route_null NOT_FOUND wording to the commands the page names.

Method: docs-checked 2026-11-09 against docs.memcached.org/features/proxy/reference/ and /examples/ (HTML converted to text and read in full).
