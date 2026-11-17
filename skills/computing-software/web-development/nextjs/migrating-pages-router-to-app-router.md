---
id: computing-software.web-development.nextjs.migrating-pages-router-to-app-router
name: migrating-pages-router-to-app-router
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, pages-router-migration, app-router, getserversideprops, getstaticprops, incremental-adoption, web-development]
level: practitioner
status: docs-checked
description: "Incrementally migrating Next.js from the Pages Router to the App Router: coexistence, mapping data-fetching APIs, _app/_document, next/router and head."
sources:
  - https://nextjs.org/docs/app/guides/migrating/app-router-migration
  - https://nextjs.org/docs/pages/building-your-application/data-fetching
  - https://nextjs.org/docs/app/api-reference/functions/generate-static-params
  - https://nextjs.org/docs/app/guides/upgrading/version-16
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating Pages Router to App Router

**Goal:** move route by route with the app working at every step.

## 1. Coexistence
`pages/` and `app/` work side by side. Move one route at a time. Navigating between the two routers is a hard navigation (full reload) - migrate tightly linked routes together.

Upgrade Next and React first (`npx @next/codemod@canary upgrade latest`, the command in the Next upgrade guides), then migrate.

## 2. Map the concepts
| Pages Router | App Router |
|---|---|
| `pages/_app.tsx`, `_document.tsx` | `app/layout.tsx` (root layout with `<html><body>`), client providers component |
| `next/head` | `export const metadata` / `generateMetadata` |
| `getServerSideProps` | async server component with uncached fetch / dynamic API |
| `getStaticProps` + `revalidate` | cached fetch (`cache: "force-cache"`, `next: { revalidate }`) or `"use cache"` |
| `getStaticPaths` | `generateStaticParams` |
| `fallback: false` | `export const dynamicParams = false` |
| `next/router` `useRouter` | `next/navigation`: `useRouter`, `usePathname`, `useSearchParams` |
| `router.query` | `params`/`searchParams` props (Promises in 15+) |
| `pages/api/*` | can stay, or `app/**/route.ts` route handlers |
| `pages/404.tsx`, `_error.tsx` | `not-found.tsx`, `error.tsx`, `global-error.tsx` |

## 3. A page conversion
```tsx
// before: pages/posts/[id].tsx with getServerSideProps
// after: app/posts/[id]/page.tsx
export default async function Post({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const post = await getPost(id);
  if (!post) notFound();
  return <PostView post={post} />;            // existing component; add "use client" if it uses hooks
}
```
Start by moving the old page component into the app route as a client component, then push data fetching up to the server component.

## 4. Things that change behaviour
- `useRouter().events` don't exist; use `usePathname` + `useSearchParams` in an effect for analytics.
- CSS: global CSS can be imported in any layout; CSS-in-JS libraries need extra setup for server rendering (see Next's CSS-in-JS guide).
- `fetch` caching semantics differ by Next version (not cached by default in 15+).
- `next/link` no longer needs a child `<a>` (since 13).

## 5. Order of work
Root layout + providers -> leaf static pages -> dynamic pages -> pages with forms (convert to server actions optionally) -> remove `_app`/`_document` when `pages/` is empty.

## Verify
- [ ] Every migrated route has the same metadata, status codes and HTML output (diff `curl` results).
- [ ] Analytics page views fire on App Router navigations.
- [ ] No route is served by both `pages/` and `app/`.

## Checked
Date: 2026-10-25. Documentation: Next.js documentation source (vercel/next.js canary, commit of 2026-10-24; latest release v16.4.3) (guides/migrating/app-router-migration, upgrading version-15 and version-16).
Confirmed: hard navigation between routers, `_app`/`_document` replaced by the root layout, `_error`/404 replaced by `error.js`/`not-found.js`, `pages/api` keeps working, `useRouter` from `next/navigation` without events or `query`, `<Link>` without a child `<a>` (default since 13), `fallback` replaced via `generateStaticParams` and `dynamicParams`, `fetch` caching changes in 15, upgrade command with `@next/codemod@canary`.
Corrected or removed: the "same path is a build error" claim (not documented), the `@latest` upgrade command, and the styled-components/emotion registry wording.
Method: documentation only; no commands were run.
