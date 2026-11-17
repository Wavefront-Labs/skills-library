---
id: computing-software.web-development.nextjs.static-export
name: static-export
category: computing-software
field: web-development
product: nextjs
tags: [static-export, output-export, nextjs-static-site, generatestaticparams, unoptimized-images, nextjs]
level: practitioner
status: verified
description: "Building a fully static Next.js site with output export: what works and what does not (middleware, ISR, cookies, image optimisation), dynamic routes, trailing slashes and hosting."
sources:
  - https://nextjs.org/docs/app/guides/static-exports
  - https://nextjs.org/docs/app/api-reference/config/next-config-js/output
  - https://nextjs.org/docs/app/api-reference/config/next-config-js/trailingSlash
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static export

```js
// next.config.mjs
export default {
  output: "export",
  trailingSlash: true,                 // emit /about/index.html for hosts without rewrite support
  images: { unoptimized: true },       // or a custom loader pointing at an image CDN
  basePath: process.env.BASE_PATH,     // e.g. "/docs" for sub-path hosting (GitHub Pages project sites)
};
```
`next build` writes static HTML/JS/CSS to `out/`; deploy to any static host (S3 + CloudFront, GitHub Pages, Netlify, nginx).

## 1. Works
Server Components (run at build time), static route handlers (a GET handler without request data must also set `export const dynamic = "force-static"`; ran on 16.4.2: without it the build fails with `export const dynamic = "force-static"/export const revalidate not configured on route "/api/s" with "output: export"`), `generateStaticParams` dynamic routes, `next/link` client navigation and prefetching, client components and client-side data fetching, metadata files (sitemap, robots, OG images rendered at build; ran on 16.4.2: `sitemap.ts`, `robots.ts` and `opengraph-image.tsx` each failed the export with the same `force-static not configured` error until `export const dynamic = "force-static"` was added, after which `out/sitemap.xml`, `out/robots.txt` and `out/opengraph-image` were written).

## 2. Does not work (build error or silently unavailable)
Ran on 16.4.2, one at a time: a dynamic route without `generateStaticParams` fails (`Page "/nogsp/[id]" is missing "generateStaticParams()" so it cannot be used with "output: export" config`); `cookies()` and `await searchParams` fail (`couldn't be rendered statically because it used cookies()`); `export const dynamic = "force-dynamic"` fails; a Server Action fails (`Server Actions are not supported with static export`); `rewrites`/`redirects`/`headers` in config only warn (`will not automatically work with "output: export"`) and are not applied; `proxy.ts` only warns (`disables API routes and middleware`); `export const revalidate`, `draftMode()`, `after()` and the default image loader built without any error or warning here, but the static-exports guide lists ISR, Draft Mode and default-loader Image Optimization as unsupported, and `after` is not supported in static export per its docs, so they do nothing useful.
- Middleware, rewrites/redirects/headers in `next.config` (configure them on the host).
- `cookies()`, `headers()`, `searchParams` on the server, `draftMode`.
- ISR / `revalidate`, on-demand revalidation, Server Actions, dynamic route handlers.
- Default image optimisation (needs a server).
- Dynamic routes without `generateStaticParams` (set `dynamicParams = false` to make missing params a clear 404).

## 3. Dynamic data
Fetch on the client (SWR/TanStack Query) from an API, or rebuild on content changes (CMS webhook triggers CI build).

## 4. Hosting details
- 404: Next emits `404.html` (ran: `out/404.html`, plus `out/404/index.html` with `trailingSlash: true`); configure the host's error document to it.
- Without `trailingSlash`, `/about` maps to `about.html`; hosts like S3 website endpoints need rewrites or `trailingSlash: true`.
- Cache `/_next/static/*` immutable for a year; HTML `no-cache`.

## Verify
- [ ] `npx serve out` locally: deep links, refresh on nested routes and the 404 page all work; no server-only feature warnings in the build log.
