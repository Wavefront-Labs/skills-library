---
id: computing-software.web-development.hono.hono-deno
name: hono-deno
category: computing-software
field: web-development
product: hono
tags: [hono, deno, runtime, jsr, deployment]
level: intro
status: docs-checked
description: "Run Hono on Deno: deno init template, Deno.serve, port option, @hono/deno serveStatic, Deno.test and npm versus JSR import maps."
sources:
  - https://github.com/honojs/website/blob/main/docs/getting-started/deno.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hono on Deno

```sh
deno init --npm hono --template=deno my-app
cd my-app          # no explicit Hono install needed
deno task start    # http://localhost:8000
```

```ts
import { Hono } from 'hono'
const app = new Hono()
app.get('/', (c) => c.text('Hello Deno!'))
Deno.serve(app.fetch)
```
Port: `Deno.serve({ port: 8787 }, app.fetch)`.

## Static files
`deno add jsr:@hono/deno`, then `import { serveStatic } from '@hono/deno'` and use `serveStatic({ root: './' })` or `serveStatic({ path: './favicon.ico' })`.

## Testing
```ts
import { assertEquals } from '@std/assert'
Deno.test('Hello World', async () => {
  const app = new Hono()
  app.get('/', (c) => c.text('Please test me'))
  const res = await app.request('http://localhost/')
  assertEquals(res.status, 200)
})
```
`deno add jsr:@std/assert`, then `deno test hello.ts`.

## npm vs JSR imports
Hono is on npm (`npm:hono`) and JSR (`jsr:@hono/hono`). In `deno.json`:

```json
{ "imports": { "hono": "npm:hono", "hono/": "npm:/hono/" } }
```
Use the directory-style `hono/` mapping to import middleware.

## Gotcha: same registry as middleware
Use Hono from the SAME registry as third-party middleware for correct type inference:

```json
{ "imports": { "hono": "npm:hono", "zod": "npm:zod", "@hono/zod-validator": "npm:@hono/zod-validator" } }
```
For JSR middleware use `"hono": "jsr:@hono/hono"` and `"@hono/zod-validator": "jsr:@hono/zod-validator"`.

Deno Deploy also runs Hono (see the Deno Deploy manual).

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/getting-started/deno.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
