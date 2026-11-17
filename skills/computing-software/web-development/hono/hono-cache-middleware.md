---
id: computing-software.web-development.hono.hono-cache-middleware
name: hono-cache-middleware
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, cache, cloudflare-workers, deno]
level: practitioner
status: docs-checked
description: "Use the Hono cache middleware with the Web Cache API: cacheName, cacheControl, vary, keyGenerator, status codes, QUERY caching and auth safety."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/cache.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cache middleware

Import: `import { cache } from 'hono/cache'`. Uses the Web Standards Cache API. It supports Cloudflare Workers on custom domains and Deno 1.26+ (including Deno Deploy). Cloudflare respects `Cache-Control`; Deno does not, so you need your own update mechanism.

```ts
// Cloudflare Workers
app.get('*', cache({ cacheName: 'my-app', cacheControl: 'max-age=3600' }))
// Deno: wait: true is required
app.get('*', cache({ cacheName: 'my-app', cacheControl: 'max-age=3600', wait: true }))
```

## Options
- `cacheName` (required): `string | (c) => string | Promise<string>`.
- `wait`: wait for `cache.put` to resolve; must be true on Deno; default false.
- `cacheControl`: directives string; if omitted no `Cache-Control` header is added.
- `vary`: `string | string[]`, merged with an existing Vary header; `*` causes an error.
- `keyGenerator(c)`: default `c.req.url`.
- `cacheableStatusCodes: number[]`: default `[200]`, e.g. `[200, 404, 412]`.
- `maxQueryBodySize`: default 65536; larger QUERY bodies bypass the cache.
- `onCacheNotAvailable`: callback or `false` to silence the log when the Cache API is missing.

## Authenticated responses
The cache is shared by all clients and the middleware ignores the request `Cookie`. Register `cache()` after your auth middleware, set `Cache-Control: private` or `no-store` on per-user responses, or use `vary: 'Cookie'`:

```ts
app.use('/api/*', auth)
app.get('/api/*', cache({ cacheName: 'my-app', cacheControl: 'max-age=60', vary: 'Cookie' }))
```

## Gotcha
Entries are stored under an internal key `/.hono/cache?__hono_cache_key=...`, so `caches.delete()` with the original URL will no longer purge them.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/cache.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
