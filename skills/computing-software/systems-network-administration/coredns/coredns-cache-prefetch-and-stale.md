---
id: computing-software.systems-network-administration.coredns.coredns-cache-prefetch-and-stale
name: coredns-cache-prefetch-and-stale
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, cache, prefetch, serve-stale, servfail]
level: advanced
status: docs-checked
description: "Keep hot names warm with prefetch and serve expired answers with serve_stale, including verify mode and the servfail cache duration."
sources:
  - https://coredns.io/plugins/cache/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reduce latency spikes and outage impact with cache.

`prefetch AMOUNT [[DURATION] [PERCENTAGE%]]` refreshes popular items before expiry. Popular means AMOUNT queries with no gap of DURATION (default 1m) between them. Prefetch fires when TTL falls below PERCENTAGE (default 10%, range 10% to 90%, percent sign mandatory) or one second before expiry at the latest. Concurrent requests for the same entry trigger at most one background fetch.

`serve_stale [DURATION] [REFRESH_MODE [VERIFY_TIMEOUT]]` serves an expired entry if it has not been expired longer than DURATION (default 1 hour). The response TTL is 0.
- `immediate` (default): send the expired entry, then refresh in the background.
- `verify`: first check the source; can raise latency but never serves stale data if a fresh answer exists.
- VERIFY_TIMEOUT only with verify bounds the wait before falling back to stale; default 0 waits for the upstream's own timeout. Example: `serve_stale 1h verify 100ms`.

`servfail DURATION` caches SERVFAIL for DURATION. Default is 5 seconds; 0 disables it; the maximum is 5 minutes.

`keepttl` serves the original TTL instead of the aged one. Useful when authoritative; not recommended for non-authoritative records because downstream clients could use stale answers.

Metrics include `coredns_cache_prefetch_total` and `coredns_cache_served_stale_total`.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/cache/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
