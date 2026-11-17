---
id: computing-software.web-development.sveltekit.sveltekit-build-and-preview
name: sveltekit-build-and-preview
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, building, build-stages, vite-build, preview]
level: intro
status: docs-checked
description: "Understand SvelteKit's two-stage vite build, guard build-time code with the building flag, and preview the production build locally."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/10-building-your-app.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: build a SvelteKit app for production without running runtime-only code during the build, then preview it.

## The two stages
Both happen in `vite build` (usually `npm run build`):
1. Vite makes an optimized production build of server code, browser code and the service worker (if any). Prerendering runs at this stage when appropriate.
2. An adapter takes that output and tunes it for the deployment target.

## Guard code that must not run at build time
During the build SvelteKit loads your `+page/layout(.server).js` files and everything they import, to analyse them. Any code that should not execute then (opening a database, for example) must check that `building` from `$app/env` is `false`:

```js
import { building } from '$app/env';
import { initialiseDatabase } from '#lib/server/database.js';

if (!building) {
	initialiseDatabase();
}

export function load() {
	// ...
}
```

## Preview locally
After building, run `vite preview` (via `npm run preview`) to view the production build.

## Gotcha
Preview runs the app in Node, so it is not a perfect reproduction of the deployed app. Adapter-specific adjustments, such as the `platform` object, do not apply to previews.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `25-build-and-deploy/10-building-your-app.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
