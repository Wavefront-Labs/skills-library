---
id: computing-software.web-development.hono.hono-bun
name: hono-bun
category: computing-software
field: web-development
product: hono
tags: [hono, bun, runtime, deployment, testing]
level: intro
status: docs-checked
description: "Run Hono on Bun: bun create hono, hot-reload dev script, custom port export, serveStatic from @hono/bun and bun:test testing."
sources:
  - https://github.com/honojs/website/blob/main/docs/getting-started/bun.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hono on Bun

New project: `bun create hono@latest my-app` (template `bun`), `cd my-app`, `bun install`. Existing project: `bun add hono` and add a script:

```json
{ "scripts": { "dev": "bun run --hot src/index.ts" } }
```

```ts
import { Hono } from 'hono'
const app = new Hono()
app.get('/', (c) => c.text('Hello Bun!'))
export default app
```
`bun run dev` serves on `http://localhost:3000`.

## Change the port
Export an object instead of the app:

```ts
export default { port: 3000, fetch: app.fetch }
```

## Static files
`bun add @hono/bun`, then:

```ts
import { serveStatic } from '@hono/bun'
app.use('/static/*', serveStatic({ root: './' }))
app.use('/favicon.ico', serveStatic({ path: './favicon.ico' }))
app.get('*', serveStatic({ path: './static/fallback.txt' }))
```
Options: `rewriteRequestPath`, `mimes`, `onFound`, `onNotFound`, `precompressed`. See the serve-static skill.

## Testing
```ts
import { describe, expect, it } from 'bun:test'
import app from '.'

describe('My first test', () => {
  it('Should return 200 Response', async () => {
    const res = await app.fetch(new Request('http://localhost/'))
    expect(res.status).toBe(200)
  })
})
```
Run `bun test index.test.ts`.

## Gotchas
- With an existing project the `bun run dev` script expects the app at `src/index.ts`.
- Route matching is case-sensitive but the file system may not be (Windows, macOS, 8.3 short names). `app.use('/admin/*', auth)` does not protect files under a static root; keep protected files outside the served directory.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/getting-started/bun.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); "same on Deno and Node" (not on the Bun page) and the JSX rename advice (belongs to the JSX page).

Method: documentation only; no commands were run.
