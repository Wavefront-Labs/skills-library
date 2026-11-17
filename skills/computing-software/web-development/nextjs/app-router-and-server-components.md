---
id: computing-software.web-development.nextjs.app-router-and-server-components
name: app-router-and-server-components
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, next-js, app-router, react-server-components, rsc, server-components, client-components, use-client, use-server, server-actions, route-handlers, data-fetching, fetch-cache, revalidate, revalidatepath, revalidatetag, isr, ssg, ssr, generatestaticparams, loading-tsx, error-tsx, middleware, proxy, use-cache, streaming, suspense, vercel, react, web-development]
level: practitioner
status: verified
description: "Next.js App Router: server vs client components, the use client boundary, fetch caching and revalidation, server actions, route handlers, loading/error files, middleware."
sources:
  - https://nextjs.org/docs/app
  - https://nextjs.org/docs/app/getting-started/server-and-client-components
  - https://react.dev/reference/rsc/server-components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Next.js App Router and server components — draw the boundary, then control the cache

**Goal:** keep most of the tree on the server, ship JavaScript only for interactive
leaves, and know exactly when each page is static, cached or rendered per request.

## 1. Server vs client components
Everything in `app/` is a **server component** by default: it can be `async`, read the
database or secrets directly, and sends zero component JS to the browser. Add
`'use client'` at the top of a file only when you need state, effects, event handlers or
browser APIs.

```tsx
// app/products/[id]/page.tsx  (server)
import AddToCart from './add-to-cart';         // client leaf
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;                 // params is async from Next 15
  const product = await db.product.find(id);
  return <><h1>{product.name}</h1><AddToCart id={id} /></>;
}
```

Boundary rules that bite:
- `'use client'` marks a **module boundary**: everything that file imports becomes client code too. Push it to the smallest leaf.
- A client component can't import a server component, but can render one passed as `children` or another prop.
- Props crossing the boundary must be serialisable (no functions except server actions, no class instances).
- Guard server-only modules with `import 'server-only'` so a stray client import fails the build instead of leaking secrets.

## 2. Caching — check your version first
Caching defaults changed in **Next 15**: `fetch` is no longer cached by default (the docs call this `auto no cache`: refetched on every request in dev, but fetched once during `next build` when the route is otherwise static, and per request once the route reads a request-time API), GET route
handlers are not cached by default (ran: `/api/hello` shows as dynamic in the build table), and the client router cache no longer reuses page
segments by default (`staleTimes.dynamic` default changed from 30s to 0 in v15.0.0). Next 16 has opt-in "Cache Components" (`cacheComponents: true` in next.config, ran on 16.4.2) with the `'use cache'` directive. With it enabled, route segment config such as `export const dynamic` is a build error (ran). Read the docs for your
installed major (`npx next --version`) — blog posts from the Next 13/14 era describe the
opposite defaults.

Explicit controls (ran on 16.4.2, without `cacheComponents`):

```ts
await fetch(url, { cache: 'force-cache' });            // cache indefinitely
await fetch(url, { next: { revalidate: 3600 } });      // ISR: refresh at most hourly
await fetch(url, { next: { tags: ['products'] } });     // tag for on-demand invalidation
export const revalidate = 60;                           // segment-level default
export const dynamic = 'force-dynamic';                 // always per request
```

Using `cookies()`, `headers()` or `searchParams` makes a route dynamic. Run `next build`:
the route table marks each route static or dynamic — check it after every change.

## 3. Static generation of dynamic routes
```ts
export async function generateStaticParams() {
  const slugs = await getAllSlugs();
  return slugs.map(slug => ({ slug }));
}
export const dynamicParams = true;  // unknown slugs render on demand (false = 404)
```

## 4. Mutations: server actions
```tsx
// app/actions.ts
'use server';
import { revalidatePath } from 'next/cache';
export async function createPost(formData: FormData) {
  const session = await auth();                       // ALWAYS re-check auth here
  if (!session) throw new Error('Unauthorised');
  const title = z.string().min(1).parse(formData.get('title'));
  await db.post.create({ title });
  revalidatePath('/posts');                           // or revalidateTag('posts')
}
```
A server action is a public POST endpoint: validate input and authorise inside it, even if
the button is only shown to admins. Use `useActionState` for pending/error state. The
signature of `revalidateTag` is `revalidateTag(tag, profile)` in Next 16 (TypeScript rejects one argument; at runtime one argument still works with a deprecation warning and behaves like `{ expire: 0 }`). `revalidateTag('t', 'max')` is stale-while-revalidate: ran, the first request after the call served the stale value and the next served fresh data. In Server Actions prefer `updateTag(tag)` (read-your-own-writes); `updateTag` in a Route Handler throws (ran). Neither `revalidateTag` nor `updateTag` can be called from Proxy or Client Components.

## 5. Route handlers
`app/api/items/route.ts` exporting `GET`, `POST` etc. using Web `Request`/`Response`. Use
them for webhooks, third-party callers and non-React clients; prefer server actions for
your own forms.

## 6. Special files
| File | Purpose |
|---|---|
| `layout.tsx` | Persistent shell; does not re-render on navigation between children |
| `loading.tsx` | Suspense fallback for the segment; streams instantly |
| `error.tsx` | Error boundary — must be `'use client'`; gets `reset()` |
| `not-found.tsx` | Rendered by `notFound()` |
| `global-error.tsx` | Catches errors in the root layout |

Wrap slow parts in `<Suspense>` yourself for finer streaming than per-segment `loading.tsx`.

## 7. Middleware
`middleware.ts` at the project root runs before routing for redirects, rewrites, auth
gating and headers; restrict it with `export const config = { matcher: ['/dashboard/:path*'] }`.
In Next 16 the file is `proxy.ts` exporting `proxy` (a `middleware.ts` still builds on 16.4.2 but prints `The "middleware" file convention is deprecated. Please use "proxy" instead`; codemod: `npx @next/codemod@canary middleware-to-proxy .`). Proxy defaults to the Node.js runtime.
Keep it light and never rely on it as the only auth check; verify again in the page or action.

## Verify
- [ ] `'use client'` appears only on interactive leaf files; bundle analyser shows no server libs in client chunks.
- [ ] `next build` route table shows the static/dynamic status you intended.
- [ ] Every fetch or segment has an explicit cache/revalidate choice, not an assumed default.
- [ ] Every server action and route handler validates input and checks authorisation.
- [ ] Each segment with slow data has `loading.tsx` or a `<Suspense>` fallback, and an `error.tsx`.
