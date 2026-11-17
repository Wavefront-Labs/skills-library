---
id: computing-software.web-development.sveltekit.sveltekit-spa-mode
name: sveltekit-spa-mode
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, spa, single-page-app, fallback-page, ssr-false]
level: practitioner
status: docs-checked
description: "Turn a SvelteKit app into a client-rendered SPA with ssr=false and an adapter-static fallback page, prerender selected pages, and route Apache to the fallback."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/55-single-page-apps.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: serve a fully client-rendered SPA by giving SvelteKit a fallback page for any URL not served otherwise.

## Know the cost first
SPA mode adds network round trips (blank HTML, then JavaScript, then data), delays startup especially on mobile, tends to hurt SEO and Core Web Vitals, and breaks the app when JavaScript fails or is disabled. Prerender as many pages as possible (especially the homepage). If you can prerender everything, use plain static site generation instead; otherwise consider an adapter that supports SSR.

## Steps
1. Disable SSR for pages you will not prerender; for everything by default:
```js
// src/routes/+layout.js
export const ssr = false;
```
2. With no server logic (`+page.server.js`, `+layout.server.js`, `+server.js`), use `adapter-static` with a `fallback`:
```js
sveltekit({
	adapter: adapter({
		fallback: '200.html' // may differ from host to host
	})
})
```
The fallback is an HTML page built from your template (e.g. `app.html`) that loads the app and navigates to the right route. Surge, for example, serves a `200.html` for requests that match no asset or prerendered page. Other hosts differ, so check your platform's docs. Avoid `index.html`: it can conflict with prerendering.

## Prerender selected pages
Re-enable `ssr` alongside `prerender` for just those routes:
```js
// src/routes/my-prerendered-page/+page.js
export const prerender = true;
export const ssr = true;
```
This needs no Node server; SSR happens only at build time to emit an `.html` file for any static host.

## Apache
Add `static/.htaccess`:
```
<IfModule mod_rewrite.c>
	RewriteEngine On
	RewriteBase /
	RewriteRule ^200\.html$ - [L]
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteRule . /200.html [L]
</IfModule>
```

## Gotcha
The fallback page always uses absolute asset paths (starting with `/`), regardless of `paths.relative`, because it answers requests for arbitrary paths.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 25-build-and-deploy/55-single-page-apps.md in full: ssr false, adapter-static fallback, hosting notes, prerendering a subset. No claims trimmed.
