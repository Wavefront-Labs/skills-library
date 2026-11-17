---
id: computing-software.web-development.nextjs.data-fetching-caching-and-revalidation
name: data-fetching-caching-and-revalidation
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, app-router, caching, isr, revalidatepath, revalidatetag, server-actions, route-handlers, fetch, data-fetching, web-development]
level: advanced
status: verified
description: "Next.js App Router data layer: fetch's caching semantics, revalidatePath/revalidateTag, ISR, and when to use a route handler vs a server action."
sources:
  - https://nextjs.org/docs/app/building-your-application/caching
  - https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Next.js data fetching, caching, and revalidation

**Goal:** know exactly which layer is caching a value (there are four) so a
"why is this stale" bug takes minutes, not an afternoon of adding random
`no-store`s until it goes away. This has shifted across Next versions — verify
against the version in use; defaults changed between 13/14 and 15.

## 1. The cache layers, outside-in
1. **Request memoization** — within a single render pass, calling `fetch()` with
   identical args twice dedupes to one request (React's `cache()` semantics).
   Resets per request; doesn't persist across requests.
2. **Data cache** — `fetch()`'s own persistent cache across requests/deployments.
   In Next 13/14, GET `fetch()` calls were cached by default; **Next 15 flipped
   the default to uncached** (`auto no cache`): refetched every request in dev, but fetched once during `next build` if the route is statically prerendered, and per request if a request-time API is used (ran on 16.4.2: a page with a plain `fetch` stayed frozen at the build-time value, `cache: 'no-store'` made the route dynamic, `next: { revalidate: 3 }` refreshed in the background after the window). Opt in explicitly if you want persistent caching.
   `fetch(url, { cache: 'force-cache' })` to cache, `{ cache: 'no-store' }` to
   always refetch, `{ next: { revalidate: 60 } }` for time-based (ISR) caching.
3. **Full route cache** — the rendered HTML/RSC payload for a static route,
   produced at build time or on first request for routes without dynamic data.
   A `cookies()`/`headers()`/`searchParams` read, or any uncached dynamic fetch,
   opts a route out of this (marks it dynamic).
4. **Router cache (client-side)** — the Router (in the browser) caches visited
   route segments for back/forward navigation; `router.refresh()` clears it for
   the current route tree.

## 2. On-demand invalidation — targeted, not a blunt flush
```ts
revalidatePath('/blog/[slug]', 'page');   // route pattern + type: every matching page (a literal path like '/blog/hello' targets one page)
revalidateTag('products', 'max');          // stale-while-revalidate for every fetch tagged this way
```
`revalidateTag(tag, profile)` takes a second argument in Next 16: `'max'` serves stale content while revalidating, `{ expire: 0 }` forces a blocking refresh, and the one-argument form is deprecated (it warned and behaved like `{ expire: 0 }`). `revalidateTag` works in Server Functions and Route Handlers, not Proxy or Client Components. Tag fetches at the call site (`fetch(url, { next: { tags: ['products'] } })`) so a
single mutation (e.g. updating one product) can invalidate exactly the fetches
that depend on it, rather than nuking the whole route cache or falling back to
`no-store` everywhere out of caution — that trades correctness for giving up all
caching benefit.

## 3. Server actions vs route handlers — pick by caller, not habit
- **Server action** (`'use server'` function): called directly from a form
  action or client component event handler; Next handles the RPC wiring, request
  dedup, and can trigger `revalidatePath`/`revalidateTag` as part of the mutation.
  Best for form submissions and mutations triggered from your own UI.
- **Route handler** (`app/api/.../route.ts`): a real HTTP endpoint with a stable
  URL — needed for anything called from outside your app (webhooks, a mobile
  client, a third-party integration) or where you need explicit control over
  HTTP methods/status codes/headers.
Don't build a route handler just to call it from your own client component —
that's what server actions replace.

## 4. Common staleness bugs
- Mutating data in a server action but forgetting `revalidatePath`/`Tag` — UI
  shows old data until a full reload bypasses the router cache.
- Assuming a fetch is cached when the Next 15 default (uncached) applies — check
  the major version before reasoning about defaults.
- A dynamic route segment (`[id]`) with `generateStaticParams` still serving a
  stale pre-rendered page after data changed without revalidation configured.
- `fetch` inside a Server Component tagged for revalidation, but the actual
  mutation goes through a different code path (a webhook, cron job, admin
  panel) that never calls `revalidateTag` — add invalidation to every mutation
  path, not just the primary UI one.

## Verify
- [ ] The Next.js major version's `fetch` caching default is confirmed, not assumed.
- [ ] Every fetch whose data can change is tagged, and every mutation path (UI, webhook, cron) revalidates that tag.
- [ ] Route handlers exist only where a stable external HTTP endpoint is actually needed.
- [ ] A route's dynamic vs static classification is understood (check `next build` output), not accidental.
