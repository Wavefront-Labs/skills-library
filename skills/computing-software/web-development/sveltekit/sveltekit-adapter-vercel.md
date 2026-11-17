---
id: computing-software.web-development.sveltekit.sveltekit-adapter-vercel
name: sveltekit-adapter-vercel
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, adapter-vercel, vercel, isr, skew-protection]
level: practitioner
status: docs-checked
description: "Deploy SvelteKit to Vercel with adapter-vercel: per-route config, image optimization, ISR with bypassToken, deployment env vars, skew protection and pitfalls."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/90-adapter-vercel.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: deploy to Vercel and tune how routes become functions. `adapter-auto` installs this adapter automatically; add it directly to set options.

## Setup
`npx sv add sveltekit-adapter="adapter:vercel"` or `npm i -D @sveltejs/adapter-vercel`, then `adapter: adapter({ ... })` in `sveltekit()`.

## Deployment configuration
Set options in the adapter call or per file with `export const config` in `+server.js`, `+page(.server).js` and `+layout(.server).js`. Layout config applies to routes beneath it unless overridden.
```js
/** @type {import('@sveltejs/adapter-vercel').Config} */
export const config = {
	split: true
};
```
Options: `runtime` (Node versions such as `'nodejs22.x'`, `'nodejs24.x'`, `'nodejs26.x'`, or `bun1.x`/`bun1.4.x`; defaults to the build's runtime); `regions` (default `["iad1"]`; multiple regions for serverless functions need Enterprise); `split` (own function per route; at adapter level, all routes); `memory` (default 1024 Mb, 128 Mb minimum, up to 3008 Mb in 64Mb steps on Pro/Enterprise); `maxDuration` (default 10 s Hobby, 15 Pro, 900 Enterprise); `isr`. Deploy functions in or near the region of the data they access.

## Image optimization
```js
adapter({
	images: {
		sizes: [640, 828, 1200, 1920, 3840],
		formats: ['image/avif', 'image/webp'],
		minimumCacheTTL: 300,
		domains: ['example-app.vercel.app']
	}
})
```

## Incremental Static Regeneration
Use only where every visitor sees the same content; anything user-specific (session cookies) must happen client-side to avoid leaking data across visits. ISR on a prerendered route has no effect.
```js
import { BYPASS_TOKEN } from '$app/env/private';

export const config = {
	isr: {
		expiration: 60,
		bypassToken: BYPASS_TOKEN,
		allowQuery: ['search']
	}
};
```
- `expiration` (required): seconds before regeneration; `false` means never (then use a bypass token to regenerate on demand).
- `bypassToken`: at least 32 characters (e.g. `crypto.randomUUID()`), baked in at build time, so changing it needs a redeploy. Send cookie `__prerender_bypass=<token>` for draft mode, or a `GET`/`HEAD` with header `x-prerender-revalidate: <token>` to revalidate. Set it as `BYPASS_TOKEN` under Settings > Environment Variables; for local dev run `vercel env pull .env.development.local`.
- `allowQuery`: query parameters that form the cache key; others (e.g. utm codes) are ignored. Default: all ignored.

## Environment variables
Vercel's deployment variables are readable from `$app/env/private` if defined in `src/env.ts`. Pass them to the client via a server load (e.g. `VERCEL_COMMIT_REF`). Since they do not change between build and run, configure them with `static: true` to allow dead-code elimination.

## Skew protection
SvelteKit already hard-reloads on version-skew errors (losing client state); `updated.current` from `$app/state` lets you react earlier. Vercel's skew protection (enable in Advanced project settings) routes requests to the original deployment via a cookie. Caveat: with several app versions open in tabs, older tabs are routed to the newest, falling back to SvelteKit's mechanism.

## Notes
- `waitUntil` and similar come from `@vercel/functions`.
- Files in a root `api` directory take over `/api/*`; implement APIs as SvelteKit routes instead, unless you need a non-JS language (then keep no `/api/*` SvelteKit routes).
- Old projects may default to an older Node version; change it in project settings.
- `node:fs` in serverless functions does not see project files; use `read` from `$app/server` or prerender.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `25-build-and-deploy/90-adapter-vercel.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
