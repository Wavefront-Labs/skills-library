---
id: computing-software.systems-network-administration.dns-dhcp.resolver-cache-sizing
name: resolver-cache-sizing
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, max-cache-size, cache-sizing, bind, unbound, resolver-performance]
level: practitioner
status: docs-checked
description: "Size resolver caches on BIND (max-cache-size) and Unbound (msg/rrset cache, slabs, threads), monitor hit rates and avoid memory exhaustion."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-max-cache-size
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/core/performance.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cache sizing

## BIND
```
options {
    max-cache-size 2g;           // or a percentage of physical memory
    max-cache-ttl 86400;         // cap TTLs (default 604800 s = one week)
    max-ncache-ttl 3600;         // negative cache cap (default 10800 s = 3 hours; cannot exceed 7 days)
};
```
The limit applies to each cache database, and by default each view has its own cache, so total memory is the
sum over all views. The default per cache is 90% of physical memory for views with recursion enabled, so
several recursive views can add up to far more than the machine has: set explicit sizes when using views.
When the limit is reached, named purges non-expired records using an LRU-based strategy.
`max-cache-ttl 0` can make queries return SERVFAIL (lost intermediate NS and glue records), so do not use it.

## Unbound
```
server:
    num-threads: 4
    msg-cache-size: 256m
    rrset-cache-size: 512m        # about twice msg-cache
    msg-cache-slabs: 4            # power of 2 near num-threads
    rrset-cache-slabs: 4
    infra-cache-slabs: 4
    key-cache-slabs: 4
    cache-min-ttl: 0
    prefetch: yes
```
Defaults are 4m for each of msg-cache-size and rrset-cache-size. Use roughly twice as much rrset cache
as msg cache. Because of malloc overhead, total memory use is likely double (or 2.5x) the configured cache
sizes. Slabs must be a power of 2 and are chosen automatically (a power of 2 close to `num-threads`) if left
unconfigured. `prefetch` refreshes popular entries in the last 10 percent of their TTL, at about 10 percent
more traffic. `unbound-control stats` reports `total.num.cachehits`, `total.num.cachemiss` and `mem.cache.rrset`.

## How big?
- Raise the sizes while watching the hit rate and memory; stop when more memory no longer helps.

## Gotchas
- Size the cache against the host or container memory limit, remembering Unbound can use 2x-2.5x the configured size.
- `cache-min-ttl` defaults to 0. Above 0 it caches data longer than the owner intended; the man page warns that
  values above an hour or so can cause trouble because cached data no longer matches the real data.

## Verify
- [ ] Memory stays below the host/container limit at peak and the cache hit ratio is stable.

## Checked
Date: 2026-10-28.
Confirmed against the BIND 9 reference (max-cache-size, max-cache-ttl, max-ncache-ttl statements), the Unbound
performance tuning page, the unbound.conf man page (cache sizes, slabs, cache-min-ttl, prefetch) and the
unbound-control man page (stat names). Removed: BIND statistics-channel counter names (not on the fetched pages),
the `9.16+` version claim, "typical enterprise/ISP" sizing figures, the 80% hit-rate target, the RRL remark and the
OOM-kill remark.
Method: documentation only; no commands were run.
