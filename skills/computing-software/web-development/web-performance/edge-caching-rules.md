---
id: computing-software.web-development.web-performance.edge-caching-rules
name: edge-caching-rules
category: computing-software
field: web-development
product: web-performance
tags: [edge-caching, cloudflare-cache-rules, cdn-caching, edge-compute, vercel-caching]
level: advanced
status: docs-checked
description: "Caching HTML and APIs at the edge: s-maxage, stale-while-revalidate, CDN-Cache-Control (RFC 9213), Vercel CDN headers, Cloudflare Cache Rules and a personalisation checklist."
sources:
  - https://developers.cloudflare.com/cache/how-to/cache-rules/
  - https://vercel.com/docs/edge-cache
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
  - https://www.rfc-editor.org/rfc/rfc9213
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Edge caching rules and edge compute

Caching static assets at a CDN is easy; the big TTFB wins come from caching HTML and API responses at the edge without leaking personalised content.

## 1. Header contract
```http
Cache-Control: public, max-age=0, s-maxage=300, stale-while-revalidate=86400
CDN-Cache-Control: max-age=300          # RFC 9213 targeted field: same syntax as Cache-Control, aimed at CDNs
Vercel-CDN-Cache-Control: max-age=3600  # Vercel's cache only
```
- `s-maxage` sets freshness in shared caches and is ignored by private caches.
- `CDN-Cache-Control` controls the Vercel CDN or another CDN separately from the browser; `Vercel-CDN-Cache-Control` affects only Vercel's cache, neither is returned to the browser.
- On Vercel, if you set `Cache-Control` without `CDN-Cache-Control`, the CDN strips `s-maxage` and `stale-while-revalidate` before responding to the browser.
- `no-store` stops any cache storing the response; `private` limits it to a private cache. Use one for anything personalised.

## 2. Cloudflare
- Cache Rules set what is eligible to cache, for how long and where, per matching request. They need the DNS record proxied through Cloudflare, can be created in the dashboard, API or Terraform, and per-plan rule limits are on the Cache Rules page. Read its docs for the exact match fields and TTL options before copying a rule.
- Bypass the cache for requests that carry a session; decide the match expression from your own cookie names.

## 3. Vercel
- Check `x-vercel-cache` to see whether a response came from the cache. A `Vary` header only matters together with caching directives such as `s-maxage`; a `Vary` key the origin sends can stop a route being cached (`MISS`).

## 4. Safe HTML caching checklist
- Strip or vary on everything that personalises: cookies, `Authorization`, geolocation, A/B buckets.
- Do not cache responses that set cookies unless you have confirmed your CDN's behaviour.
- Logged-in pages: bypass, or cache the shell and fetch personalised fragments client-side.
- CSRF tokens embedded in cached HTML are shared across users: fetch them separately.

## 5. Verify at the edge
```bash
curl -sI https://example.com/blog/post
```
Look at the cache-status response headers your CDN documents (on Vercel, `x-vercel-cache`) and check hit ratio in the CDN analytics.

## Verify
- [ ] Anonymous HTML served from edge with a hit status; logged-in requests bypass; personalised responses never cached; purge works on publish.

## Checked
2026-11-01. Confirmed against RFC 9213, MDN Cache-Control, the Vercel CDN cache page (CDN-Cache-Control, Vercel-CDN-Cache-Control, s-maxage stripping, x-vercel-cache, Vary) and the Cloudflare Cache Rules page. Removed default-caching claims, rule expressions, purge, Workers, Netlify and `cf-cache-status` details (not in the fetched pages).
Method: documentation only; no commands were run.
