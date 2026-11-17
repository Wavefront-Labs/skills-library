---
id: computing-software.web-development.elysia.elysia-cloudflare-workers-adapter
name: elysia-cloudflare-workers-adapter
category: computing-software
field: web-development
product: elysia
tags: [integrations-deploy, cloudflare, workers, adapter, wrangler]
level: advanced
status: docs-checked
description: "Deploy Elysia to Cloudflare Workers with the experimental CloudflareAdapter, compile(), a recent compatibility_date, static assets and bindings."
sources:
  - https://elysiajs.com/integrations/cloudflare-worker.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run Elysia on Cloudflare Workers (the docs mark this EXPERIMENTAL).

1. Scaffold with Wrangler: `wrangler init elysia-on-cloudflare`.
2. Export the app with the adapter and call `.compile()`:

```ts
import { Elysia } from 'elysia'
import { CloudflareAdapter } from 'elysia/adapter/cloudflare-worker'

export default new Elysia({ adapter: CloudflareAdapter })
    .get('/', () => 'Hello Cloudflare Worker!')
    .compile()          // required on Cloudflare Worker
```

3. Set `compatibility_date` to at least `2025-06-01` in wrangler.jsonc/wrangler.toml (with `main` pointing at `src/index.ts`).
4. Run `wrangler dev`; the dev server is at `http://localhost:8787`. No `nodejs_compat` flag is needed.
5. pnpm: `pnpm add @sinclair/typebox openapi-types`.

Static files: the Static plugin and `file()` need `fs` and do not work. Use Cloudflare assets: add `"assets": { "directory": "public" }` (toml: `assets = { directory = "public" }`). `public/static/mika.webp` is then served at `/static/mika.webp`.

Bindings: `import { env } from 'cloudflare:workers'` and use `await env.KV.get('my-key')` inside handlers.

AoT: since Elysia 1.4.7 Ahead-of-Time compilation works, so drop the old `aot: false` flag. `aot: false` remains available but the docs recommend AoT for performance and accurate plugin encapsulation.

Limitations from the docs:
- OpenAPI Type Gen does not work (no `fs`).
- You cannot define a Response before server start or use a plugin that does, so inline values fail: `.get('/', 'Hello Elysia')` throws. Use a function: `.get('/', () => 'Hello Elysia')`.

Gotcha: the docs say `.compile()` is required before exporting the app.

## Checked

Checked 2026-11-07 against the Elysia documentation source (integrations/cloudflare-worker.html); each claim, option name and default was compared with the page text. Removed the invented Verify step.

Method: documentation only; no commands were run.
