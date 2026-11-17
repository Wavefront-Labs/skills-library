---
id: computing-software.web-development.sveltekit.sveltekit-faq-recipes
name: sveltekit-faq-recipes
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, faq, client-only-code, backend-proxy, vite-middleware, view-transitions, package-compat]
level: practitioner
status: docs-checked
description: "SvelteKit FAQ recipes: client-only libraries, calling an external API through a proxy route, Vite dev middleware, view transitions, package.json data, broken packages and Yarn."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/60-appendix/10-faq.md
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/60-appendix/20-integrations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: quick answers for common "how do I do X" problems.

## Client-only libraries (need `document`/`window`)
- Guard with a `browser` check (imported from `$app/env`):
```js
if (browser) {
	// client-only code here
}
```
- Or load inside `onMount`: `onMount(async () => { const { method } = await import('some-browser-only-library'); method('hello world'); });`
- A side-effect-free library can be imported statically; it is tree-shaken from the server build, where `onMount` becomes a no-op.
- Or pick a component with `{#await promise}` where `promise = browser ? import('./BrowserComponent.svelte') : import('./ServerComponent.svelte')`.

## External backend API
`event.fetch` works but you must handle CORS (preflights add latency; a separate subdomain adds DNS/TLS cost); `handleFetch` helps. Alternatively proxy: rewrite `/api` to the API server in production, use Vite `server.proxy` in dev. Without rewrites, add a route `src/routes/api/[...path]/+server.js`:
```js
export function GET({ params, url }) {
	return fetch(`https://example.com/${params.path + url.search}`);
}
```
You may also need to proxy `POST`/`PATCH` and forward `request.headers`.

## Database
Query from a server route, never in `.svelte` files. Make a `db.js` that connects immediately and exports a singleton; run one-time setup in `hooks.server.js`. `sv add` can set up database integrations (drizzle among the add-ons).

## Middleware
`adapter-node` builds middleware for your own server in production. In dev add a Vite plugin with `configureServer(server) { server.middlewares.use((req, res, next) => { ...; next(); }); }` and put it in `plugins` before `sveltekit(...)`.

## View transitions
Call `document.startViewTransition` in `onNavigate`; return a promise that resolves inside the transition callback, then `await navigation.complete`. Skip when `document.startViewTransition` is missing.

## package.json data
`import pkg from './package.json' with { type: 'json' };` in `vite.config.js`.

## Package fails to import
Usually bad packaging: check with publint.dev. `exports` beats `main`/`module` (adding it blocks deep imports); ESM files end `.mjs` unless `"type": "module"`; `main` is needed without `exports`; ship Svelte components as uncompiled `.svelte` (svelte-package does this). CJS deps are pre-bundled by vite-plugin-svelte. `optimizeDeps` / `ssr` config are short-term workarounds.

## Browsers
Client targets Vite's `build.target` default `'baseline-widely-available'` (with Vite 8: Chrome 111, Edge 111, Firefox 114, Safari 16.4). No polyfills; a lower target only changes syntax transforms (use `@vitejs/plugin-legacy`).

## Preprocessing
`vitePreprocess` defaults `style: true`, `script: false` (PostCSS, SCSS, Less, Stylus, SugarSS). Set `script: true` for pre-Svelte-5 projects or TypeScript features that emit code. `svelte-preprocess` adds Pug, Babel, global styles (not CoffeeScript); install it and the matching library (`sass`, `less`).

## Yarn
Yarn 2 Plug'n'Play is broken for SvelteKit: set `nodeLinker: 'node-modules'` in `.yarnrc.yml` (npm or pnpm is easier). Yarn 3 ESM is experimental; with `enableGlobalCache: true` builds fail, so use `nodeLinker: node-modules` there too.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `60-appendix/10-faq.md`, `60-appendix/20-integrations.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: the claim that SvelteKit 3 renames the env module; the FAQ page imports `browser` from `$app/env`.

Method: documentation only; no commands were run.
