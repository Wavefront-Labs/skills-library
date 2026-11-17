---
id: computing-software.web-development.web-performance.debugging-cache-behaviour
name: debugging-cache-behaviour
category: computing-software
field: web-development
product: web-performance
tags: [cache-debugging, cache-status-header, cf-cache-status, cdn-hit-ratio, http-caching]
level: practitioner
status: docs-checked
description: "Diagnosing browser and CDN caching: reading Cache-Control, Age, ETag and Vary, Cache-Status and cf-cache-status headers, common BYPASS causes."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching
  - https://www.rfc-editor.org/rfc/rfc9211
  - https://developers.cloudflare.com/cache/concepts/cache-responses/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Debugging cache behaviour

## 1. Read the headers
```bash
curl -sI https://example.com/assets/app.3f9a.js | grep -iE "cache-control|age|etag|last-modified|vary|expires|cache-status|cf-cache-status"
curl -sI https://example.com/ ; sleep 5 ; curl -sI https://example.com/    # Age should increase on a cache hit
```
| Header | Meaning |
|---|---|
| `Cache-Control` | policy from origin (max-age, s-maxage for shared caches, no-store, private) |
| `Age` | seconds the object has been in the shared cache. Cloudflare sets it on HIT, STALE and UPDATING, not on MISS, DYNAMIC or BYPASS |
| `ETag` / `Last-Modified` | validators for 304 revalidation |
| `Vary` | request headers that split the cache key |
| `Cache-Status` (RFC 9211) | standard per-cache hit/miss detail |
| `cf-cache-status` | Cloudflare: HIT, MISS, EXPIRED, STALE, BYPASS, REVALIDATED, UPDATING, DYNAMIC, NONE/UNKNOWN |

Other CDNs use their own status headers; check the vendor's documentation.

## 2. Why it is not cached
- Cloudflare BYPASS causes: `Cache-Control: no-store` or `private`; a `Set-Cookie` response header; `Vary: *`; a response over the plan's maximum cacheable size; an `Authorization` request header (when Origin Cache Control is enabled, cacheable only if `Cache-Control` also has `public`, `s-maxage` or `must-revalidate`).
- Cloudflare `DYNAMIC`: the asset is not a default cached file type (for example HTML or JSON) and no Cache Rule makes it eligible.
- Cache key fragmentation: `Vary: User-Agent` has so many variations that cache reuse drops (MDN); for cookie-personalised content use `Cache-Control: private` instead of varying on a cookie.

## 3. Browser side
Use the browser DevTools Network panel to see whether a response came from cache or was revalidated (status `304`), and make sure cache-disabling is off while testing.

## 4. Process
1. Confirm origin headers (`curl` the origin directly, bypassing the CDN).
2. Confirm CDN rules/cache key settings for that path.
3. Request twice from the same location; check status/Age.
4. After purge, verify MISS then HIT.
5. Track hit ratio per path in CDN analytics; investigate drops after deploys.

## Verify
- [ ] Hashed static assets: `HIT` with large `Age` and `max-age=31536000, immutable`; HTML policy deliberate (short/stale-while-revalidate or bypass).

## Checked
2026-11-01. Confirmed against the Cloudflare cache responses page (status values, Age behaviour, BYPASS and DYNAMIC causes), RFC 9211 (Cache-Status) and the MDN HTTP caching guide (Vary, immutable, max-age=31536000). Removed: x-cache and x-vercel-cache values, per-CDN details, DevTools label specifics, utm query-string and method claims.
Run 2026-11-01 against example.com (served by Cloudflare): `curl -sI` showed `Age` and `cf-cache-status: HIT`, and two HEAD requests 5 s apart on one connection showed Age rising 1840 to 1845, as the skill says. The BYPASS, DYNAMIC and Vary causes, and `Cache-Status`, cannot be provoked on a site we do not control (the response had no Cache-Control, Vary, ETag or Cache-Status), so they stay documentation-only; the skill stays docs-checked.
Method: documentation plus the header-reading commands run.
