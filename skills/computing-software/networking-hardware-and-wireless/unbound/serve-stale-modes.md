---
id: computing-software.networking-hardware-and-wireless.unbound.serve-stale-modes
name: serve-stale-modes
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, serve-expired, rfc8767, serve-expired-client-timeout, stale-data, resilience]
level: practitioner
status: docs-checked
description: "Choose between classic serve-expired and RFC 8767 mode in Unbound, and set the TTL and client-timeout options that select between them."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/core/serve-stale.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# serve stale modes
Two modes:
- Classic serve-expired (since 1.6.0): return an expired record immediately and refresh in the background. Favours cache-hit ratio and client speed.
- RFC 8767 mode (added in 1.11.0, default since 1.23.0): resolve normally and use the expired record only as a fallback when resolution runs past a time limit or would return SERVFAIL.

Options:
- `serve-expired: yes` (manual default no) enables it.
- `serve-expired-ttl` (86400 s) maximum age to serve; 0 means no limit. RFC 8767 suggests one to three days.
- `serve-expired-reply-ttl` (30 s) TTL on stale answers, capped by the original TTL.
- `serve-expired-client-timeout` (1800 ms): 0 gives classic behaviour; above 0 enables RFC mode.
- `serve-expired-ttl-reset` (no) resets expired records to the serve-expired-ttl after a failed refresh.

The page calls RFC mode the safest approach for availability, network or configuration failures; choose classic when client performance matters more, with `prefetch`. Stale answers may send clients to outdated destinations. Counter `num.expired` shows stale replies.

## Checked
2026-11-04. Confirmed against the serve-stale topic page, the unbound.conf manual and the unbound-control statistics list: version statements (1.6.0, 1.11.0, 1.23.0), option defaults and the closing recommendation. Nothing removed.
Method: documentation only; no commands were run.
