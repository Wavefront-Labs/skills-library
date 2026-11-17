---
id: computing-software.web-development.nextjs.loading-error-and-not-found-files
name: loading-error-and-not-found-files
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, loading-ui, nextjs-error-handling, error-tsx, not-found, global-error, suspense, web-development]
level: practitioner
status: verified
description: "Using Next.js loading.tsx, error.tsx, global-error.tsx and not-found.tsx correctly: boundaries, reset, notFound(), status codes and expected vs unexpected errors."
sources:
  - https://nextjs.org/docs/app/getting-started/error-handling
  - https://nextjs.org/docs/app/api-reference/file-conventions/loading
  - https://nextjs.org/docs/app/api-reference/file-conventions/error
  - https://nextjs.org/docs/app/api-reference/file-conventions/not-found
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# loading.tsx, error.tsx and not-found.tsx

**Goal:** every route segment has an instant loading state, a contained error state and a real 404.

## 1. loading.tsx
```tsx
// app/dashboard/loading.tsx
export default function Loading() { return <DashboardSkeleton />; }
```
Wraps the segment's `page` (and children) in `<Suspense>`. The layout stays interactive; the skeleton shows instantly on navigation and is prefetched for dynamic routes. For finer control use `<Suspense>` inside the page around slow components.

## 2. error.tsx
```tsx
"use client";                                     // required
export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  useEffect(() => { reportError(error); }, [error]);
  return <div role="alert"><p>Something went wrong.</p><button onClick={() => reset()}>Try again</button></div>;
}
```
- Catches errors in the segment's page and children, **not** in its own `layout.tsx` (put `error.tsx` in the parent for that).
- In production, server error messages are replaced with a generic message plus `digest` matching the server log (ran: the server thrown text never reached the HTML, the response was HTTP 500 with `noindex`, and the browser rendered `error.tsx` client-side with the generic message and the digest).
- From Next 16.3 (`retry` prop stable per the error.js version history) use `retry()`: it re-fetches and re-renders the boundary's children. `reset()` only clears the error state and re-renders without re-fetching, so for server data errors prefer `retry()` (on older versions: `router.refresh()` inside `startTransition`, then `reset()`).
- Ran: an error thrown in `app/err/inner/layout.tsx` was NOT caught by the sibling `error.tsx` in the same folder; the default full-page error appeared instead.

## 3. global-error.tsx
Catches errors in the root layout. Must render its own `<html><body>` because it replaces the root layout. Since v15.2.0 it is also displayed in development (version history of error.js). It does not include your global styles.

## 4. not-found.tsx and notFound()
```tsx
import { notFound } from "next/navigation";
const post = await getPost(slug);
if (!post) notFound();
```
Renders the closest `not-found.tsx` with HTTP 404 (when not already streaming). `app/not-found.tsx` also handles unmatched URLs. If streaming already started, Next adds `<meta name="robots" content="noindex">` because the status can't change. Ran on 16.4.2: a dynamic page calling `notFound()` after an `await` returned 404 with no `loading.tsx`, but with a `loading.tsx` in that segment the same page returned HTTP 200 with `noindex` and the not-found markup in the body. If real 404 status codes matter, look the resource up in `generateMetadata`/a parent layout or avoid `loading.tsx` on that segment.

## 5. Expected vs unexpected errors
- Expected (validation, "not allowed", 404): return values or `notFound()`/`redirect()`; don't throw. In server actions return `{ error }` to `useActionState`.
- Unexpected (bugs, DB down): let them throw to `error.tsx`.
- Never wrap `redirect()`/`notFound()` in a try/catch that swallows them - they work by throwing.

## 6. Placement
Root: `not-found.tsx`, `global-error.tsx`, `error.tsx`. Per feature: `loading.tsx` and `error.tsx` where a section can fail or load independently.

## Verify
- [ ] Unknown URL and unknown slug both return HTTP 404 (`curl -I`), including segments that have a `loading.tsx` (they may return 200).
- [ ] Throwing in a page shows the segment error UI while layout navigation still works.
- [ ] Slow page shows the skeleton immediately on navigation (throttle network).
