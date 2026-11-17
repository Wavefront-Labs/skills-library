---
id: computing-software.web-development.web-performance.cache-keys-and-vary
name: cache-keys-and-vary
category: computing-software
field: web-development
product: web-performance
tags: [cache-key, vary-header, cdn-caching, cache-fragmentation, http-caching]
level: advanced
status: verified
description: "Designing CDN cache keys: what goes in the key, the Vary header and its pitfalls, query string and cookie normalisation, avoiding cache fragmentation and cache poisoning."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary
  - https://www.rfc-editor.org/rfc/rfc9111#name-calculating-cache-keys-with
  - https://developers.cloudflare.com/cache/how-to/cache-keys/
  - https://portswigger.net/research/practical-web-cache-poisoning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cache keys, Vary and cookies that bust caches

A cache key decides which requests share a stored response. Too broad leaks content between users; too narrow means 0% hit ratio.

## 1. Default key
Method + scheme + host + path + full query string, plus any request headers listed in the response's `Vary`. Cloudflare's documented default key is the full URL plus the client `Origin` header (for CORS), the method-override headers and the `x-forwarded-host`, `x-host`, `x-forwarded-scheme`, `x-original-url`, `x-rewrite-url` and `forwarded` headers (see its Cache keys page).

## 2. Vary
```http
Vary: Accept-Encoding          # fine: CDNs normalise to a few values
Vary: Accept                   # image format negotiation (AVIF/WebP) - normalise at the edge
Vary: Origin                   # required when Access-Control-Allow-Origin echoes the request origin
Vary: Cookie                   # usually destroys hit ratio: every user has distinct cookies
Vary: User-Agent               # thousands of variants; avoid - normalise to a device class header instead
Vary: *                        # uncacheable
```
- CDNs differ in how they treat Vary: Cloudflare now has a Vary setting in Cache Rules where you choose, per header, how it enters the cache key (the origin response must still send `Vary`; `Vary: *` always bypasses cache), plus a separate image-format feature keyed on `Accept`. Check your CDN's current docs rather than assuming it ignores Vary.
- Browsers honour Vary but keep one variant per URL in the HTTP cache (run in Chromium with `Vary: X-Foo` and `max-age=60`: requests with `X-Foo` 1, 1, 2, 2, 1 hit the server for 1, 2 and 1 again; `Vary: *` was never served from cache).
- If the response differs by a header but you forget Vary, you get wrong-content bugs (e.g. gzip served to clients that didn't ask, CORS headers for another origin).

## 3. Normalise the key
- **Query strings**: sort parameters; strip tracking params (`utm_*`, `gclid`, `fbclid`) that don't change the response; or allowlist the ones that do.
- **Cookies**: exclude cookies from the key except a specific bucket cookie (A/B variant, locale); bypass cache entirely when an auth cookie is present.
- **Headers**: derive a small set (`X-Device: mobile|desktop`, `X-Country`) at the edge and key on that.
- **Host**: www vs apex and trailing slashes - redirect to one canonical form before caching.

## 4. Cache poisoning
If the response reflects an **unkeyed** input (e.g. `X-Forwarded-Host` used to build absolute URLs, an unkeyed query param echoed into HTML), an attacker can store a malicious response for everyone. Defences: don't trust forwarding headers from clients (strip them at the edge), include anything that changes the response in the key, and never cache responses with reflected request data.

## 5. Diagnose
- Low hit ratio: check CDN analytics for top-missed URLs - usually query-string noise or cookies.
- `curl -sI -H 'Cookie: a=1'` vs without: same `Age`/HIT means cookies are excluded from the key.

## Verify
- [ ] Hit ratio for cacheable HTML/assets above target (e.g. 90% assets); no Vary: Cookie/User-Agent on cached routes; unkeyed header injection tested.
