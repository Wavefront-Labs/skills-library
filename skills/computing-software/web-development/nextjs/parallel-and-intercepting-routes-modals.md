---
id: computing-software.web-development.nextjs.parallel-and-intercepting-routes-modals
name: parallel-and-intercepting-routes-modals
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, parallel-routes, intercepting-routes, modals, slots, default-tsx, app-router, web-development]
level: practitioner
status: verified
description: "Building URL-addressable modals and dashboards in Next.js with parallel routes (@slots, default.tsx) and intercepting routes ((.), (..), (...))."
sources:
  - https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes
  - https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes
  - https://github.com/vercel/nextgram
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parallel and intercepting routes (modals)

**Goal:** a photo/login modal that opens over the current page on soft navigation, is shareable by URL, shows a full page on reload, and closes with Back.

## 1. Parallel routes: slots
`@name` folders are slots passed to the parent layout as props:
```tsx
// app/layout.tsx
export default function Layout({ children, modal }: { children: React.ReactNode; modal: React.ReactNode }) {
  return <>{children}{modal}</>;
}
```
Slots are not URL segments. Each slot can have its own `loading.tsx`/`error.tsx` - good for dashboards with independently streaming panels (`@analytics`, `@team`).

## 2. default.tsx is required
On a hard navigation/reload Next can't recover a slot's active state for unmatched URLs. Ran on 16.4.2: with `@modal/(.)photos/[id]/page.tsx` and no `@modal/default.tsx`, `next build` fails with `Interception routes must have a canonical route` (older versions rendered a 404 for unmatched URLs). Add:
```tsx
// app/@modal/default.tsx
export default function Default() { return null; }
```
Also add `app/default.tsx` if `children` may be unmatched.

## 3. Intercepting routes
Prefix a folder to intercept a route from another part of the tree during **client-side** navigation:
- `(.)` same level, `(..)` one level up, `(..)(..)` two levels, `(...)` from app root.
Levels are route segments, not file-system folders (slots don't count).

## 4. The modal pattern
```
app/
  layout.tsx                         # renders {children}{modal}
  @modal/default.tsx                 # null
  @modal/(.)photos/[id]/page.tsx     # modal version
  photos/[id]/page.tsx               # full-page version (direct visit / reload)
  page.tsx                           # gallery with <Link href={`/photos/${id}`}>
```
```tsx
// app/@modal/(.)photos/[id]/page.tsx
export default async function PhotoModal({ params }) {
  const { id } = await params;
  return <Modal><Photo id={id} /></Modal>;
}
// Modal.tsx (client)
"use client";
export function Modal({ children }) {
  const router = useRouter();
  return <dialog open onClose={() => router.back()}>{children}</dialog>;
}
```

## 5. Closing on other navigations
The slot keeps its state when navigating elsewhere with `<Link>`. Add a catch-all that returns null so the modal clears:
```
app/@modal/[...catchAll]/page.tsx   -> export default () => null
```

## 6. Gotchas
- Interception only happens on soft navigation; reload always shows the full page.
- Conditional slot rendering by role (`isAdmin ? admin : user`) works for auth-based layouts.
- Restart the dev server after adding new slots if they don't appear.

Ran on a 16.4.2 production build with this exact layout (`app/layout.tsx` rendering `{children}{modal}`, `@modal/default.tsx`, `@modal/(.)photos/[id]/page.tsx`, `photos/[id]/page.tsx`, a `<Link href="/photos/1">` on `/`): clicking the link kept the same document (a JS marker survived), the URL became `/photos/1` and the body showed the home page plus the modal; `history.back()` returned to `/` without the modal; loading `/photos/1` directly rendered only the full page. A build while a client was connected to an older server instance fell back to a full page load, so restart the server after rebuilding when testing.

## Verify
- [ ] Click opens modal over gallery; URL updates; Back closes it.
- [ ] Reloading the modal URL shows the full photo page.
- [ ] Navigating away via a link removes the modal.
