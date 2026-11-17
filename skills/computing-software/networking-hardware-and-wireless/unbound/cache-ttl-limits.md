---
id: computing-software.networking-hardware-and-wireless.unbound.cache-ttl-limits
name: cache-ttl-limits
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, cache-max-ttl, cache-min-ttl, negative-ttl, serve-original-ttl, ttl]
level: practitioner
status: docs-checked
description: "Clamp cached TTLs in Unbound with cache-max-ttl, cache-min-ttl and the negative TTL limits, and serve original TTLs instead of decremented ones."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cache ttl limits
- `cache-max-ttl` (86400 s) upper limit on TTL for cached RRsets and messages.
- `cache-min-ttl` (0, disabled) lower limit; the manual warns that raising it can cause stale data.
- `cache-max-negative-ttl` (3600 s) upper limit for NXDOMAIN and NODATA answers.
- `cache-min-negative-ttl` (0, disabled) lower limit for negative answers; setting 1 honours the upstream TTL.
- `serve-original-ttl: yes` (default no) returns the upstream TTL rather than the decrementing cache TTL, and disables min/max TTL enforcement.
- `val-bogus-ttl` (60 s) applies to bogus data.

`cache-max-ttl`, `cache-min-ttl` and `cache-max-negative-ttl` can be changed at runtime with `unbound-control set_option`.

Remove entries with `flush`, `flush_type`, `flush_zone` or `flush_negative`; see unbound-control-cache-inspection-and-flushing.

## Checked
2026-11-04. Confirmed against the unbound.conf manual and unbound-control manual: TTL option defaults, serve-original-ttl note (min/max TTL not enforced), and that cache-max-ttl, cache-min-ttl and cache-max-negative-ttl are in the set_option list. Nothing removed.
Method: documentation only; no commands were run.
