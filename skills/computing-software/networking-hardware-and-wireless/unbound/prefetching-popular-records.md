---
id: computing-software.networking-hardware-and-wireless.unbound.prefetching-popular-records
name: prefetching-popular-records
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, prefetch, prefetch-key, cache-hit-ratio, latency]
level: practitioner
status: docs-checked
description: "Refresh popular cache entries before they expire in Unbound with prefetch and prefetch-key, and the extra load they cost."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/core/serve-stale.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# prefetching popular records
`prefetch: yes` (default no) refreshes popular items when they are in the last 10% of their TTL, at about 10% extra upstream load. The serve-stale page describes the same trigger as a record's TTL falling within 10% of the original.

`prefetch-key: yes` (default no) fetches DNSKEYs earlier in validation, when a DS record is encountered, lowering latency at the cost of slightly more CPU. The manual says it has no use if the cache is set to 0.

Both can be changed at runtime with `unbound-control set_option` without a reload.

Counters: `num.prefetch` counts prefetches and is included in `num.cachehits` (the client got a cached answer); it is not counted in `num.recursivereplies` or `num.cachemiss`.

The serve-stale page says using prefetch together with serve-expired is "highly recommended" to keep an updated cache; its serve-expired example enables prefetch too. See serve-stale-modes.

## Checked
Method: 2026-11-08 read the unbound.conf, serve-stale and unbound-control pages. Claims were broadly right; replaced "needs the cache enabled" detail with the manual's actual prefetch-key behaviour, softened the serve-stale recommendation to its wording, and added the counter detail.
