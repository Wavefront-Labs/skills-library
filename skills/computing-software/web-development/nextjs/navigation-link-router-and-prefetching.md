---
id: computing-software.web-development.nextjs.navigation-link-router-and-prefetching
name: navigation-link-router-and-prefetching
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, nextjs-navigation, nextjs-prefetching, next-link, userouter, redirect, client-navigation, web-development]
level: practitioner
status: verified
description: "Navigating in the Next.js App Router: Link and prefetch behaviour, useRouter, redirect/permanentRedirect, scroll handling, pending state and soft vs hard navigation."
sources:
  - https://nextjs.org/docs/app/getting-started/linking-and-navigating
  - https://nextjs.org/docs/app/api-reference/components/link
  - https://nextjs.org/docs/app/api-reference/functions/use-router
  - https://nextjs.org/docs/app/api-reference/functions/redirect
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Navigation: Link, useRouter, redirect, prefetching

**Goal:** fast client-side navigation with correct prefetching and server-side redirects.

## 1. `<Link>` first
```tsx
import Link from "next/link";
<Link href={`/posts/${post.slug}`}>Read</Link>
<Link href="/search?q=next" scroll={false} replace>Search</Link>
```
Renders a real `<a>` (works without JS, middle-click, SEO). Soft navigation keeps shared layouts and client state.

## 2. Prefetching (production only)
- Links prefetch when they enter the viewport (and on hover).
- Static routes: the full route payload is prefetched.
- Dynamic routes: prefetched down to the nearest `loading.tsx`, so the skeleton shows instantly.
- `prefetch={false}` for huge link lists (footers, tables of thousands); `prefetch={true}` forces full prefetch of dynamic routes.
- Prefetching doesn't happen in `next dev` - test in `next build && next start`.

## 3. useRouter (client components)
```tsx
"use client";
import { useRouter } from "next/navigation";      // not next/router (Pages Router)
const router = useRouter();
router.push("/dashboard"); router.replace("/login"); router.back();
router.refresh();      // re-fetch server components for the current route, keep client state
router.prefetch("/checkout");
```
Use for navigation after an event (post-submit). For plain links use `<Link>`.

## 4. Server redirects
```tsx
import { redirect, permanentRedirect } from "next/navigation";
if (!session) redirect("/login");            // 307 (303 in server actions)
permanentRedirect("/new-slug");              // 308
```
Works in server components, actions and route handlers. It throws - don't call inside try/catch. In route handlers you can also `return NextResponse.redirect(url)`. Static redirect maps belong in `next.config` `redirects()`.

## 5. Reading location
`usePathname()`, `useSearchParams()` (wrap the component in `<Suspense>` on static routes), `useParams()`, `useSelectedLayoutSegment()`.

## 6. Pending UI
Navigations are transitions; the old page stays until the new one is ready (unless a `loading.tsx` shows). `useLinkStatus()` (Next 15.3+) inside a Link child gives a per-link pending flag.

## 7. Hard navigations
Happen across multiple root layouts, to external URLs, between Pages and App Router, and with `<a>` tags. Use `<Link>` for internal links.

Ran on a 16.4.2 production build: `redirect('/dashboard')` in a page answers 307 with `location: /dashboard`; `permanentRedirect` answers 308; `redirect()` after streaming started returns HTTP 200 with a `NEXT_REDIRECT;replace;/dashboard;307;` meta/payload instead of a Location header; a Server Action's redirect is 303 only for no-JS form posts (client-side navigation otherwise), per the redirect docs. `useLinkStatus` was introduced in v15.3.0 (docs version history). Route groups with different root layouts cause a full page load (route-groups docs).

## Verify
- [ ] Production build: hovering/visible links show prefetch requests in the Network tab.
- [ ] `curl -I` on a redirected path shows 307/308 with the right Location.
- [ ] No imports from `next/router` in `app/`.
