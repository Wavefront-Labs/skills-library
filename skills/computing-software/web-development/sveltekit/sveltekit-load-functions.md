---
id: computing-software.web-development.sveltekit.sveltekit-load-functions
name: sveltekit-load-functions
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, load, load-functions, page-data, layout-data, universal-vs-server, svelte]
level: intro
status: docs-checked
description: "Write SvelteKit load functions for pages and layouts and choose between universal (+page.js) and server (+page.server.js) variants."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/20-load.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get data into a page or layout before it renders, using the right kind of `load` function.

## Page and layout data
- `+page.js` exports `load({ params })`; the returned object arrives in `+page.svelte` as the `data` prop.
- `+layout.js` / `+layout.server.js` work the same for `+layout.svelte` (`let { data, children } = $props()`, render the page with `{@render children()}`).
- Type props with `import('./$types').PageProps` / `LayoutProps` (since 2.16.0; earlier you typed `PageData` / `LayoutData` individually).

```js
// src/routes/blog/[slug]/+page.server.js
import * as db from '#lib/server/database.js';

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
	return { post: await db.getPost(params.slug) };
}
```

Layout data is available to child layouts and the page. If several `load` functions return the same key, the last one wins: layout `{ a: 1, b: 2 }` plus page `{ b: 3, c: 4 }` gives `{ a: 1, b: 3, c: 4 }`.

A parent layout that needs child page data can read `page.data` from `$app/state` (typed by `App.PageData`), e.g. `<title>{page.data.title}</title>` in the root layout.

## Universal vs server
- Universal (`+page.js`, `+layout.js`): runs on the server during SSR, again in the browser during hydration (reusing fetch responses), and in the browser for later navigations. Can return anything, including class instances and component constructors. If SSR is disabled it always runs on the client.
- Server (`+page.server.js`, `+layout.server.js`): always runs on the server. Gets a `ServerLoadEvent` (adds `cookies`, `getClientAddress`, `locals`, `platform`, `request`). The return value must be serializable by devalue (JSON plus `BigInt`, `Date`, `Map`, `Set`, `RegExp`, repeated or cyclical references); promises are streamed. Custom types need a `transport` hook.
- Use server for databases, the filesystem and private env vars. Use universal to fetch an external API with no private credentials, or to return non-serializable values.
- If both exist, the server `load` runs first and its result is the `data` property of the universal `load` argument:

```js
// +page.js
export async function load({ data }) {
	return { serverMessage: data.serverMessage, universalMessage: 'hello from universal load function' };
}
```

`load` runs at runtime, or at build time if the page is prerendered.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `20-core-concepts/20-load.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
