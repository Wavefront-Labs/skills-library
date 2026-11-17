---
id: computing-software.web-development.sveltekit.sveltekit-migrate-from-sapper
name: sveltekit-migrate-from-sapper
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, sapper, migration, migrate-sapper, routing, package-json, app-html]
level: practitioner
status: docs-checked
description: "Convert a Sapper app to SvelteKit: package.json and scripts, config, template and route file renames, preload to load, stores, URLs and endpoints."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/60-appendix/40-migrating.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: port an existing Sapper app to SvelteKit step by step. Examples of migrated apps are linked from the additional-resources page.

## package.json
- Add `"type": "module"` (separable step if Sapper is 0.29.3+).
- Remove `polka`/`express` and middleware such as `sirv`, `compression`. Replace `sapper` with `@sveltejs/kit` plus an adapter.
- Scripts: `sapper build` becomes `vite build` with adapter-node; `sapper export` becomes `vite build` with adapter-static; `sapper dev` becomes `vite dev`; `node __sapper__/build` becomes `node build`.

## Project files
- `webpack.config.js`/`rollup.config.js` become `vite.config.js`; preprocessor options go to the plugin `config.preprocess` setting. Find Vite equivalents for any filetype plugins.
- `src/client.js` has no equivalent; put custom logic in `+layout.svelte` inside `onMount`.
- `src/server.js`: with adapter-node use a custom server; otherwise no equivalent.
- `src/service-worker.js`: `@sapper/service-worker` imports map to `$service-worker`: `files` unchanged, `routes` removed, `shell` is `build`, `timestamp` is `version`.
- `src/template.html` becomes `src/app.html`: drop `%sapper.base%`, `%sapper.scripts%`, `%sapper.styles%`; `%sapper.head%` becomes `%sveltekit.head%`, `%sapper.html%` becomes `%sveltekit.body%`; the `<div id="sapper">` is unnecessary.
- `src/node_modules` does not work with Vite; use `src/lib` instead (imports via the lib alias).

## Pages and layouts
- `routes/about/index.svelte` and `routes/about.svelte` both become `routes/about/+page.svelte`; `_error.svelte` becomes `+error.svelte`; `_layout.svelte` becomes `+layout.svelte`; other files are ignored.
- `goto`, `prefetch`, `prefetchRoutes` from `@sapper/app` become `goto`, `preloadData`, `preloadCode` from `$app/navigation`.
- `preload` becomes `load` in `+page.js`/`+layout.js`, taking a single `event` argument instead of `page` and `session`. No `this`: use the `fetch` from the event, and `error`/`redirect` helpers.
- Stores: `stores()` becomes `getStores`, though you can import `page` and `navigating` from `$app/stores` directly (or `$app/state` on Svelte 5 with SvelteKit 2.12+). `preloading` is replaced by `navigating` with `from`/`to`. `page` has `url` and `params`, no `path` or `query`.
- Regex routes are gone: use advanced route matching. The `segment` prop is gone: derive it from `page.url.pathname`.
- Relative URLs now resolve against the current page, not the base; root-relative (`/...`) URLs are simpler.
- `sapper:prefetch` becomes `data-sveltekit-preload-data`; `sapper:noscroll` becomes `data-sveltekit-reset="false"`.

## Endpoints
No `req`/`res`; rewrite endpoints to the SvelteKit signature. `fetch` is global, so drop `node-fetch`/`cross-fetch`.

## HTML minifier
Not built in. Add `html-minifier` as a prod dependency and use the `handle` hook's `resolve(event, { transformPageChunk })`, accumulating `html` and calling `minify(page, options)` when `done` and the build flag from the env module is true. `prerendering` is false under `vite preview`, so inspect built HTML files to check minification.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `60-appendix/40-migrating.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
