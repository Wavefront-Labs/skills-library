---
id: computing-software.web-development.sveltekit.sveltekit-adapter-static-and-github-pages
name: sveltekit-adapter-static-and-github-pages
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, adapter-static, ssg, prerender, github-pages]
level: practitioner
status: docs-checked
description: "Generate a fully prerendered SvelteKit site with adapter-static, set its options, and deploy to GitHub Pages with the base path and workflow."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/50-adapter-static.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: publish SvelteKit as static files. To prerender only some pages and server-render others, use a different adapter plus the `prerender` option.

## Setup
`npx sv add sveltekit-adapter="adapter:static"` or `npm i -D @sveltejs/adapter-static`, then:
```js
import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		sveltekit({
			adapter: adapter({
				// defaults shown
				pages: 'build',
				assets: 'build',
				fallback: undefined,
				precompress: false,
				strict: true
			})
		})
	]
});
```
and in the root layout:
```js
// src/routes/+layout.js
export const prerender = true;
```
On Vercel (zero-config), omit the adapter options so the adapter picks the optimal config.

## Options
- `pages`: where prerendered pages go. `assets`: where `static` plus generated JS/CSS go (defaults to `pages`).
- `fallback`: name of a fallback page, making it a single-page app (see the SPA skill); large performance and SEO cost.
- `precompress`: `true` writes `.br` and `.gz` files.
- `strict`: by default the build checks that all pages and endpoints were prerendered or a `fallback` is set; set `false` to skip that check if a page legitimately only exists conditionally.

## Gotchas
- Set `trailingSlash` for your host. If it will not serve `/a.html` for `/a`, use `trailingSlash: 'always'` in the root layout to produce `/a/index.html`.
- `ssr` must not be `false`, or prerendering saves an empty shell page.

## GitHub Pages
If the repo is not `your-username.github.io`, set `paths.base` to the repo name, since the site is served under `/your-repo-name`. Also generate `404.html` as the fallback:
```js
sveltekit({
	adapter: adapter({ fallback: '404.html' }),
	paths: {
		base: process.argv.includes('dev') ? '' : process.env.BASE_PATH
	}
})
```
(with `import process from 'node:process'`). The page's example workflow `.github/workflows/deploy.yml` runs on push to `main` with `permissions: contents: read, pages: read`, a `build_site` job (checkout, setup-node with Node 24 and npm cache, `npm i`, `actions/configure-pages` with `id: pages`, `npm run build` with `BASE_PATH: ${{ steps.pages.outputs.base_path }}`, then `actions/upload-pages-artifact` with `path: 'build/'` and `include-hidden-files: true` to keep `static/.well-known`), and a `deploy` job needing it, with `pages: write`, `id-token: write`, environment `github-pages`, using `actions/deploy-pages`. The artifact `path` must match the adapter's `pages` option.

If you deploy without GitHub Actions (for example pushing the built site to its own repo), add an empty `.nojekyll` file in `static` so Jekyll does not interfere.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `25-build-and-deploy/50-adapter-static.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
