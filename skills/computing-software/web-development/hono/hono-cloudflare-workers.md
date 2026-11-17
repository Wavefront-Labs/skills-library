---
id: computing-software.web-development.hono.hono-cloudflare-workers
name: hono-cloudflare-workers
category: computing-software
field: web-development
product: hono
tags: [hono, cloudflare-workers, wrangler, bindings, deployment]
level: practitioner
status: docs-checked
description: "Build and deploy Hono on Cloudflare Workers: create-hono, wrangler, typed Bindings, secrets in middleware, .dev.vars, scheduled handlers and CI deploy."
sources:
  - https://github.com/honojs/website/blob/main/docs/getting-started/cloudflare-workers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hono on Cloudflare Workers

```sh
npm create hono@latest my-app   # choose cloudflare-workers
cd my-app && npm i
npm run dev      # http://localhost:8787
npm run deploy
```

```ts
import { Hono } from 'hono'
const app = new Hono()
app.get('/', (c) => c.text('Hello Cloudflare Workers!'))
export default app
```
Change the port in `wrangler.toml` / `wrangler.json` / `wrangler.jsonc` or with Wrangler CLI options. In `package.json` change `$npm_execpath` to your package manager.

## Other handlers (scheduled etc.)
```ts
export default { fetch: app.fetch, scheduled: async (batch, env) => {} }
```

## Static assets
In `wrangler.jsonc`: `"assets": { "directory": "public" }`; `./public/static/hello.txt` is served at `/static/hello.txt`.

## Bindings and types
```ts
type Bindings = { MY_BUCKET: R2Bucket; USERNAME: string; PASSWORD: string }
const app = new Hono<{ Bindings: Bindings }>()
app.put('/upload/:key', async (c) => {
  await c.env.MY_BUCKET.put(c.req.param('key'), c.req.body)
  return c.text('ok')
})
```
Generate types: `wrangler types --env-interface CloudflareBindings` then `new Hono<{ Bindings: CloudflareBindings }>()`. The `--env-interface` flag avoids a clash with Hono's built-in `Env`. Install `@cloudflare/workers-types` for runtime types.

## Secrets in middleware options
```ts
app.use('/auth/*', async (c, next) => {
  const auth = basicAuth({ username: c.env.USERNAME, password: c.env.PASSWORD })
  return auth(c, next)
})
```

## Local env
Put `SECRET_KEY=value` lines in `.dev.vars` or `.env`, read via `c.env.SECRET_KEY`.

## CI
GitHub Actions with `cloudflare/wrangler-action@v3`, `apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}` (token from the Edit Cloudflare Workers template); add `"main": "src/index.ts", "minify": true` to `wrangler.jsonc`.

## Gotchas
- `process.env` is NOT available by default; use `c.env` (or enable `nodejs_compat_populate_process_env`).
- Set production secrets in the Cloudflare project, not just locally.
- Test with `@cloudflare/vitest-pool-workers`, or `app.request('http://localhost/')`.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/getting-started/cloudflare-workers.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
