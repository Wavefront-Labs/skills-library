---
id: computing-software.web-development.sveltekit.sveltekit-adapter-cloudflare-workers-sites
name: sveltekit-adapter-cloudflare-workers-sites
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, adapter-cloudflare-workers, workers-sites, wrangler, migration]
level: practitioner
status: docs-checked
description: "Use or migrate off the deprecated adapter-cloudflare-workers (Workers Sites): wrangler.jsonc, platform.env bindings, and the switch to adapter-cloudflare."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/70-adapter-cloudflare-workers.md
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/60-adapter-cloudflare.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: maintain an app on `adapter-cloudflare-workers` (Cloudflare Workers Sites), or move it to `adapter-cloudflare`. The adapter is deprecated in favour of `adapter-cloudflare` with Workers Static Assets, because Workers Sites will be deprecated.

## Migrate (recommended)
1. Replace `@sveltejs/adapter-cloudflare-workers` with `@sveltejs/adapter-cloudflare` in `vite.config.js`: `adapter: adapter()`.
2. In the Wrangler config remove all `site` settings and add `assets.directory` and `assets.binding`. `wrangler.toml`:
```toml
assets.directory = ".cloudflare/public"
assets.binding = "ASSETS" # Exclude this if you don't have a `main` key configured.
```
`wrangler.jsonc`:
```jsonc
{
	"assets": {
		"directory": ".cloudflare/public",
		"binding": "ASSETS" // Exclude this if you don't have a `main` key configured.
	}
}
```
Bindings then come from `cloudflare:workers` instead of `platform.env` (see the adapter-cloudflare skill).

## Staying on adapter-cloudflare-workers
Install `npm i -D @sveltejs/adapter-cloudflare-workers` and set `adapter: adapter({})` in `sveltekit()`. Options: `config` (Wrangler file path, if not `wrangler.jsonc`, `wrangler.json` or `wrangler.toml`) and `platformProxy` (emulated `platform.env` bindings).

Wrangler config in the project root:
```jsonc
{
	"name": "<your-service-name>",
	"account_id": "<your-account-id>",
	"main": "./.cloudflare/worker.js",
	"site": {
		"bucket": "./.cloudflare/public"
	},
	"build": {
		"command": "npm run build"
	},
	"compatibility_date": "2021-11-12"
}
```
The account id comes from `wrangler whoami` or the end of your Cloudflare dashboard URL. Add the `main` and `site.bucket` directories (`.cloudflare`) and `.wrangler` to `.gitignore`. Then:
```sh
npm i -D wrangler
wrangler login
wrangler deploy
```

## Bindings
`env` (KV/DO namespaces etc.) arrives on `platform` along with `ctx`, `caches` and `cf`, usable in hooks and endpoints: `platform?.env.YOUR_DURABLE_OBJECT_NAMESPACE.idFromName('x')`. For types, install `@cloudflare/workers-types` and declare `env?: { YOUR_KV_NAMESPACE: KVNamespace; YOUR_DURABLE_OBJECT_NAMESPACE: DurableObjectNamespace }` on `App.Platform` in `src/app.d.ts`. Prefer `$app/env/*` for environment variables.

## Local and troubleshooting
Dev and preview emulate `platform.env` from the Wrangler config; test the build with Wrangler 4 via `wrangler dev`. Enable Node.js compatibility with `"compatibility_flags": ["nodejs_compat"]`. The server is one bundled file and Wrangler fails if it exceeds the worker size limits (import big libraries client-side only). `fs` is unavailable; prerender those routes.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `25-build-and-deploy/70-adapter-cloudflare-workers.md`, `25-build-and-deploy/60-adapter-cloudflare.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
