---
id: computing-software.web-development.hono.hono-adapter-helper
name: hono-adapter-helper
category: computing-software
field: web-development
product: hono
tags: [hono, helper, runtime, environment-variables]
level: practitioner
status: docs-checked
description: "Read environment variables portably with env(c) and detect the runtime with getRuntimeKey in Hono across Workers, Node, Bun, Deno and others."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/adapter.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Adapter helper

Import: `import { env, getRuntimeKey } from 'hono/adapter'`.

## env()
Retrieves environment variables across runtimes (not only Cloudflare bindings). What `env(c)` returns can differ per runtime.

```ts
app.get('/env', (c) => {
  // NAME is process.env.NAME on Node.js or Bun
  // NAME is the value in wrangler.toml on Cloudflare
  const { NAME } = env<{ NAME: string }>(c)
  return c.text(NAME)
})
```

Sources: Cloudflare Workers (`wrangler.toml`, `wrangler.jsonc`), Deno (`Deno.env`, `.env` file), Bun (`Bun.env`, `process.env`), Node.js (`process.env`), Vercel, AWS Lambda.

Force a runtime by passing its key as the second argument: `env<{ NAME: string }>(c, 'workerd')`.

## getRuntimeKey()
```ts
if (getRuntimeKey() === 'workerd') return c.text('You are on Cloudflare')
else if (getRuntimeKey() === 'bun') return c.text('You are on Bun')
```
Keys: `workerd` (Cloudflare Workers), `deno`, `bun`, `node`, `edge-light` (Vercel Edge Functions), `fastly` (Fastly Compute), `other` (unknown runtimes).

## Gotchas
- Lambda@Edge does not support Lambda environment variables; use the Lambda@Edge event instead.
- On Fastly Compute use the ConfigStore for user-defined data; on Netlify use Netlify Contexts.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/helpers/adapter.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
