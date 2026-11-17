---
id: computing-software.networking-hardware-and-wireless.squid.collapsed-forwarding
name: collapsed-forwarding
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, collapsed-forwarding, concurrent-requests, cache-miss]
level: advanced
status: docs-checked
description: "Merge concurrent requests for the same URI with collapsed_forwarding so only the first goes upstream."
sources:
  - https://www.squid-cache.org/Doc/config/collapsed_forwarding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# collapsed_forwarding
Default `off`. When on, Squid merges concurrent requests for the same URI before knowing if the response is cacheable; only the first is sent, the rest wait and reuse it if cacheable.

Caveats:
- Off by default because collapsing can delay requests that turn out uncacheable; it helps highly cacheable content with grouped expiry.
- Revalidation collapsing is disabled for SMP-aware caches and Vary-controlled objects.
- Reused responses are treated as fresh: no `refresh_pattern` or freshness checks, though `send_hit` still applies.

## Checked

2026-11-04. Read the collapsed_forwarding directive page and confirmed the default, the merge behaviour, the reasons it is off by default, the SMP and Vary limit and the freshness and send_hit notes. Nothing was removed.

Method: documentation only; no commands were run.
