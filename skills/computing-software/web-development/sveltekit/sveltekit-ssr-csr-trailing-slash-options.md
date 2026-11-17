---
id: computing-software.web-development.sveltekit.sveltekit-ssr-csr-trailing-slash-options
name: sveltekit-ssr-csr-trailing-slash-options
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, ssr, csr, trailing-slash, config, page-options, spa, hydration]
level: practitioner
status: docs-checked
description: "Set the SvelteKit ssr, csr, trailingSlash and adapter config page options per page, per layout or app-wide, with their trade-offs."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/40-page-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: choose how each route is rendered and configured.

Options are exported from `+page.js` / `+page.server.js`, or from `+layout.js` / `+layout.server.js` for groups of pages; the root layout sets the app default; children override parents. By default SvelteKit renders on the server, then hydrates in the browser, where a router takes over.

## ssr
```js
export const ssr = false;   // renders an empty shell
```
Use when a page cannot render on the server (browser globals such as `document`). Mostly not recommended. In the root `+layout.js` it makes the whole app an SPA; do not do that if you want a statically generated site. If both `ssr` and `csr` are `false`, nothing is rendered.

If all page options are boolean or string literals SvelteKit evaluates them statically; otherwise it imports your `+page.js` / `+layout.js` on the server (at build time, and at runtime if not fully static). Then browser-only code must not run at module load: import it in the `.svelte` file instead.

## csr
```js
export const csr = false;
```
Ships no JavaScript: the page must work with HTML and CSS only; `<script>` tags in all Svelte components are removed; forms cannot be progressively enhanced; links cause full-page navigations; HMR is disabled. To keep HMR in development:
```js
import { dev } from '$app/env';
export const csr = dev;
```

## trailingSlash
Values: `'never'` (default; `/about/` redirects to `/about`), `'always'`, `'ignore'`. Also exportable from `+server.js`.
```js
// src/routes/+layout.js
export const trailingSlash = 'always';
```
It affects prerendering: `'always'` makes `/about` produce `about/index.html`, otherwise `about.html`. `'ignore'` is not recommended: relative paths differ (`./y` from `/x` is `/y`, from `/x/` is `/x/y`) and `/x` and `/x/` are separate URLs, bad for SEO.

## config
An object of adapter-specific settings; each adapter provides a `Config` type.
```js
/** @type {import('some-adapter').Config} */
export const config = { runtime: 'edge' };
```
Merging happens at the top level only, not deeper. Layout `{ runtime: 'edge', regions: 'all', foo: { bar: true } }` overridden by page `{ regions: ['us1', 'us2'], foo: { baz: true } }` yields `{ runtime: 'edge', regions: ['us1', 'us2'], foo: { baz: true } }`.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 20-core-concepts/40-page-options.md in full, focusing on ssr, csr, trailingSlash and option merging. No claims trimmed.
