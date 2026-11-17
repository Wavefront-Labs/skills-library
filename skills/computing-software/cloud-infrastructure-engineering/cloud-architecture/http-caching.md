---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.http-caching
name: http-caching
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, caching-strategy, http-caching, cache-control, etag, stale-while-revalidate, surrogate-control, cdn-caching-headers]
level: practitioner
status: docs-checked
description: "Set HTTP caching headers correctly: Cache-Control directives, s-maxage vs max-age, ETag/Last-Modified validation, Vary, stale-while-revalidate and private data."
sources: ["https://www.rfc-editor.org/rfc/rfc9111", "https://www.rfc-editor.org/rfc/rfc5861", "https://developer.mozilla.org/docs/Web/HTTP/Caching"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP caching headers

## Directives (RFC 9111; `stale-while-revalidate` and `stale-if-error` are RFC 5861; `immutable` is documented on MDN)
| Header | Meaning |
|---|---|
| `Cache-Control: max-age=N` | Fresh for N s in any cache |
| `s-maxage=N` | Overrides max-age for shared caches (CDN) |
| `no-cache` | May store, must revalidate before use |
| `no-store` | Never store (sensitive data) |
| `private` | Browser only, not CDN (per-user responses) |
| `public` | Shared caches may store even with Authorization |
| `immutable` | Never revalidate during freshness (fingerprinted assets) |
| `stale-while-revalidate=N` | Serve stale up to N s while refreshing in background (RFC 5861) |
| `stale-if-error=N` | Serve stale on origin errors |

## Recipes
- Fingerprinted static assets: `Cache-Control: public, max-age=31536000, immutable`.
- HTML: `Cache-Control: no-cache` + `ETag` (always revalidate, cheap 304s).
- Public API reads: `Cache-Control: public, max-age=<short>, s-maxage=<longer for the CDN>, stale-while-revalidate=<N>`.
- Personalised responses: `Cache-Control: private, no-store` (or private, max-age short).

## Validation
`ETag` (strong or `W/` weak) with `If-None-Match`, or `Last-Modified` with `If-Modified-Since`
-> `304 Not Modified`.

## Vary
`Vary: Accept-Encoding` is the common case; varying on `Cookie` or `Authorization` fragments the shared cache, so normalise or strip those instead.

## Gotchas
- Do not let shared caches store responses that carry `Set-Cookie` for a user session.
- Long max-age on non-fingerprinted URLs: can't update without purge.

## Checked
2026-10-28. Confirmed against RFC 9111 (`max-age`, `s-maxage`, `no-cache`, `no-store`, `private`, `public` and the Authorization rule, Vary), RFC 5861 (`stale-while-revalidate`, `stale-if-error`) and the MDN HTTP caching guide (`immutable`, `max-age=31536000` for fingerprinted assets, `must-revalidate`, ETag and conditional requests). Removed: the CDN cache-key remark and the fixed 30/300/60 example values. Header strings in the Recipes are illustrations built from those directives.
Method: documentation only; no commands were run.

## Verify
- [ ] `curl -I` shows expected headers; CDN shows HIT on second request for public resources.
