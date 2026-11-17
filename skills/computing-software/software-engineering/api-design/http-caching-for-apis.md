---
id: computing-software.software-engineering.api-design.http-caching-for-apis
name: http-caching-for-apis
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, rest, http-caching, cache-control, etag, conditional-requests, cdn]
level: practitioner
status: docs-checked
description: "Make APIs cacheable with Cache-Control, ETag/Last-Modified and conditional GETs (304), Vary, private vs shared caches, CDN rules and pitfalls with authenticated data."
sources:
  - https://www.rfc-editor.org/rfc/rfc9111
  - https://www.rfc-editor.org/rfc/rfc9110#name-conditional-requests
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP caching for APIs (RFC 9111, RFC 9110)

## Cache-Control directives that matter
| Directive | Meaning |
|---|---|
| `max-age=60` | fresh for 60 s in any cache |
| `s-maxage=300` | overrides max-age for shared caches (CDN, proxies) |
| `private` | shared caches must not store it; a private cache (dedicated to a single user) may (RFC 9111) |
| `public` | shared caches may store even if the request had Authorization |
| `no-cache` | may store, but must revalidate before every use |
| `no-store` | never store (secrets, highly sensitive data) |
| `must-revalidate` | do not serve stale after expiry |
| `immutable` | content never changes, so no revalidation on reload (MDN; versioned assets) |

## Validators and conditional requests
```
GET /products/42
200 OK
ETag: "v17-3fa2"
Cache-Control: private, max-age=0, must-revalidate

GET /products/42
If-None-Match: "v17-3fa2"
304 Not Modified        (no body; client reuses its copy)
```
- **ETag:** strong (`"abc"`, byte-identical) or weak (`W/"abc"`, semantically equivalent). Derive from a version column or hash of the serialised representation - cheap to compute is the point (a version column avoids rendering the body).
- **Last-Modified / If-Modified-Since:** the date-based validator; ETag is preferred.
- Same ETags serve optimistic concurrency on writes (`If-Match`, RFC 9110 conditional requests).

## Vary
`Vary: Accept, Accept-Encoding, Accept-Language` tells caches the response differs by those headers. Missing `Vary` can serve the wrong representation (for example the wrong language or encoding). Mark per-user responses `private` instead of relying on `Vary`.

## Policy by resource type
- Per-user data (`/me`, carts): `private, no-cache` + ETag (revalidation saves bandwidth).
- Public catalogue data: `public, max-age=60, s-maxage=300`; purge or version the CDN entry on change (see your CDN's docs).
- Lists with pagination: short max-age or `no-cache` + ETag.
- Mutations (POST, PUT, DELETE and other unsafe methods): a cache must invalidate the target URI when it receives a non-error status to an unsafe request (RFC 9111 section 4.4).

## Pitfalls
- Caching authenticated responses on a CDN keyed only by URL leaks one user's data to another. Default API responses to `private` or `no-store` and opt in to public caching explicitly.
- Framework defaults vary (some add `no-cache` to everything); set headers explicitly.
- Caches may apply heuristic freshness to responses without explicit freshness information (RFC 9111); set Cache-Control explicitly.

## Verify
- [ ] `curl -sI URL` shows intended Cache-Control/ETag; second request with `-H 'If-None-Match: <etag>'` returns 304.
- [ ] CDN cache-hit ratio and `Age` header checked for public endpoints; per-user endpoints show no shared-cache hits.

## Checked
2026-11-01. Confirmed: RFC 9111 (shared vs private cache, private directive, unsafe-request invalidation, heuristic freshness), MDN HTTP Caching (immutable, Vary). The directives max-age, s-maxage, no-cache, no-store, must-revalidate, public were present in the fetched RFC 9111/MDN pages. Removed: stale-while-revalidate and stale-if-error rows, Vary: Authorization advice, CDN tag header names, Last-Modified resolution claim, 412 code.
Method: documentation only; no commands were run.
