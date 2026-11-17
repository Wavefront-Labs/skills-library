---
id: computing-software.web-development.nextjs.static-vs-dynamic-rendering
name: static-vs-dynamic-rendering
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, static-rendering, dynamic-rendering, dynamic-apis, route-segment-config, ssg, isr, web-development]
level: practitioner
status: verified
description: "Controlling whether Next.js routes render statically or per request: dynamic APIs that opt in, route segment config, build output symbols and debugging surprises."
sources:
  - https://nextjs.org/docs/app/getting-started/partial-prerendering
  - https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config
  - https://nextjs.org/docs/app/api-reference/functions/connection
  - https://nextjs.org/docs/app/guides/caching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static vs dynamic rendering

**Goal:** know, for each route, whether HTML is built once (fast, cacheable) or rendered per request - and control it deliberately.

## 1. What makes a route dynamic
Using any request-time API in the route's server components:
- `cookies()`, `headers()`, `draftMode()` (async in Next 15+)
- `searchParams` prop in a page
- `connection()` (explicit "render per request" marker; the docs recommend it instead of `unstable_noStore` since v15)
- `fetch(url, { cache: "no-store" })` or `revalidate: 0`
- Dynamic route params not returned by `generateStaticParams` (rendered on demand, then cached unless `dynamicParams = false`).

Everything else is prerendered at build time (static), optionally refreshed with `revalidate` (ISR).

## 2. Read the build output
Ran on 16.4.2: `○` Static (prerendered as static content), `●` SSG (prerendered as static HTML, uses `generateStaticParams`), `ƒ` Dynamic (server-rendered on demand); a page with only a plain `fetch` was `○`, `cookies()`/`searchParams`/`connection()`/`cache: 'no-store'`/`force-dynamic` made it `ƒ`, and a GET route handler was `ƒ`. Unknown slugs under a `generateStaticParams` route were rendered on demand then cached (`x-nextjs-cache: MISS`, then HIT).
```
Route (app)              Size
┌ ○ /                    static
├ ● /blog/[slug]         SSG via generateStaticParams
└ ƒ /dashboard           dynamic (server-rendered on demand)
```
Check it in CI; a route flipping from ○ to ƒ is a performance regression.

## 3. Route segment config
```ts
export const dynamic = "force-static";   // cookies()/headers()/useSearchParams() return empty values (docs; ran: a page reading both rendered `undefined`/`null`)
export const dynamic = "error";          // build error if anything dynamic is used (guard)
export const dynamic = "force-dynamic";  // always per request
export const revalidate = 3600;          // ISR interval for the segment
export const dynamicParams = false;      // unknown [slug] -> 404
```
With Next 16 `cacheComponents` enabled, segment config like `dynamic`/`revalidate` is replaced by `use cache` + Suspense (partial prerendering).

## 4. Next 15 defaults changed
`fetch` is **not** cached by default (was cached in 14); GET route handlers are dynamic by default; client router cache doesn't reuse page segments by default. Opt in with `cache: "force-cache"`, `export const revalidate`, or `use cache`.

## 5. Keep pages static when personalising
- Read the cookie in a small client component or a Suspense-wrapped dynamic component, not at page top.
- Put personalisation behind PPR / a client fetch.
- Use `searchParams` only where needed - a filterable list page can render the shell statically and filter on the client.

## 6. Debugging "why is this dynamic?"
`export const dynamic = "error"` temporarily: the build error names the API that opted in (ran: `couldn't be rendered statically because it used cookies()`). Common culprits: auth helpers calling `cookies()` in the root layout (makes every route dynamic).

## Verify
- [ ] Build output marks marketing/content routes ○ or ●.
- [ ] `curl -I` on a static route shows cache headers (`x-nextjs-cache: HIT` / `s-maxage`).
- [ ] No `cookies()`/`headers()` calls in shared layouts unless intended.
