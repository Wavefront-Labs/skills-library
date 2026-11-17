---
id: computing-software.web-development.web-performance.caching-strategies-cdn-and-http
name: caching-strategies-cdn-and-http
category: computing-software
field: web-development
product: web-performance
tags: [http-caching, cache-control, etag, cdn, invalidation, immutable, stale-while-revalidate, performance, web-development, immutable-caching, cache-busting]
level: advanced
status: docs-checked
description: "HTTP caching for real sites: Cache-Control directive combinations, ETag/conditional requests, CDN edge caching, and cache-busting with hashed filenames."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Conditional_requests
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# HTTP caching strategy — Cache-Control, ETags, and CDN layers

**Goal:** every response says exactly how long it can be reused and by whom, so
a stale page or a double-fetched asset is a deliberate choice, not an accident.

## 1. `Cache-Control` directives, read correctly
```
Cache-Control: public, max-age=31536000, immutable        # hashed static asset
Cache-Control: no-cache                                     # always revalidate, cache may still store it
Cache-Control: no-store                                     # never cache, anywhere
Cache-Control: private, max-age=0, must-revalidate           # per-user data, always check
```
`no-cache` does **not** mean "don't cache" — it means "cache it, but revalidate
with the server on every use" (via ETag/Last-Modified, below). `no-store` is the
one that actually forbids storing — the naming is the single most common
`Cache-Control` misunderstanding. `private` vs `public` controls whether a
shared cache (CDN, corporate proxy) may store it at all — any response with
per-user content (account data, personalized pricing) must be `private` or a CDN
can serve User A's cached page to User B.

## 2. The hashed-filename pattern — the only real way to cache "forever"
```
/assets/app.3f8a21.js   Cache-Control: public, max-age=31536000, immutable
```
Because the filename encodes a content hash, a new deploy produces a new
filename — the browser/CDN cache for the *old* filename is simply never
reused, no invalidation needed. `immutable` tells the browser to skip even the
revalidation check on back-navigation. This only works if the referencing HTML
(`index.html`, the entry page) is itself served with a short/no cache so
clients always get the current list of hashed asset URLs.

## 3. Conditional requests — ETag and Last-Modified
```
ETag: "a1b2c3"
→ next request: If-None-Match: "a1b2c3" → 304 Not Modified, no body sent
```
A `304` still costs a round trip but saves the response body — valuable for
large, infrequently-changing resources where you can't use a hashed filename
(user-uploaded content served from a stable URL, an API response). Weak ETags
(`W/"..."`) allow semantically-equivalent-but-byte-different responses (e.g.
different gzip compression) to still match; strong ETags require byte-identical
content.

## 4. CDN edge caching — a second cache with its own rules
A CDN (Cloudflare, Fastly, CloudFront) caches at edge locations independent of
the browser cache, and respects `Cache-Control` unless overridden by CDN-specific
rules/page-rules — check for a `s-maxage` directive, which targets *shared*
caches specifically and can differ from browser `max-age`:
```
Cache-Control: public, max-age=0, s-maxage=86400   # browser always revalidates; CDN holds 24h
```
Purging a CDN cache after a deploy (or via API/webhook on content change) is
necessary when you can't hash the URL (HTML pages, API responses) — check your
CDN's documentation for how long a purge takes to propagate and don't assume it is instant.

## 5. `stale-while-revalidate` — serve stale instantly, refresh in background
```
Cache-Control: public, max-age=60, stale-while-revalidate=86400
```
Within the `max-age` window, serve the cached copy. After it expires but within
the `stale-while-revalidate` window, still serve the (now stale) cached copy
immediately while a background fetch refreshes it for next time — users never
wait on a cache miss, at the cost of occasionally seeing slightly stale data.
Good fit for content that's fine to be a minute or two old (a homepage feed) but
bad for anything needing strict freshness (a live price).

## Checked

2026-11-01. Confirmed in MDN source (Cache-Control reference, HTTP caching guide, ETag reference, conditional requests guide): `no-cache` vs `no-store`, `private`/`public`, `s-maxage`, `stale-while-revalidate`, `max-age=31536000, immutable`, `If-None-Match` and 304, weak vs strong validation. Removed: CDN purge timing claim.

Method: documentation only; no commands were run.

## Verify
- [ ] Hashed, immutable filenames are used for all static build assets; the referencing HTML is cached short or not at all.
- [ ] Any per-user response is marked `private`, never cacheable by a shared CDN.
- [ ] `no-cache` vs `no-store` usage matches the actual intended behaviour, not assumed from the name.
- [ ] CDN purge is wired into the deploy/content-update pipeline for any non-hashed URL that can change.
- [ ] `stale-while-revalidate` is used only where briefly-stale data is acceptable.
