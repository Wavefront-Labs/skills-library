---
id: computing-software.web-development.nextjs.next-config-redirects-rewrites-headers
name: next-config-redirects-rewrites-headers
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, next-config, nextjs-redirects, rewrites, security-headers, basepath, next-config-ts, web-development]
level: practitioner
status: verified
description: "Configuring next.config: redirects, rewrites (beforeFiles/afterFiles/fallback), custom headers, path matching, evaluation order and common options."
sources:
  - https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects
  - https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites
  - https://nextjs.org/docs/app/api-reference/config/next-config-js/headers
  - https://nextjs.org/docs/app/api-reference/config/typescript#type-checking-nextconfigts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# next.config: redirects, rewrites and headers

**Goal:** URL migrations, proxies and security headers declared once, evaluated before rendering.

## 1. Typed config
```ts
// next.config.ts (ran on 16.4.2)
import type { NextConfig } from "next";
const config: NextConfig = {
  async redirects() { return [...]; },
  async rewrites() { return [...]; },
  async headers() { return [...]; },
};
export default config;
```

## 2. Redirects
```ts
async redirects() {
  return [
    { source: "/blog/:slug", destination: "/articles/:slug", permanent: true },   // 308
    { source: "/docs/:path*", destination: "https://docs.example.com/:path*", permanent: false }, // 307
    { source: "/old", has: [{ type: "query", key: "ref" }], destination: "/new", permanent: false },
  ];
}
```
- `permanent: true` = 308 (cached by browsers/search engines - be sure).
- Matchers: `:param`, `:path*` (zero or more), `:path+`, regex `:id(\\d{1,})`, `has`/`missing` conditions on header/cookie/query/host.
- Ran on 16.4.2: `permanent: true` answered 308 and `permanent: false` 307 with the destination substituted (`/old/x` -> `/articles/x`, `/docs/a/b` -> `https://docs.example.com/a/b`); a `has` query condition redirected `/oldq?ref=1` (query string preserved) and `/oldq` without it returned 404; a `headers()` entry applied to every response including 404s; `poweredByHeader: false` removed `X-Powered-By`.
- Very large redirect sets: check your host's limits and consider a lookup inside `proxy.ts` instead of a huge config array.

## 3. Rewrites
Serve another path or origin while the URL stays the same:
```ts
async rewrites() {
  return {
    beforeFiles: [{ source: "/", has: [{ type: "host", value: "app.example.com" }], destination: "/app" }],
    afterFiles:  [{ source: "/api/legacy/:path*", destination: "https://legacy.example.com/:path*" }],
    fallback:    [{ source: "/:path*", destination: "https://old-site.example.com/:path*" }],   // incremental migration
  };
}
```

## 4. Headers
```ts
async headers() {
  return [{
    source: "/(.*)",
    headers: [
      { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" },
      { key: "X-Content-Type-Options", value: "nosniff" },
      { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
      { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
    ],
  }];
}
```
Nonce-based CSP must be set per request in middleware/proxy, not here.

## 5. Evaluation order
(Matches the rewrites docs for 16.4.2.) `headers` -> `redirects` -> middleware/proxy -> `beforeFiles` rewrites -> filesystem (public, _next/static, pages) -> `afterFiles` -> dynamic routes -> `fallback`.

## 6. Other frequently used options
`basePath`, `trailingSlash`, `images.remotePatterns`, `output`, `poweredByHeader: false`, `typedRoutes`, `serverExternalPackages`, `transpilePackages`.

## Verify
- [ ] `curl -I` each redirect source: correct status and Location.
- [ ] securityheaders.com / `curl -I` shows headers on HTML and API responses.
- [ ] Rewritten proxy paths return upstream content with the original URL.
