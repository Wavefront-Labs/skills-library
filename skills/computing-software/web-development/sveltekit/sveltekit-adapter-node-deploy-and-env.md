---
id: computing-software.web-development.sveltekit.sveltekit-adapter-node-deploy-and-env
name: sveltekit-adapter-node-deploy-and-env
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, adapter-node, node-env, environment-variables, reverse-proxy]
level: practitioner
status: docs-checked
description: "Build and run a SvelteKit app with adapter-node, and configure PORT, ORIGIN, proxy headers, client address, body size limit and envPrefix."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/40-adapter-node.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: deploy a standalone Node server from `adapter-node` and configure it through environment variables.

## Set up and run
```js
import adapter from '@sveltejs/adapter-node';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit({ adapter: adapter() })]
});
```
Install with `npx sv add sveltekit-adapter="adapter:node"` or `npm i -D @sveltejs/adapter-node`. Run `npm run build`; output goes to `build` by default. To run you need the output directory, `package.json` and production dependencies (copy `package.json` and `package-lock.json`, then `npm ci --omit dev`; skip if the app has no dependencies). Start with `node build`.

Dev dependencies are bundled with Rolldown. Put a package in `dependencies` to externalise it, or `devDependencies` to bundle it.

## Adapter options (defaults)
`out: 'build'`, `precompress: true` (writes `.br` and `.gz`; the server negotiates `Accept-Encoding`, brotli preferred), `envPrefix: ''`. With `envPrefix: 'MY_CUSTOM_'` you set `MY_CUSTOM_HOST=127.0.0.1 MY_CUSTOM_PORT=4000 node build`.

## Environment variables
- `.env` files load in dev and preview only. In production use `node --env-file=.env build`.
- `PORT` / `HOST`: default `0.0.0.0:3000`. `SOCKET_PATH` overrides both (`SOCKET_PATH=/tmp/socket node build`).
- Origin: set `paths.origin` in the `sveltekit()` config, or `ORIGIN=https://my.site` at runtime. Otherwise the origin is derived from the `host` header plus `PROTOCOL_HEADER`/`HOST_HEADER`/`PORT_HEADER`, e.g. `PROTOCOL_HEADER=x-forwarded-proto HOST_HEADER=x-forwarded-host node build`. Only set these behind a trusted proxy, or clients can spoof them. If the URL is wrong, form actions can fail with "Cross-site POST form submissions are forbidden".
- `ADDRESS_HEADER` (e.g. `True-Client-IP`) tells `event.getClientAddress()` where to read the client IP. For `X-Forwarded-For`, set `XFF_DEPTH` to the number of trusted proxies; the adapter reads from the right, so a spoofed left-most entry is not trusted.
- `BODY_SIZE_LIMIT`: bytes, or with a `K`/`M`/`G` suffix; default 512kb; `Infinity` disables it (0 in older adapter versions).
- `KEEP_ALIVE_TIMEOUT`, `HEADERS_TIMEOUT`: seconds for Node's `keepAliveTimeout` and `headersTimeout`.
- `SHUTDOWN_TIMEOUT` (default 30) and `IDLE_TIMEOUT`: see the lifecycle skill.

## Compression
Behind a reverse proxy, compress there (Node is single-threaded). In a custom server use `@polka/compression`, not `compression`, which does not support streaming and may cause errors.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `25-build-and-deploy/40-adapter-node.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
