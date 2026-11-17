---
id: computing-software.systems-network-administration.coredns.coredns-cache-sizing-and-eviction
name: coredns-cache-sizing-and-eviction
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, cache, success, denial, capacity, eviction]
level: advanced
status: docs-checked
description: "Size the success and denial caches separately and understand shard rounding, the 1024 minimum and eviction behaviour."
sources:
  - https://coredns.io/plugins/cache/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set cache capacity and minimum TTLs per category.

```
cache [TTL] [ZONES...] {
    success CAPACITY [TTL] [MINTTL]
    denial CAPACITY [TTL] [MINTTL]
}
```

- `success` overrides settings for successful responses. CAPACITY is the packet count before eviction starts; eviction is random.
- `denial` overrides settings for denial of existence; eviction here is LRU.
- TTL overrides the maximum TTL; MINTTL overrides the minimum (default 5), which can limit queries to the backend.
- There is a third category, error, but those responses are never cached.

Size rules:
- Default capacity is 9984 per cache; the minimum allowed is 1024.
- A specified CAPACITY is rounded down to a multiple of 256 so every shard has equal size.
- Eviction is per shard, using capacity divided by 256 per shard. Shards do not fill evenly, so evictions occur before the cache is entirely full.
- Entries with 0 TTL stay until randomly evicted when a shard fills.

Example:

```
example.org {
    cache {
        success 5000
        denial 2500
    }
}
```

`disable success|denial [ZONES...]` turns off one cache; without zones it applies to all, and `disable denial sub.example.org` skips denials only for that subdomain.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/cache/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
