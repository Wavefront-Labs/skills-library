---
id: computing-software.web-development.sveltekit.sveltekit-prerender-entries
name: sveltekit-prerender-entries
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, prerender, entries, static, ssg, page-options, build]
level: practitioner
status: docs-checked
description: "Enable SvelteKit prerendering, feed dynamic routes to the crawler with entries, and fix the 'marked as prerenderable but were not prerendered' error."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/40-page-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: generate routes as static HTML at build time and make sure every dynamic route is reached.

## Turn it on
Export from `+page.js`, `+page.server.js` or `+server.js`, or from a root `+layout.js` / `+layout.server.js` for the whole app (children override parents):
```js
export const prerender = true;   // or false, or 'auto'
```
- `true`: prerendered and excluded from the dynamic SSR manifest (smaller server).
- `'auto'`: prerendered but still in the manifest, so the long tail can be server-rendered (e.g. `/blog/[slug]`).
- `false`: set it on pages that must stay dynamic when the layout says `true`.
If the whole app is prerenderable, `adapter-static` outputs files for any static server. While prerendering, `building` is `true`.

## How routes are found
The prerenderer starts at the app root and follows `<a>` links to other prerenderable pages. By default all non-dynamic routes are entry points. Add others via `config.prerender.entries`, or export `entries` from a dynamic route (can be `async`, e.g. to query a CMS):
```js
// src/routes/blog/[slug]/+page.server.js
/** @type {import('./$types').EntryGenerator} */
export function entries() {
	return [{ slug: 'hello-world' }, { slug: 'another-blog-post' }];
}

export const prerender = true;
```

## Rules
- A page is prerenderable only if any two users hitting it directly get the same content. Personalised data can be fetched in `onMount`, at the cost of blank content or loaders.
- Pages may still load data from route parameters.
- `url.searchParams` is forbidden during prerendering; use it only in the browser (e.g. `onMount`).
- Pages with form actions cannot be prerendered.
- `prerender` also applies to `+server.js`, which ignores layouts but inherits from the pages that fetch it: if a prerendered `+page.js` does `fetch('/my-server-route.json')`, that `+server.js` is prerendered unless it exports `prerender = false`.
- Filesystem conflicts: `src/routes/foo/+server.js` and `src/routes/foo/bar/+server.js` would need both a file and a directory named `foo`. Use extensions (`foo.json`, `foo/bar.json`). Pages write `foo/index.html`.

## Troubleshooting
Error "The following routes were marked as prerenderable, but were not prerendered" means the crawler never reached a route (or its parent layout) with `prerender = true`. Fix by: adding the route to `config.prerender.entries` or the `entries` option (dynamic routes need parameter values); linking to it from another prerendered, SSR-enabled page (pages not marked prerenderable are not crawled); or changing `true` to `'auto'`.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 20-core-concepts/40-page-options.md in full, focusing on prerender, entries, route conflicts and troubleshooting. No claims trimmed.
