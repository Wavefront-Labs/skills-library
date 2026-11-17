---
id: computing-software.web-development.nextjs.streaming-with-suspense
name: streaming-with-suspense
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, streaming-ssr, suspense, loading-ui, use-hook, waterfalls, app-router, web-development]
level: practitioner
status: verified
description: "Streaming Next.js pages with Suspense: placing boundaries, avoiding request waterfalls, passing promises to client components with use(), and status/SEO effects."
sources:
  - https://nextjs.org/docs/app/getting-started/fetching-data#streaming
  - https://react.dev/reference/react/Suspense
  - https://react.dev/reference/react/use
  - https://nextjs.org/docs/app/guides/streaming
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming with Suspense

**Goal:** send the page shell immediately and stream slow sections as their data resolves, instead of blocking on the slowest query.

## 1. Boundaries around slow parts
```tsx
export default async function Page() {
  return (
    <>
      <Header />                                   {/* static, instant */}
      <Suspense fallback={<RevenueSkeleton />}><Revenue /></Suspense>
      <Suspense fallback={<FeedSkeleton />}><Feed /></Suspense>
    </>
  );
}
async function Revenue() { const data = await getRevenue(); return <Chart data={data} />; }
```
Each async component streams in independently; HTML chunks arrive in one response with inline scripts that swap fallbacks.

## 2. Avoid waterfalls
```tsx
// Sequential: 3 x latency
const user = await getUser(); const posts = await getPosts(); const tags = await getTags();
// Parallel
const [user, posts, tags] = await Promise.all([getUser(), getPosts(), getTags()]);
```
Or start promises early and await them in separate Suspense-wrapped children. Only make calls sequential when one depends on the other.

## 3. Promises to client components
```tsx
// server
const commentsPromise = getComments(id);         // not awaited
return <Suspense fallback={<Spinner />}><Comments promise={commentsPromise} /></Suspense>;
// client
"use client";
export function Comments({ promise }) { const comments = use(promise); return ...; }
```

## 4. Boundary design
- Fallbacks should match final layout size (avoid CLS).
- Group things that should appear together under one boundary; avoid popcorn UI.
- `loading.tsx` = a boundary for the whole page segment; nested `<Suspense>` for finer control.

## 5. HTTP and SEO implications
- Once streaming begins, the status is 200 and headers are sent. `redirect()`/`notFound()` inside a streamed boundary are handled with client-side instructions (and `noindex` meta for not-found). Do access checks and 404 lookups **before** the first Suspense boundary when status codes matter.
- Streamed content is in the HTML response, so crawlers see it. Next limits streaming metadata for known bots (`htmlLimitedBots`).
- Proxies/CDNs that buffer (some nginx configs) defeat streaming: set `X-Accel-Buffering: no` / disable proxy buffering.

Ran on a 16.4.2 production build (`force-dynamic` page, 1.5 s async child inside `<Suspense>`): `curl -sN` printed the shell and fallback markup first and the resolved child later in the same response. A `notFound()` thrown inside a Suspense boundary after streaming began returned HTTP 200 with `<meta name="robots" content="noindex">`; a `redirect()` inside a boundary returned HTTP 200 with a `NEXT_REDIRECT;replace;/dashboard;307;` instruction in the payload. The self-hosting guide documents disabling nginx buffering with `X-Accel-Buffering: no`, and the metadata docs say streamed metadata is blocking for HTML-limited bots (configurable with `htmlLimitedBots`).

## Verify
- [ ] `curl -N` shows the shell arriving before slow sections.
- [ ] Performance panel: TTFB/FCP not tied to the slowest query.
- [ ] Missing resources still return 404 status (checked before streaming).
