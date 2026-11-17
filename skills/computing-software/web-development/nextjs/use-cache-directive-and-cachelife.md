---
id: computing-software.web-development.nextjs.use-cache-directive-and-cachelife
name: use-cache-directive-and-cachelife
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, use-cache-directive, cachelife, cachetag, cache-components, updatetag, revalidatetag, web-development]
level: practitioner
status: verified
description: "Caching in Next.js 16 with the use cache directive: file/component/function scope, cacheLife profiles, cacheTag invalidation, updateTag and serialisable keys."
sources:
  - https://nextjs.org/docs/app/api-reference/directives/use-cache
  - https://nextjs.org/docs/app/api-reference/functions/cacheLife
  - https://nextjs.org/docs/app/api-reference/functions/cacheTag
  - https://nextjs.org/blog/next-16
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# use cache directive and cacheLife

**Goal:** explicit, composable caching of data and UI in Next.js 16 (Cache Components) instead of implicit fetch caching.

## 1. Enable
```ts
// next.config.ts
export default { cacheComponents: true };
```
(Next 15 canary used `experimental.useCache`/`experimental.dynamicIO`; both flags were removed in Next 16 per the upgrade guide. 16.4.2 also warns when `cacheComponents` is set without `partialPrefetching`.)

## 2. Scopes
```ts
// function
export async function getProducts(category: string) {
  "use cache";
  cacheLife("hours");
  cacheTag("products", `products:${category}`);
  return db.product.findMany({ where: { category } });
}
```
```tsx
// component
async function Footer() { "use cache"; const links = await getLinks(); return <nav>...</nav>; }
// whole file: put "use cache" at the top of a page/layout file
```
The cache key is built from the build id, function id and **serialised arguments** (plus closed-over values). Non-serialisable args (class instances, functions) can be passed through as children/props but not inspected inside.

## 3. cacheLife profiles
Built-in (cacheLife docs table; stale / revalidate / expire): `default` 5 min / 15 min / never; `seconds` 30 s / 1 s / 1 min; `minutes` 5 min / 1 min / 1 hour; `hours` 5 min / 1 hour / 1 day; `days` 5 min / 1 day / 1 week; `weeks` 5 min / 1 week / 30 days; `max` 5 min / 30 days / 1 year. Each has `stale` (client may use without checking), `revalidate` (background refresh) and `expire` (hard max). Custom:
```ts
// next.config.ts
export default { cacheComponents: true, cacheLife: { catalog: { stale: 300, revalidate: 900, expire: 86400 } } };
```

## 4. Invalidation
```ts
"use server";
import { updateTag, revalidateTag } from "next/cache";
export async function updateProduct(id: string, data: FormData) {
  await db.product.update(...);
  updateTag(`product:${id}`);            // server actions: expire now, user sees own write (read-your-writes)
}
// webhook/route handler: stale-while-revalidate refresh
revalidateTag("products", "max");        // Next 16: second argument is the profile (one argument is deprecated and behaves like { expire: 0 })
```

## 5. Rules and gotchas
- Can't call `cookies()`/`headers()`/`searchParams` inside a cached scope; read them outside and pass the value as an argument (it becomes part of the key).
- `"use cache: private"` allows request APIs for per-user caching in the browser only; `"use cache: remote"` stores in a remote cache handler for serverless.
- Default in-memory cache is per instance; self-hosted multi-instance setups need a shared `cacheHandlers` implementation (e.g. Redis).
- Anything not cached must sit inside `<Suspense>` with `cacheComponents`, or the build fails.

## Verify
- [ ] Logging inside a cached function shows one execution per key per revalidate window (ran on 16.4.2 with a 5 s `revalidate` profile: repeated requests inside the window logged nothing; after the window a request got the stale value and triggered one refetch; `revalidateTag('t1','max')` from a Route Handler then refreshed on the next request; `updateTag` from a Route Handler throws `updateTag can only be called from within a Server Action`).
- [ ] Mutation followed by reload shows fresh data (tag invalidated).
- [ ] No `cookies()` calls inside cached scopes (build passes).
