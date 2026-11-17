---
id: computing-software.web-development.sveltekit.sveltekit-adapter-bun
name: sveltekit-adapter-bun
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, adapter-bun, bun, compiled-executable, bun-serve]
level: practitioner
status: docs-checked
description: "Deploy SvelteKit to a Bun server with adapter-bun: build with --bun, serverOptions, compiled executables, env vars, proxy headers and shutdown."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/45-adapter-bun.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: build and run a SvelteKit app on Bun. Bun 1.4 or newer is required. The server uses `Bun.serve`.

## Setup
`npx sv add sveltekit-adapter="adapter:bun"` or `npm i -D @sveltejs/adapter-bun`, then `adapter: adapter()` inside `sveltekit({...})` in `vite.config.js`.

The adapter calls Bun's build API, so the build itself must run in Bun; `--bun` overrides Vite's Node.js shebang:
```sh
bun run --bun build
bun ./build
```
To run you need the output, `package.json` and production dependencies: copy `package.json` and `bun.lock`, then `bun install --production --frozen-lockfile`. Dev dependencies are bundled; `dependencies` vs `devDependencies` controls externalising.

Client assets and prerendered output are served before a request reaches SvelteKit, for `GET` and `HEAD` only (other methods continue to SvelteKit); each has a build-time ETag (conditional requests get an empty `304`); files under `immutable` get `Cache-Control: public,max-age=31536000,immutable`.

## Options
```js
adapter({
	out: 'build',
	envPrefix: '',
	serverOptions: { idleTimeout: 30 }
})
```
- `precompress: true` writes `.br`/`.gz` variants (ignored when `buildOptions.compile` is set).
- `envPrefix` prefixes every variable below (`MY_APP_HOST=... bun ./build`); with a prefix, startup fails on unknown variables with that prefix.
- `serverOptions` (JSON-serializable `Bun.serve` defaults): `hostname`, `port`, `unix`, `reusePort`, `ipv6Only`, `idleTimeout`, `maxRequestBodySize`, `development`. Env vars win; a `unix` socket wins over TCP options. `websocket`, `error`, TLS, HTTP/3 and HTTP/1 settings are not exposed.

## Compiled executable
`buildOptions` (`sourcemap`, `minify`, `bytecode`, `banner`, `footer`, `drop`, `features`, `optimizeImports`, `external`, `compile`) only applies when `compile` is set. `compile: true` writes `<out>/server`, embedding code, assets and the Bun runtime; run `./build/server`. Source maps default to `external`. For a name or cross-compile:
```js
adapter({
	out: 'dist',
	buildOptions: {
		compile: { outfile: 'application', target: 'bun-linux-x64' },
		minify: true,
		bytecode: true,
		sourcemap: 'linked'
	}
});
```
Result: `dist/application`. Dependencies are bundled; to load one from `node_modules` instead, list it in `external` and set `compile: { autoloadPackageJson: true }` (needed for packages like `jsdom`).

## Environment variables
Bun loads `.env` automatically.
- `HOST`, `PORT` (default 3000), `SOCKET_PATH` (Unix socket; TCP options ignored), `REUSE_PORT`, `IPV6_ONLY` (booleans: `1/true/yes/on`, `0/false/no/off`).
- `BODY_SIZE_LIMIT` (default `512K`, `K/M/G` suffix, `Infinity` disables).
- `CONNECTION_IDLE_TIMEOUT`: integer 0-255 seconds, 0 disables. Disabled for `text/event-stream` responses, which also get `X-Accel-Buffering: no`. Not named `IDLE_TIMEOUT`, which means something different in adapter-node.
- `DEVELOPMENT`: Bun dev error pages, default `false`.
- Origin: `paths.origin` or `ORIGIN` wins. Otherwise host comes from `Host` and the scheme is assumed `https`; set `paths.origin`, `ORIGIN` or `PROTOCOL_HEADER` if serving plain HTTP. Behind a trusted proxy: `PROTOCOL_HEADER=x-forwarded-proto HOST_HEADER=x-forwarded-host PORT_HEADER=x-forwarded-port`. Invalid values give `400 Bad Request`; empty headers are ignored.
- `ADDRESS_HEADER` for `getClientAddress()`; with `x-forwarded-for` set `XFF_DEPTH` (integer >= 1, default 1, read from the right). It throws if the header is missing or has too few addresses.

## Platform and shutdown
`platform.server` is the Bun server (`id`, `pendingRequests`, `pendingWebSockets`). On `SIGINT`/`SIGTERM` it calls `server.stop()`, waits for pending requests, emits `sveltekit:shutdown` with the signal name, and force-closes connections after `SHUTDOWN_TIMEOUT` seconds (non-negative integer, default 30). A second signal exits with status 1.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `25-build-and-deploy/45-adapter-bun.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: the unconfirmed 'native Bun routes' wording and the claim that filenames containing a literal `*` are rejected; the asset-serving sentence now follows the page.

Method: documentation only; no commands were run.
