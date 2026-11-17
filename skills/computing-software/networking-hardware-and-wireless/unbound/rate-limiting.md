---
id: computing-software.networking-hardware-and-wireless.unbound.rate-limiting
name: rate-limiting
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, ratelimit, ip-ratelimit, ratelimit-for-domain, ratelimit-list, abuse-mitigation]
level: advanced
status: docs-checked
description: "Limit query rates in Unbound per nameserver zone with ratelimit and per client IP with ip-ratelimit, including cookies, factors and inspection commands."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rate limiting
Both are experimental and default 0 (disabled).

Per upstream zone: `ratelimit` is queries per second allowed toward each nameserver zone during recursion; excess gets SERVFAIL. Cached answers are not limited and forwarders are excluded. `ratelimit-factor` (10) lets one in N excess queries through (0 drops all); `ratelimit-backoff` (no); `ratelimit-size` (4m); `ratelimit-slabs`; `ratelimit-for-domain` and `ratelimit-below-domain` give per-name or per-suffix overrides (0 disables).

Per client: `ip-ratelimit` is queries per second per client IP; excess is dropped with no reply, checked before the cache. Clients with a valid DNS Cookie bypass it, and `ip-ratelimit-cookie` sets a separate limit, suggested at about tenfold. `ip-ratelimit-factor`, `-backoff`, `-size` and `-slabs` mirror the others.

Inspect with `unbound-control ratelimit_list [+a]` and `ip_ratelimit_list [+a]`. `ratelimit` and `ip-ratelimit` can be changed with `set_option`. Counters: `num.queries_ip_ratelimited`, `num.query.ratelimited`.

## Checked
2026-11-04. Confirmed against the unbound.conf manual and unbound-control manual: ratelimit and ip-ratelimit semantics, factor/backoff/size options, per-domain overrides, cookie bypass, tenfold suggestion, set_option support. Nothing removed.
Method: documentation only; no commands were run.
