---
id: computing-software.web-development.web-performance.cdn-purge-and-surrogate-keys
name: cdn-purge-and-surrogate-keys
category: computing-software
field: web-development
product: web-performance
tags: [http-caching, cdn-purge, surrogate-keys, cache-invalidation, cdn, fastly]
level: practitioner
status: docs-checked
description: "Invalidating CDN caches precisely: purge by URL vs surrogate keys/cache tags, s-maxage and stale-while-revalidate, tag header limits, and wiring purges into CMS and deploys."
sources:
  - https://www.fastly.com/documentation/guides/full-site-delivery/purging/working-with-surrogate-keys/
  - https://developers.cloudflare.com/cache/how-to/purge-cache/purge-by-tags/
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
  - https://www.rfc-editor.org/rfc/rfc9213
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CDN invalidation and surrogate keys

## 1. Cache long, purge precisely
For HTML and API responses that change unpredictably (CMS content, product prices), the best pattern is: long CDN TTL (`s-maxage`) + **purge on change**, with short or no browser caching:
```
Cache-Control: public, max-age=0, s-maxage=86400, stale-while-revalidate=60, stale-if-error=86400
```
Or a CDN-only header such as `CDN-Cache-Control` (RFC 9213 targeted cache control) so browsers don't see the CDN TTL.

## 2. Purge methods
| Method | Use | Limit |
|---|---|---|
| By URL | single page changed | must know every URL variant (query strings, locales, AMP, pagination) |
| By prefix/wildcard | section rebuilds | not on every CDN, can be slow |
| By **tag / surrogate key** | content-driven invalidation | header size limits (Fastly: tokens up to 1 KB, header value up to 16 KB, extra tokens ignored; Cloudflare: `Cache-Tag` header up to 16 KB, about 1,000 unique tags) |
| Purge all | emergencies, deploys of global templates | origin stampede risk |

## 3. Surrogate keys / cache tags
Origin labels each response with the entities it contains:
```
Surrogate-Key: product-123 category-shoes brand-acme template-pdp     (Fastly)
Cache-Tag: product-123,category-shoes                                  (Cloudflare; comma-separated, no spaces inside a tag)
```
When product 123 changes, purge key `product-123` - every page showing it (PDP, category lists, search landing pages) invalidates at once. Cloudflare lets you purge up to 100 tags at a time from the dashboard.

## 4. Wiring
- CMS publish webhooks -> purge API with tags; deploy pipelines purge HTML templates (static hashed assets never need purging).
- Purge APIs are authenticated and rate-limited (see your CDN's limits page) - queue and batch purges; log them.
- Verify cache keys: query string normalisation, `Vary` headers, device variants.

## Checked
2026-10-31. Confirmed against the Fastly surrogate-key page (1 KB token and 16 KB header limits, overflow ignored), the Cloudflare purge-by-tags page (`Cache-Tag` header, comma separation, 16 KB / about 1,000 tags, 100 tags per dashboard purge) and RFC 9213 (`CDN-Cache-Control`). Removed: `Surrogate-Control`, Akamai and Enterprise remarks, soft purge and request-collapsing bullets, framework mappings, `Vary: Cookie` and specific cache-status header names.
Method: documentation only; no commands were run.

## Verify
Edit content and check your CDN's cache-status response headers (MISS after the purge, then HIT) within seconds; purge logs show tag purges; origin request rate stays stable after purges.
