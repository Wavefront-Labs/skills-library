---
id: computing-software.web-development.nextjs.layouts-templates-and-nested-routes
name: layouts-templates-and-nested-routes
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, nextjs-layouts, app-router, nested-routes, root-layout, template-tsx, web-development]
level: practitioner
status: verified
description: "Structuring Next.js App Router layouts: root layout requirements, nested layouts, layout vs template, what layouts can't access, and shared UI state."
sources:
  - https://nextjs.org/docs/app/getting-started/layouts-and-pages
  - https://nextjs.org/docs/app/api-reference/file-conventions/layout
  - https://nextjs.org/docs/app/api-reference/file-conventions/template
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Layouts, templates and nested routes

**Goal:** shared UI that persists across navigations without re-fetching or losing state, and pages that compose cleanly.

## 1. File conventions
```
app/
  layout.tsx            # root layout (required)
  page.tsx              # /
  dashboard/
    layout.tsx          # wraps everything under /dashboard
    page.tsx            # /dashboard
    settings/page.tsx   # /dashboard/settings
```
A folder is a route segment; it's only publicly routable when it contains `page.tsx` (or `route.ts`).

## 2. Root layout
```tsx
export const metadata = { title: { default: "Acme", template: "%s | Acme" } };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
```
Must render `<html>` and `<body>`. Don't add `<head>` tags manually - use the Metadata API.

## 3. Layout behaviour
- Layouts **persist** on navigation between their child routes: they don't re-render, state in client components inside them survives, their data isn't refetched.
- Layouts don't receive `searchParams`, and don't know the current pathname on the server (they'd be stale). Read them in the page, or in a client component with `usePathname()`/`useSearchParams()`.
- Layouts receive `params` for their segment and parents (a Promise in Next 15+: `const { team } = await params`).
- Data needed in both layout and page: fetch in both; requests are deduplicated (`fetch` memoisation or React `cache()`).

## 4. Template vs layout
`template.tsx` has the same shape but **remounts** on every navigation: new state, effects re-run. Use for enter animations, per-page `useEffect` logging, or resetting forms. Default to layouts.

## 5. Active nav links
```tsx
"use client";
export function NavLink({ href, children }) {
  const active = usePathname().startsWith(href);
  return <Link href={href} aria-current={active ? "page" : undefined}>{children}</Link>;
}
```
Keep the layout itself a server component; make only the link a client component.

## 6. Pitfalls
- Auth checks in a layout don't run on client-side navigation between its children (the layout doesn't re-render). Check in pages / data access layer.
- Heavy client providers in the root layout make the whole app client-bound at that point; pass server components as `children`.

Checked against the 16.4.2 docs shipped in the `next` package: layouts preserve state, stay interactive and do not re-render on navigation; they cannot read `searchParams` or the pathname (use the page `searchParams` prop or `useSearchParams`/`usePathname` in a Client Component); the root layout must define `<html>` and `<body>` and should not hold manual `<head>` tags (use the Metadata API); a template gets a unique key per segment level and remounts when that segment (including its dynamic params) changes, but search-param changes and navigations deeper in the tree do not remount higher templates.

## Verify
- [ ] Navigating between sibling routes keeps layout client state (e.g. sidebar scroll, input text).
- [ ] React DevTools shows the layout not re-rendering on child navigation.
- [ ] Each page sets its own `metadata.title` through the template.
