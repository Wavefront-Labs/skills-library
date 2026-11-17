---
id: computing-software.collaboration-platform-administration.vikunja.config-ratelimit
name: config-ratelimit
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, ratelimit-section, noauthlimit, basicauthlimit, tokenrefreshlimit, rate-limit-store]
level: practitioner
status: docs-checked
description: "Set up Vikunja rate limiting: per-user or per-IP limits, period, store backend, and the fixed limits for unauthenticated routes, token refresh and BasicAuth."
sources:
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
General limiter, off by default (`ratelimit.enabled` false):
- `kind`: `user` (default) or `ip`.
- `period` 60 seconds; `limit` 100 requests per period.
- `store`: `keyvalue` (default, follows the `keyvalue` section), `memory` or `redis`.

Separate limits that apply regardless and "cannot be disabled" for the first two:
- `noauthlimit` 10 requests per minute per IP across unauthenticated routes (login, register, password confirmation, email verification, password reset request). Change only if you know what you are doing.
- `tokenrefreshlimit` 60 per minute per IP for session renewal (token refresh and the OAuth token endpoint), kept separate so periodic renewals do not exhaust the login budget.
- `basicauthlimit` 10 failed HTTP BasicAuth attempts (CalDAV, feeds) per IP per minute before 429. Only failures count, so regular syncs are not limited.

Client IPs come from `service.ipextractionmethod`: `direct` (default) uses the TCP remote address and ignores forwarding headers; behind a proxy use `xff` (or `realip`) and set `service.trustedproxies` to the proxy CIDR ranges.

## Checked

2026-11-04: checked against config-raw.json (ratelimit section, service.ipextractionmethod, service.trustedproxies). Replaced the claim that every client shares the proxy's address with the documented extraction behaviour.

Method: documentation only; no commands were run.
