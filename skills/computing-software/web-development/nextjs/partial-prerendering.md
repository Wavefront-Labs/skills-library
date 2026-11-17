---
id: computing-software.web-development.nextjs.partial-prerendering
name: partial-prerendering
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, partial-prerendering, ppr, cache-components, suspense, static-shell, web-development]
level: practitioner
status: verified
description: "Using Next.js Partial Prerendering: static shell plus streamed dynamic holes via Suspense, enabling cacheComponents in Next 16, and designing boundaries."
sources:
  - https://nextjs.org/docs/app/getting-started/partial-prerendering
  - https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents
  - https://nextjs.org/blog/next-16
  - https://vercel.com/blog/partial-prerendering-with-next-js-creating-a-new-default-rendering-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partial Prerendering (PPR)

**Goal:** one route that serves a prebuilt static shell from the CDN instantly and streams only the personalised parts per request.

## 1. The model
At build time Next renders the route until it hits dynamic access (cookies, headers, uncached data). The output up to each `<Suspense>` boundary around dynamic content becomes the static shell (including fallbacks). At request time the shell is sent immediately and the dynamic holes stream in the same response.

## 2. Enabling
- Next 16: `cacheComponents: true` in `next.config.ts` - PPR becomes the default model, together with `use cache`. 16.4.2 also warns that `cacheComponents` is enabled without a `partialPrefetching` option and asks you to set it to `true` or `false` (new projects should enable both).
- Next 14/15: experimental `experimental: { ppr: "incremental" }` plus `export const experimental_ppr = true` per route (canary). Next 16 removed `experimental.ppr` and the `experimental_ppr` segment config (migrating-to-cache-components guide).
```ts
// next.config.ts (Next 16)
const config = { cacheComponents: true };
export default config;
```

## 3. Writing a PPR route
```tsx
export default function ProductPage({ params }) {
  return (
    <>
      <ProductDetails params={params} />          {/* cached with "use cache" -> in shell */}
      <Suspense fallback={<CartSkeleton />}>
        <Cart />                                  {/* reads cookies() -> dynamic hole */}
      </Suspense>
      <Suspense fallback={<RecsSkeleton />}><Recommendations /></Suspense>
    </>
  );
}
```
With `cacheComponents`, uncached data access or request APIs **outside** a Suspense boundary cause a build error. Ran on 16.4.2 (a page reading `cookies()` at the top): `Route "/bad": Next.js encountered uncached or runtime data during prerendering.` with the fixes `[stream]` wrap in `<Suspense fallback>`, `[cache]` use `"use cache"` (not for `connection()`), or `[block]` set `export const instant = false` to allow a blocking route. Segment config such as `export const dynamic = 'force-dynamic'` is itself a build error (`Route segment config "dynamic" is not compatible with nextConfig.cacheComponents`).

## 4. Designing boundaries
- Push dynamic access as deep as possible; pass the `params`/`searchParams` promise down instead of awaiting at the top.
- Make fallbacks the same size as content (shell is what users see first; CLS counts).
- Group small dynamic bits (user avatar, cart count) into one client-fetched or Suspense region rather than many.

## 5. Hosting
Works on Vercel and self-hosted Node; the static shell is cached by Next's cache handler. Purely static export (`output: "export"`) can't serve dynamic holes.

## Verify
- [ ] Build output marks the route as partially prerendered (◐; legend `Partial Prerender: prerendered as static HTML with dynamic server-streamed content`, ran).
- [ ] `curl -N` shows shell HTML first, then streamed chunks (ran: the shell plus fallback came first, the cookie-dependent text arrived later, and the response carried `x-nextjs-postponed: 1`).
- [ ] Logged-out and logged-in users receive the same shell bytes; personal data only in streamed parts.
