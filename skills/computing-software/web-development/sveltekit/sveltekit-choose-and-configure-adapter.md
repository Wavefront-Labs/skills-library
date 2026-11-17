---
id: computing-software.web-development.sveltekit.sveltekit-choose-and-configure-adapter
name: sveltekit-choose-and-configure-adapter
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, adapters, adapter-auto, vite-config, zero-config]
level: intro
status: docs-checked
description: "Pick a SvelteKit adapter, register it in vite.config.js, and know when adapter-auto is enough versus installing a concrete adapter for options."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/20-adapters.md
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/30-adapter-auto.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: choose the adapter for your deployment target and wire it into the project.

## Install and register
Run `npx sv add sveltekit-adapter` to install an adapter and add it to your config, or install it yourself and set it in `vite.config.js`:

```js
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import adapter from 'svelte-adapter-foo';

export default defineConfig({
	plugins: [
		sveltekit({
			adapter: adapter()
		})
	]
});
```

## Official adapters
- `@sveltejs/adapter-cloudflare`: Cloudflare Workers and Cloudflare Pages
- `@sveltejs/adapter-netlify`: Netlify
- `@sveltejs/adapter-node`: Node servers
- `@sveltejs/adapter-bun`: Bun servers
- `@sveltejs/adapter-static`: static site generation (SSG)
- `@sveltejs/adapter-vercel`: Vercel

Community adapters exist for other platforms.

## adapter-auto (zero config)
`npx sv create` installs `adapter-auto` by default. On deploy it installs and uses the right adapter for supported environments: Cloudflare (Workers and Pages), Netlify, Vercel, `svelte-adapter-azure-swa` for Azure Static Web Apps, `svelte-kit-sst` for AWS via SST, and `@sveltejs/adapter-node` for Google Cloud Run and Render.

- Once you settle on a target, install that adapter into `devDependencies`: it lands in your lockfile and slightly speeds CI installs.
- `adapter-auto` takes no options. To set options such as `{ edge: true }` for `adapter-vercel` or `adapter-netlify`, install the underlying adapter.
- To add zero-config support for another adapter, edit `adapters.js` in the adapter-auto package and open a pull request.

## Platform-specific context
Some adapters expose extra request information (for example Cloudflare's `env` bindings). It is passed to `RequestEvent` as `platform`, usable in hooks and server routes; see each adapter's docs.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `25-build-and-deploy/20-adapters.md`, `25-build-and-deploy/30-adapter-auto.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
