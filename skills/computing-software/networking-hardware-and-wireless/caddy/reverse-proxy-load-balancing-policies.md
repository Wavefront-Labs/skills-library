---
id: computing-software.networking-hardware-and-wireless.caddy.reverse-proxy-load-balancing-policies
name: reverse-proxy-load-balancing-policies
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [lb-policy, load-balancing, least-conn, round-robin, sticky-sessions, cookie, hrw, reverse-proxy]
level: practitioner
status: docs-checked
description: "Choose a reverse_proxy lb_policy: random, first, round robin, weighted, least_conn, hashes, query, header and cookie stickiness, with fallbacks and HRW hashing."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick how requests spread across upstreams.

The default is `lb_policy random`. Hashing policies use highest-random-weight hashing so the same key keeps mapping to the same upstream even when the list changes. Some policies take a block `fallback <policy>` (default fallback `random`, nestable). Example: `lb_policy header X-Upstream { fallback first }` lets developers pick a backend while everyone else gets primary/secondary failover.

Policies: `random`; `random_choose <n>` picks n at random and takes the least loaded (n usually 2); `first` uses the first available in config order (enable health checks or failover will not happen); `round_robin`; `weighted_round_robin <weights...>` with one non-negative integer per upstream, at least one above zero, so `5 1` selects the first five times in a row, and weight 0 disables new requests to that upstream; `least_conn` (random among ties); `ip_hash` (immediate peer IP); `client_ip_hash` (real client IP, best with the `servers > trusted_proxies` global option, otherwise same as ip_hash); `uri_hash` (path and query); `query [key]`; `header [field]`; `cookie [<name> [<secret>]]`.

Cookie details: first request has no cookie, so the fallback chooses and Caddy sets a cookie (default name `lb`) whose value is the upstream dial address hashed with HMAC-SHA256 using the secret (empty by default). Later requests map back if that upstream is available. For debugging you can pin an upstream by computing `hash_hmac('sha256', '10.1.0.10:8080', 'secret')` and setting it as the cookie.

## Checked
2026-11-03. Confirmed against the Caddy reverse_proxy directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
