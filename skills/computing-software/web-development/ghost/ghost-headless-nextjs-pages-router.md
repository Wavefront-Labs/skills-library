---
id: computing-software.web-development.ghost.ghost-headless-nextjs-pages-router
name: ghost-headless-nextjs-pages-router
category: computing-software
field: web-development
product: ghost
tags: [ghost, nextjs, headless, jamstack, content-api, react, vercel]
level: advanced
status: docs-checked
description: "Use Ghost as a headless backend for a Next.js site: prerequisites, pages router setup and the Content API client."
sources:
  - https://github.com/TryGhost/docs/blob/main/jamstack/next.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build a Next.js front end that reads Ghost content.

Prerequisites from the guide: moderate knowledge of JavaScript and React, and a Ghost site (self-hosted or Ghost(Pro)). Create the app with `yarn create next-app`. The guide answers "No" to every prompt for simplicity (TypeScript, ESLint, Tailwind CSS, `src/` directory, App Router, Turbopack, import alias), so it uses the pages router, not the app router. Start it with `yarn dev`.

Pattern:
1. Create a custom integration in Ghost Admin to generate the key. The URL is the Ghost URL ending in `.ghost.io` for Ghost(Pro), or the URL used to view the admin panel when self-hosted.
2. `yarn add @tryghost/content-api`, then in `lib/posts.js` create `new GhostContentAPI({ url, key, version })` (the guide's sample uses `version: "v6.0"`).
3. Export async functions that call `api.posts.browse({ limit: 15 })` (default 15, max 100) and, for one post, `api.posts.read({ slug })`.
4. Render lists from `getStaticProps` in `pages/index.js`; return `{ notFound: true }` when nothing comes back.
5. For single posts, use the dynamic route file `pages/posts/[slug].js` with `getStaticPaths` (guide uses `fallback: false`) and `getStaticProps`. `getAllPostSlugs` pages through results with `limit: 100`, `page` and `fields: "slug"`, following `meta.pagination.next`, because 100 is the maximum per request.
6. Add tags and authors to posts with `include: "tags,authors"`. Pages use `api.pages.browse`, authors use `api.authors.read({ slug })`.
7. Link with the Next.js `Link` component. The `html` field is rendered via `dangerouslySetInnerHTML`, and the guide notes it only populates for public posts in its example.

Tip: format `post.published_at` with `Intl.DateTimeFormat` for display.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 409-line next.mdx, no imported snippets). Removed as not on the page: step to rebuild via a Ghost webhook and build hook, advice about the Admin API key and environment variables, the cache `maxAge` tip, "No" described for only four prompts (page says all seven), and the Verify step. Added the browse, read, pagination and routing details from the page.
Method: documentation only; no commands were run.
