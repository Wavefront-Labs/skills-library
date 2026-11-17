---
id: computing-software.systems-network-administration.pi-hole.dns-cache-tuning
name: dns-cache-tuning
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [dns-cache-size, cache-optimizer, upstream-blocked-ttl]
level: advanced
status: docs-checked
description: "Tune Pi-hole's DNS cache size, stale-record optimizer, upstream-blocked TTL and cached record types."
sources: ["https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DNS cache tuning

All options live under `[dns.cache]`.

**size** (default `10000`). Expiring entries make room over time. Too high hurts: more memory, and lookup speed degrades in the 10,000+ range. dnsmasq may warn above 10,000 entries.

**optimizer** (default `3600` seconds). If a cached record expired only recently, Pi-hole still serves it and triggers a refresh from upstream. This lowers delays on unreliable connections but may return out-of-date data and makes the cache mostly least-recently-used. The docs strongly recommend staying below `86400` (one day). Zero serves stale data regardless of how long it has expired, which is not recommended. Any negative value disables the feature.

**upstreamBlockedTTL** (default `86400`). TTL used for queries blocked upstream; after it expires the query is forwarded again to check whether the block is still valid. Zero disables caching of upstream-blocked queries.

**rrtype** (default `ANY`). dnsmasq's `--cache-rr` option: a comma-separated list of record types to cache. `ANY` caches all types.

**Related.** `dns.localise` (default `true`) is dnsmasq's `localise-queries`; when disabled, all possible values for local records are returned.

**Checklist**

1. Keep `optimizer` well below 86400; zero serves stale data indefinitely.
2. Remember that `size` above 10,000 can slow lookups and make dnsmasq warn.

## Checked

2026-11-03. Read the `[dns.cache]`, `dns.localise` sections of the FTL configuration reference: size 10000 with the 10,000+ note, optimizer 3600 with the 86400 recommendation, zero and negative behaviour, upstreamBlockedTTL 86400, rrtype ANY, localise true. Replaced the invented checklist (evictions in statistics, testing advice) with statements from the page.

Method: documentation only; no commands were run.
