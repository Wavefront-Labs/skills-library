---
id: computing-software.cloud-infrastructure-engineering.external-dns.txt-registry-caching
name: txt-registry-caching
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, txt-cache-interval, provider-cache-time, zone-list-cache, api-rate-limits]
level: practitioner
status: docs-checked
description: "Reduce ExternalDNS provider API calls with --txt-cache-interval, and tell record caching apart from zone-list caching and --provider-cache-time."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/registry/txt.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/operational-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Caching to cut provider API traffic

Three separate caches exist; do not conflate them.

1. **TXT registry cache.** The TXT registry can cache DNS records it reads from the provider, mitigating provider rate limits. Enable it with a duration:
   ```sh
   --txt-cache-interval=2m
   ```
   The migration example in the docs runs with `--txt-cache-interval=2m` and `--interval=1m`.

2. **Provider record cache.** `--provider-cache-time` caches the DNS records within a zone. Per-provider flags are in the rate-limits page.

3. **Zone list cache.** On every reconcile ExternalDNS calls the provider to enumerate zones it may manage. For accounts with many zones or strict limits this is steady API traffic even when nothing changes. Several providers support an in-memory zone list cache with a TTL. Set it to reflect how often your zones change; for most deployments zones change rarely, so `1h` or longer is appropriate.

Record caching and zone caching can be used together.

**Trade-off:** cached data can be stale, so a record changed outside ExternalDNS may be noticed only after the cache interval.

**Check:** the flag names for your provider are listed in `docs/flags.md`; confirm with `external-dns --help` for the version you run.

## Checked

2026-11-04. Read the TXT registry page (Caching), the operational best practices page (Zone list caching, flags reference link) and the rate-limits page (--provider-cache-time, --txt-cache-interval default disabled). Confirmed the three cache kinds, the 1h-or-longer guidance and the 2m/1m example values. Removed nothing.

Method: documentation only; no commands were run.
