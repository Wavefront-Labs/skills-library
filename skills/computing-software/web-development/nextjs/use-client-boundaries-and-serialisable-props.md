---
id: computing-software.web-development.nextjs.use-client-boundaries-and-serialisable-props
name: use-client-boundaries-and-serialisable-props
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, use-client-boundary, react-server-components, client-components, serialisable-props, composition, web-development, serializable-props, context-providers-app-router]
level: practitioner
status: verified
description: "Placing 'use client' boundaries in Next.js: what crosses the boundary, serialisable props, passing server components as children and keeping client bundles small."
sources:
  - https://nextjs.org/docs/app/getting-started/server-and-client-components
  - https://react.dev/reference/rsc/use-client
  - https://react.dev/reference/rsc/server-components
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# 'use client' boundaries and serialisable props

**Goal:** keep most of the tree on the server, push interactivity to small leaf client components.

## 1. What the directive means
`"use client"` at the top of a file marks it - and every module it imports - as part of the client bundle. It's a boundary, not a per-component flag. Components without it are server components by default in `app/`.

## 2. Push the boundary to the leaves
```tsx
// app/products/[id]/page.tsx  (server)
export default async function Page({ params }) {
  const { id } = await params;
  const product = await getProduct(id);
  return <article><h1>{product.name}</h1><p>{product.description}</p><AddToCart id={product.id} /></article>;
}
// AddToCart.tsx
"use client";
export function AddToCart({ id }: { id: string }) { const [n, setN] = useState(1); ... }
```
Marking the whole page client ships the markdown renderer, data mappers and their dependencies to the browser.

## 3. Props must be serialisable
Server -> client props are serialised (RSC payload). Allowed (React `use client` docs; ran on 16.4.2 for `Date`, `Map`, `Set`, `BigInt` and a Promise): primitives (including bigint), strings, arrays, `Map`, `Set`, typed arrays and `ArrayBuffer`, `Date`, plain objects, Promises, JSX, and **Server Functions**. Not allowed: ordinary functions/event handlers, class instances (ORM models with methods), and symbols other than global-registry ones made with `Symbol.for`. Pass `product.toJSON()`-style DTOs - also prevents leaking columns.

## 4. Server components inside client components
A client component can't import a server component, but it can receive one as `children` or any prop:
```tsx
// Providers.tsx
"use client";
export function Providers({ children }) { return <ThemeProvider><QueryClientProvider client={qc}>{children}</QueryClientProvider></ThemeProvider>; }
// layout.tsx (server)
<Providers><ServerSidebar /></Providers>
```

## 5. Third-party components
Libraries that use hooks but lack the directive fail in server components. Wrap them: `"use client"; export { Carousel } from "acme-carousel";`.

## 6. Client components still SSR
"Client" means it also hydrates in the browser; it still renders to HTML on the server. Guard browser APIs (`window`, `localStorage`) in effects, or use `next/dynamic(..., { ssr: false })` in a client component for browser-only libraries.

## 7. Sharing data
Context works only in client components. For request data on the server use React `cache()`-wrapped functions instead of context.

## Verify
- [ ] Build output / bundle analyser: large server-only libs (markdown, date-fns-tz, ORM) absent from client chunks.
- [ ] No "Functions cannot be passed directly to Client Components" errors.
- [ ] `grep -rl '"use client"' app | wc -l` - each one is a deliberate interactive leaf or provider.
