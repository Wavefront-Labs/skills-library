---
id: computing-software.web-development.sveltekit.sveltekit-adapter-cloudflare
name: sveltekit-adapter-cloudflare
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, adapter-cloudflare, cloudflare, wrangler, cloudflare-pages]
level: practitioner
status: docs-checked
description: "Deploy SvelteKit to Cloudflare Workers or Pages with adapter-cloudflare: options, wrangler.jsonc, bindings via cloudflare:workers, local testing and limits."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/60-adapter-cloudflare.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: deploy to Cloudflare Workers (Static Assets) or Cloudflare Pages. `adapter-auto` installs this adapter already; install it directly to get `cloudflare:workers` emulated in dev, automatic type declarations and Cloudflare options. (`adapter-cloudflare-workers` is deprecated; `adapter-static` only makes client-side assets.)

## Setup
`npx sv add sveltekit-adapter="adapter:cloudflare"` or `npm i -D @sveltejs/adapter-cloudflare`. Options (defaults shown):
```js
adapter({
	config: undefined,
	platformProxy: { configPath: undefined, environment: undefined, persist: undefined },
	fallback: 'plaintext',
	routes: { include: ['/*'], exclude: ['<all>'] }
})
```
- `config`: path to a Wrangler config if not `wrangler.jsonc`, `wrangler.json` or `wrangler.toml`.
- `platformProxy`: preferences for emulated local `env` bindings (Wrangler `getPlatformProxy` options).
- `fallback`: `plaintext` 404.html or `spa` rendered fallback for non-matching asset requests. On Workers the default is a null-body 404 unless `assets.not_found_handling` is `"404-page"` (serves this page) or `"single-page-application"` (adapter renders an SPA `index.html` regardless). On Pages it is served only when a request matching `routes.exclude` fails to match an asset. Use `spa` if you hand-trim `routes.exclude` to stay under the route limit.
- `routes` (Pages only) customises `_routes.json`: `include` routes invoke a function; `exclude` routes do not (faster and cheaper). Special values: `<build>`, `<files>`, `<redirects>`, `<prerendered>`, `<all>` (default). Max 100 include plus exclude rules combined; e.g. use `'/articles/*'` instead of a long generated list.

## Workers
Needs a Wrangler config in the project root:
```jsonc
{
	"name": "<any-name-you-want>",
	"main": ".svelte-kit/cloudflare/_worker.js",
	"compatibility_flags": ["nodejs_als"],
	"compatibility_date": "<YYYY-MM-DD>",
	"assets": {
		"binding": "ASSETS",
		"directory": ".svelte-kit/cloudflare"
	}
}
```
Deploy with `npx wrangler deploy` or the Cloudflare Git integration.

## Pages
Git integration build settings: framework preset SvelteKit; build command `npm run build` or `vite build`; output directory `.svelte-kit/cloudflare`. A `/functions` directory is not deployed; write server endpoints instead (compiled into a single `_worker.js`).

## Bindings
Import `env` from `cloudflare:workers` in server code (prefer SvelteKit's `$app/env/*` for plain env vars):
```js
import { env } from 'cloudflare:workers';

export async function POST() {
	const x = env.YOUR_DURABLE_OBJECT_NAMESPACE.idFromName('x');
}
```
For types, install `wrangler` and run `wrangler types`. In dev and preview, local bindings come from your Wrangler config. Durable Objects and Workflows (custom exported classes) are not supported locally. Test the build with Wrangler 4: `wrangler dev .svelte-kit/cloudflare/_worker.js` (Workers) or `wrangler pages dev .svelte-kit/cloudflare` (Pages).

## Headers and redirects
`_headers` and `_redirects` in the project root apply to static assets only. For dynamic responses use server endpoints or the `handle` hook.

## Troubleshooting
- Node.js compat: add `"compatibility_flags": ["nodejs_compat"]` to the Wrangler config.
- Worker size limit: Wrangler fails to publish an oversized single-file worker; import large libraries only on the client.
- No `fs`: use `read` from `$app/server` (fetches from the deployed public assets), or prerender the route.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `25-build-and-deploy/60-adapter-cloudflare.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
