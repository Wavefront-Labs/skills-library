---
id: computing-software.web-development.nextjs.route-groups-and-private-folders
name: route-groups-and-private-folders
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, route-groups, private-folders, colocation, multiple-root-layouts, app-router, web-development]
level: practitioner
status: verified
description: "Organising the Next.js app directory with route groups for layouts and sections, private _folders for colocated code, and multiple root layouts."
sources:
  - https://nextjs.org/docs/app/api-reference/file-conventions/route-groups
  - https://nextjs.org/docs/app/getting-started/project-structure
  - https://nextjs.org/docs/app/getting-started/project-structure#private-folders
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route groups and private folders

**Goal:** organise routes by team, section or layout without affecting URLs, and colocate components safely.

## 1. Route groups `(name)`
A folder in parentheses is omitted from the URL:
```
app/
  (marketing)/
    layout.tsx          # marketing header/footer
    page.tsx            # /
    pricing/page.tsx    # /pricing
  (app)/
    layout.tsx          # authenticated shell
    dashboard/page.tsx  # /dashboard
```
Uses: different layouts for sections at the same URL level; opting specific routes into a layout (`(with-sidebar)/a`, `(with-sidebar)/b`); grouping by team ownership; scoping `loading.tsx` to a subset of routes.

## 2. Multiple root layouts
Remove the top-level `app/layout.tsx` and give each group its own layout with `<html><body>`. Navigating **between** root layouts triggers a full page load. Useful for genuinely separate apps (marketing vs product), not for minor variations.

## 3. Conflicts
Two groups resolving to the same path (`(a)/about/page.tsx` and `(b)/about/page.tsx`) is a build error. If you have multiple root layouts with no top-level `page.tsx`, the home page must live inside one group.

## 4. Private folders `_name`
```
app/dashboard/
  _components/Chart.tsx
  _lib/queries.ts
  page.tsx
```
Underscore folders are excluded from routing entirely. Files other than `page`/`route` are already unroutable when colocated, but `_` makes intent explicit, avoids clashes with future file conventions, and sorts together in editors. URL segments starting with underscore need `%5F` folder names.

## 5. Project structure choices
Pick one and stay consistent:
- Everything outside `app/` (`src/components`, `src/lib`), `app/` only for routing.
- Colocate feature code in `_components` per route.
- Split by feature/route with shared code at root.
`src/` directory is supported (`src/app`); config files stay at the project root.

Ran on 16.4.2: `app/(marketing)/pricing/page.tsx` appeared as `/pricing` in the build route table; `(a)/about` plus `(b)/about` failed the build with `You cannot have two parallel pages that resolve to the same path`. The project-structure docs confirm that `_folder` is excluded from routing and that a literal underscore URL segment uses `%5F`, and the route-groups docs confirm that navigating between different root layouts triggers a full page load.

## Verify
- [ ] `next build` route list shows expected URLs (no group names in paths).
- [ ] Navigating marketing -> app shows the intended layout swap; full reload only where multiple root layouts are intended.
- [ ] No `_components` files appear as routes.
