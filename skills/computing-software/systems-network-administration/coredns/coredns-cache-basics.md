---
id: computing-software.systems-network-administration.coredns.coredns-cache-basics
name: coredns-cache-basics
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, cache, ttl, frontend, zones]
level: intro
status: docs-checked
description: "Enable the cache plugin with its TTL cap, zone list and default size, and know that TTL only caps duration, never extends it."
sources:
  - https://coredns.io/plugins/cache/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: cache answers in front of an expensive backend.

Syntax: `cache [TTL] [ZONES...]`. With cache enabled, everything except zone transfers and metadata records is cached for up to 3600s. The plugin can be used only once per server block and passes DNSSEC DO options through for upstream queries.

TTL facts:
- Without a TTL argument the maximum is 3600 for NOERROR responses and 1800 for denial of existence ones.
- `cache 300` caps entries at 300 seconds.
- The TTL only caps; it never extends. A record with a 30s TTL stays 30s even under `cache 600`.
- The minimum cache duration defaults to 5 seconds and can be changed via MINTTL in success or denial.

Zones: if empty, the zones of the server block are used. `cache example.org` caches only that domain.

Size: the cache has 256 shards of 39 items by default, 9984 items in total.

Examples:

```
. {
    cache 10
    whoami
}
. {
    forward . 8.8.8.8:53
    cache example.org
}
```

Cached error responses (SERVFAIL aside, see the servfail option) are never cached.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/cache/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
