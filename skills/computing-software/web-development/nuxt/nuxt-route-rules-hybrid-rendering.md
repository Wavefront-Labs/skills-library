---
id: computing-software.web-development.nuxt.nuxt-route-rules-hybrid-rendering
name: nuxt-route-rules-hybrid-rendering
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, route-rules, hybrid-rendering, isr, swr]
level: advanced
status: docs-checked
description: "Configure per-route rendering and caching in Nuxt with routeRules: prerender, swr, isr, ssr false, redirect, proxy, cors, headers, noScripts, appMiddleware."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/3.guide/1.concepts/1.rendering.md
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/3.utils/define-route-rules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hybrid rendering uses `routeRules` in `nuxt.config` to define rules for groups of routes, change rendering mode or assign a cache strategy per route. The Nuxt server automatically registers the corresponding middleware and wraps routes with cache handlers using Nitro's caching layer.

```ts
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true },           // pre-rendered at build time
    '/products': { swr: true },         // on demand, revalidates in background
    '/products/**': { swr: 3600 },      // cached 1 hour (3600 seconds)
    '/blog': { isr: 3600 },             // cached on CDN for 1 hour
    '/blog/**': { isr: true },          // once until next deployment, on CDN
    '/admin/**': { ssr: false },        // renders only client-side
    '/api/**': { cors: true },
    '/old-page': { redirect: '/new-page' },
    '/proxy/**': { proxy: 'https://api.example.com/**' },
  },
})
```

Properties: `redirect` (server-side redirects), `proxy` (string target, or object with `to` and H3 proxy options), `ssr` (false renders only in the browser), `cors` (adds cors headers; customise by overriding with `headers`), `headers`, `swr` (cache headers plus server or reverse-proxy cache for a TTL; the Nitro `node-server` preset can cache the full response; after expiry the cached response is sent while the page regenerates in the background; `true` adds `stale-while-revalidate` without a MaxAge), `isr` (same as swr but can also add the response to the CDN cache on platforms that support it, currently Netlify and Vercel; `true` persists until the next deploy), `prerender`, `noScripts`, `appMiddleware` (string, array or record of booleans for page paths in the Vue app, not Nitro routes).

Notes from the page:
- Routes with `isr` or `swr` also generate `_payload.json` files alongside HTML.
- Route rules are not a security measure: `redirect` and `proxy` rules run before server middleware and may be handled by the hosting platform without reaching your server, so do not use them for endpoints needing authorization.
- A route covered by `ssr: false` is excluded from the server bundle when the covering rules resolve at build time. The page stays if a more specific rule re-enables SSR below it, the page has an alias or an absolute-path child outside the client-only region, or it is a parent shell for a child that is still server-rendered.
- Hybrid rendering is not available with `nuxt generate`. Where possible, rules are applied to the platform's native rules (Netlify and Vercel currently).

Page-level shorthand: `defineRouteRules({ prerender: true })` is experimental and needs `experimental.inlineRouteRules`. A rule in `pages/foo/[id].vue` applies to `/foo/*`. For custom `path` or `alias`, set `routeRules` directly in `nuxt.config`.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/3.guide/1.concepts/1.rendering.md (Hybrid Rendering) and docs/4.api/3.utils/define-route-rules.md. Confirmed: example rules, every property description, the payload and bundle-size notes. Added the security warning and page-level rule notes. Removed: the invented Verify step (curl and cache headers).

Method: documentation only; no commands were run.
