---
id: computing-software.cloud-infrastructure-engineering.azure.front-door-query-string-caching-and-cache-key
name: front-door-query-string-caching-and-cache-key
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, front-door, query-string-caching, cache-key, cache-duration, rules-engine, cache-purge]
level: practitioner
status: docs-checked
description: "Control what Azure Front Door caches: query string caching behaviours, cache key composition, cache duration vs origin headers, rule set overrides and safe purges."
sources: ["https://learn.microsoft.com/azure/frontdoor/front-door-caching", "https://learn.microsoft.com/azure/frontdoor/front-door-rules-engine-actions", "https://learn.microsoft.com/cli/azure/afd/endpoint#az-afd-endpoint-purge"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query string caching and cache key

**Goal:** high hit ratio without serving the wrong content to the wrong user.

## Cache key
Path plus the query string as selected by the route's caching behaviour (parameter order does not matter):
| Behaviour | Cache key uses | Good for |
|---|---|---|
| Ignore query string | None of it | Static assets with cache-busting in file names |
| Use query string | Full query string | Content varying by all parameters |
| Ignore specified query strings | All except listed (e.g. `utm_source`, `fbclid`) | Marketing tracking params |
| Include specified query strings | Only listed (e.g. `lang`, `v`) | Pages varying by a few params |
```bash
az afd route update -g rg --profile-name afd-prod --endpoint-name ep-web --route-name route-static \
  --cache-configuration "{query-parameters:<param-list>,query-string-caching-behavior:IgnoreSpecifiedQueryStrings}"
```
Caching is configured through the route's `--cache-configuration` (shorthand, JSON or YAML); to disable caching,
omit the cache configuration object. Check the exact parameter-list syntax with `az afd route update -h`.

## Cache duration
- Front Door honours origin `Cache-Control` (`s-maxage`, `max-age`). `private`, `no-cache` and `no-store` mean the response
  is not cached, even if a rules engine override is set. With no `Cache-Control`, it picks a duration between one and
  three days. Cache expiration cannot exceed 366 days.
- Rules engine caching settings always override the route's: use the **Route configuration override** action with
  *Honor origin*, *Override always* or *Override if origin missing* plus a duration.
- Compression supports gzip and Brotli; Brotli wins when the client supports both.
- If a cacheable origin response has `Set-Cookie`, Front Door strips it before replying; for a non-cacheable response it does not.

## Never cache personalised content
Disable caching on API/authenticated routes (separate route or rule condition on path/cookie). Requests with an
`Authorization` header are not cached unless the response carries `must-revalidate`, `public` or `s-maxage`, so fix origin headers.

## Purge
```bash
az afd endpoint purge -g rg --profile-name afd-prod --endpoint-name ep-web --content-paths "/assets/app.js" "/img/*" \
  --domains www.contoso.com
```
Purge accepts a trailing `/*` wildcard (`/*` purges the whole endpoint), is case-insensitive and is query-string agnostic
(purging a URL purges every query-string variation). Wildcard domains cannot be purged directly; name the subdomain.
Prefer versioned file names over purge-heavy release processes.

## Gotchas
- Including volatile params (session IDs) in the key destroys hit ratio.

## Verify
- [ ] Repeat requests report a cache hit (`TCP_HIT` in the cache status, `TCP_MISS` on first fetch); API routes never hit.

## Checked
2026-10-28. Confirmed in Learn `front-door-caching`: query string behaviours and order independence, Cache-Control
handling, 1-3 day default, 366-day cap, rules engine override and its three behaviours, gzip/Brotli, Authorization and
Set-Cookie behaviour, purge wildcard and case/query-string rules, TCP_HIT/TCP_MISS. Confirmed in the `az afd route`
and `az afd endpoint purge` references: `--cache-configuration`, `--content-paths`, `--domains`.
Removed: the nonexistent `--enable-caching`, `--query-string-caching-behavior` and `--query-parameters` flags (now
inside `--cache-configuration`), the claims that Set-Cookie responses are never cached and that purges take minutes,
the `Vary` and cache-eviction gotchas, and the Byte Hit Ratio check. The 7-day TTL is only an example value.
Method: documentation only; no commands were run.
