---
id: computing-software.web-development.elysia.deploy-elysia-to-production
name: deploy-elysia-to-production
category: computing-software
field: web-development
product: elysia
tags: [deploy, bun-build, compile-binary, cluster, docker, monorepo, railway]
level: practitioner
status: docs-checked
description: "Ship an Elysia server as a compiled Bun binary or bundled JavaScript, with cluster mode, a distroless Docker image, monorepo builds and Railway PORT."
sources:
  - https://elysiajs.com/patterns/deploy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: produce a small, multi-core production deployment of an Elysia (Bun) app.

## Cluster mode

Elysia is single-threaded by default. Fork one worker per core from an entry file that imports the server:

```ts
// src/index.ts
import cluster from 'node:cluster'
import os from 'node:os'
if (cluster.isPrimary) {
  for (let i = 0; i < os.availableParallelism(); i++) cluster.fork()
} else {
  await import('./server')
}
```

`src/server.ts` just builds the app and calls `.listen(3000)`. Elysia on Bun uses SO_REUSEPORT so workers share the port (Linux only).

## Compile to a binary

```bash
bun build --compile --minify-whitespace --minify-syntax --target bun --outfile server src/index.ts
./server
```

The binary needs no Bun on the host and typically cuts memory 2-3x versus dev. Use `--target bun-linux-x64` (or `bun-linux-arm64`, `bun-windows-x64`, `bun-darwin-arm64`, `bun-linux-x64-musl`, etc.) to pick a platform. On Linux run `chmod +x ./server` if needed.

- Do not use `--minify` when using OpenTelemetry: it reduces function names to a single character and OpenTelemetry relies on function names.
- Gibberish (random Chinese characters) on start means the CPU lacks AVX2; there is no workaround.
- On Windows servers or when compile is impossible, bundle JS instead: `bun build --minify-whitespace --minify-syntax --outfile ./dist/index.js src/index.ts`, then `NODE_ENV=production bun ./dist/index.js`.

## Docker

Use a two-stage build: `FROM oven/bun AS build`, copy `package.json` and `bun.lock`, `bun install`, copy `./src`, set `ENV NODE_ENV=production`, run the compile command, then `FROM gcr.io/distroless/base`, `COPY --from=build /app/server server`, `CMD ["./server"]`, `EXPOSE 3000`.

## Monorepo (Turborepo style)

Put the Dockerfile in `apps/server/Dockerfile`, copy each workspace `package.json` (apps/server and packages/config) before `bun install`, then copy their sources. Build from the monorepo root: `docker build -f apps/server/Dockerfile -t elysia-mono .`.

## Railway

Railway assigns a random port in `PORT`: use `.listen(process.env.PORT ?? 3000)`. Elysia binds `0.0.0.0` automatically.

## Checked

Checked 2026-11-07 against the Elysia documentation source (patterns/deploy.html); each claim, option name and default was compared with the page text. Reworded the OpenTelemetry minify note to what the page says.

Method: documentation only; no commands were run.
