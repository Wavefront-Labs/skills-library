---
id: computing-software.web-development.sveltekit.sveltekit-page-layout-error-files
name: sveltekit-page-layout-error-files
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, routing-files, routing, page-svelte, layout-svelte, load, types, error-svelte]
level: intro
status: docs-checked
description: "Create SvelteKit +page, +layout and +error files, load data with +page.js or +page.server.js, and type them with $types."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/10-routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build routes from the `+` files in `src/routes`. Directories define URLs: `src/routes/about` gives `/about`; `src/routes/blog/[slug]` gives a route with parameter `slug`.

Rules: all files can run on the server; all run on the client except `+server` files; `+layout` and `+error` apply to subdirectories too.

## +page.svelte
```svelte
<!--- file: src/routes/blog/[slug]/+page.svelte --->
<script>
	/** @type {import('./$types').PageProps} */
	let { data } = $props();
</script>

<h1>{data.title}</h1>
<div>{@html data.content}</div>
```
Navigate with plain `<a>` elements (no `<Link>` component). From 2.24 pages also get a typed `params` prop.

## +page.js / +page.server.js
```js
/// file: src/routes/blog/[slug]/+page.js
import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export function load({ params }) {
	if (params.slug === 'hello-world') {
		return { title: 'Hello world!', content: '...' };
	}
	error(404, 'Not found');
}
```
`+page.js` runs on the server for SSR and in the browser on navigation. Rename to `+page.server.js` (type `PageServerLoad`) for server-only work (databases, private env vars); returned data must be serializable with devalue. Both can export `prerender`, `ssr`, `csr`. `+page.server.js` can also export `actions`.

## +layout.svelte / +layout.js / +layout.server.js
`src/routes/+layout.svelte` wraps pages and must render children:
```svelte
<script>
	let { children } = $props();
</script>

{@render children()}
```
Layouts nest; `+layout.js` `load` data (`LayoutLoad`, or `LayoutServerLoad` in `+layout.server.js`) is available to the layout and all child pages. Page options exported from a layout become defaults for children.

## +error.svelte
```svelte
<!--- file: src/routes/blog/[slug]/+error.svelte --->
<script>
	import { page } from '$app/state';
</script>

<h1>{page.status}: {page.error.message}</h1>
```
SvelteKit uses the closest `+error.svelte` walking up the tree. For errors in a `+layout(.server).js` load, the boundary is above that layout. If the root layout's load fails it uses the static `src/error.html`. It is not used for errors in `handle` or `+server.js`.

## $types
`PageProps` / `LayoutProps` (added in 2.16.0) type `data` (plus `form`, `children`). Annotate loads with `PageLoad`, `PageServerLoad`, `LayoutLoad`, `LayoutServerLoad`. VS Code and `svelte-check` can insert these automatically.

## Other files
Any non-`+` file in a route directory is ignored, so colocate components and tests (`+page.test.js`, etc.). Shared code belongs in `#lib`.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 20-core-concepts/10-routing.md in full: +page, +layout, +error rules, params prop, PageProps version note, error.html and the ignored-files rule. No claims trimmed.
