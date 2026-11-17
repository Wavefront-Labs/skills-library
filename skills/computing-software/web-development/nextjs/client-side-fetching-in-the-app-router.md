---
id: computing-software.web-development.nextjs.client-side-fetching-in-the-app-router
name: client-side-fetching-in-the-app-router
category: computing-software
field: web-development
product: nextjs
tags: [nextjs-client-fetching, swr, tanstack-query, app-router, data-fetching]
level: practitioner
status: docs-checked
description: "Client-side fetching in the Next.js App Router: SWR or TanStack Query providers, server prefetch with hydration, polling, mutations and avoiding waterfalls."
sources:
  - https://nextjs.org/docs/app/getting-started/fetching-data
  - https://tanstack.com/query/latest/docs/framework/react/guides/advanced-ssr
  - https://swr.vercel.app/docs/with-nextjs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client-side fetching with SWR / TanStack Query in the App Router

Default to fetching in Server Components. Fetch on the client for: user-specific data on otherwise static pages, polling/real-time updates, infinite scroll, data depending on client-only state (filters typed by the user), and optimistic mutations.

## 1. Provider in a client component
```tsx
// app/providers.tsx
"use client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";
export function Providers({ children }: { children: React.ReactNode }) {
  const [qc] = useState(() => new QueryClient({ defaultOptions: { queries: { staleTime: 60_000 } } }));
  return <QueryClientProvider client={qc}>{children}</QueryClientProvider>;
}
// app/layout.tsx: <body><Providers>{children}</Providers></body>
```
On the server, create a new `QueryClient` per request so users don't share a cache; TanStack's advanced SSR guide warns that `useState` initialisation is unsafe when no Suspense boundary sits above code that may suspend. Set a default `staleTime` above 0 with SSR to avoid refetching immediately on the client.

## 2. Prefetch on the server, hydrate on the client
```tsx
// app/orders/page.tsx (Server Component)
import { dehydrate, HydrationBoundary, QueryClient } from "@tanstack/react-query";
export default async function Page() {
  const qc = new QueryClient();
  await qc.prefetchQuery({ queryKey: ["orders"], queryFn: getOrders });
  return <HydrationBoundary state={dehydrate(qc)}><OrdersTable /></HydrationBoundary>;
}
// OrdersTable is "use client" and calls useQuery({ queryKey: ["orders"], queryFn: fetchOrders })
```
First paint has data, and the client cache takes over for refetching and mutations.

For SWR, see its Next.js guide (swr.vercel.app/docs/with-nextjs).

## 3. Endpoints
Client fetchers call an API route or an external API. Server Actions remain a good fit for mutations rather than reads (TanStack Query advanced SSR guide).

## 4. Mutations
Use `useMutation` for writes; if the same data is also rendered by Server Components, make sure the server-rendered views are refreshed too.

## 5. Pitfalls
- Client waterfalls (parent fetch -> child fetch): prefetch in parallel on the server or fetch in parallel with `useSuspenseQueries`.


## Verify
- [ ] No duplicate request immediately after hydration; per-request QueryClient on the server; mutations update both client cache and server-rendered views.

## Checked

2026-10-28. Confirmed from the TanStack Query advanced SSR guide (`dehydrate`, `HydrationBoundary`, default `staleTime` above 0 with SSR, the `useState` caveat, `useSuspenseQueries` for parallel fetching, Server Actions suit mutations). Removed (not found): the SWR `fallback` snippet, `app/api/.../route.ts` path, `onMutate`/`invalidateQueries`/`router.refresh()`/`revalidatePath` specifics, `useEffect` and cookie claims, polling-pause check.

Method: documentation only; no commands were run.
