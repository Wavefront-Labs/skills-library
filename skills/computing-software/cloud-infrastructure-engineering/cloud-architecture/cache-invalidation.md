---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cache-invalidation
name: cache-invalidation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, caching-strategy, cache-invalidation, ttl-design, cache-busting, stale-while-revalidate]
level: practitioner
status: docs-checked
description: "Design cache invalidation and TTLs across CDN and application caches: versioned file names, invalidation, delete-on-write and stale-while-revalidate."
sources: ["https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html", "https://www.rfc-editor.org/rfc/rfc5861", "https://learn.microsoft.com/azure/architecture/patterns/cache-aside", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cache invalidation and TTL design

## Strategies
1. **Versioned file names (cache busting)** for static assets: a content hash in the file name (`app.3f9a2c.js`) means a deploy publishes a new name and nothing needs invalidating. CloudFront recommends versioning as the primary approach for frequently updated files: an invalidated file may still be served from a viewer's browser or a corporate proxy cache until it expires there, versioning makes it easier to analyse changes in access logs, lets you serve different versions to different users, simplifies rolling forward and back, and avoids invalidation charges.
2. **TTL-based expiry**: pick the TTL from tolerable staleness, not habit. A TTL does not guarantee a value is fresh; it bounds how stale it can get, and an expired key is treated as a miss and refetched from the database (ElastiCache caching strategies).
3. **Explicit invalidation**: a CDN invalidation removes a file from edge caches before it expires; the next viewer request returns to the origin for the latest version. Check your CDN's current limits and charges on its own pages.
4. **Event-driven invalidation** for application caches: write to the data store first, then invalidate (delete) the cached item; the next read reloads it. Updating the store before removing the cache entry matters: removing first lets a reader repopulate the cache with the outdated value (Azure Cache-Aside pattern). Or consume change events from the store to invalidate.
5. **Serve stale** with RFC 5861 extensions: `stale-while-revalidate=<seconds>` lets a cache serve a stale response while it revalidates in the background, and `stale-if-error=<seconds>` lets it return a stale response when an error (such as a 500 or a network or DNS failure) occurs, which improves availability.
6. **Write-through plus TTL**: write-through keeps cache data current but fills the cache with data that is never read; adding a TTL limits that waste.

## Gotchas
- Invalidating on every deploy instead of versioning assets sends viewers back to the origin and leaves old copies in downstream caches.
- Updating the cache on write races with concurrent readers; delete the cached item instead and let the next read reload it.
- Cache-aside does not guarantee consistency: an external process can change the store at any time and the cache shows it only after the item reloads.

## Verify
- [ ] TTL per content type documented with the staleness rationale.
- [ ] Origin load during invalidation or deploy tested.

## Checked
2026-11-08. Confirmed on the CloudFront invalidation page (invalidate vs versioning and its five reasons), RFC 5861 (stale-while-revalidate, stale-if-error definitions), the Azure Cache-Aside pattern page (invalidate on write, ordering note, consistency caveat) and the ElastiCache caching strategies page (TTL, write-through trade-offs). Removed: the CloudFront free-path and wildcard-per-path pricing claims (the fetched page text omits them, and prices are not kept), Front Door, Cloud CDN, Fastly and Cloudflare purge claims, example TTLs by content type, and the claim that purges cause origin spikes. RFC 9111 was dropped from sources because no claim relies on it.
Method: documentation only; no commands were run.
