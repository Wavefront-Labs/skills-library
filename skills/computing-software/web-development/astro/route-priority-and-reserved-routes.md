---
id: computing-software.web-development.astro.route-priority-and-reserved-routes
name: route-priority-and-reserved-routes
category: computing-software
field: web-development
product: astro
tags: [route-priority, reserved-routes, route-conflicts, endpoints]
level: practitioner
status: docs-checked
description: "Resolve conflicts when several Astro routes match the same URL using the priority rules, and avoid Astro's reserved routes _astro, _server_islands, _actions."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/routing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When multiple routes can build the same URL (e.g. all of `[...slug].astro`, `posts/create.astro`, `posts/[page].astro`, `posts/[pid].ts`, `posts/[...slug].astro` could build `/posts/create`), Astro sorts them by these rules in order:

- Astro reserved routes
- Routes with more path segments beat less specific routes
- Static routes without parameters beat dynamic routes
- Dynamic routes with named parameters beat rest parameters
- Pre-rendered dynamic routes beat server dynamic routes
- Endpoints beat pages
- File-based routes beat redirects
- Otherwise, alphabetical by the default locale of your Node installation

Results for the example:

- `pages/posts/create.astro` builds only `/posts/create`
- `pages/posts/[pid].ts` builds `/posts/abc`, `/posts/xyz`, but not `/posts/create`
- `pages/posts/[page].astro` builds `/posts/1`, `/posts/2`, but not `/posts/create`, `/posts/abc` nor `/posts/xyz`
- `pages/posts/[...slug].astro` builds `/posts/1/2`, `/posts/a/b/c`
- `pages/[...slug].astro` builds `/abc`, `/xyz`, `/abc/xyz`

Reserved routes take priority over user or integration routes:

- `_astro/`: static assets, including CSS, bundled client scripts, optimized images and Vite assets
- `_server_islands/`: dynamic components deferred into a server island
- `_actions/`: defined actions

## Checked

2026-11-04. Confirmed against the Astro routing guide: the priority rule order, the per-file build results and the three reserved routes. Nothing removed.

Method: documentation only; no commands were run.
