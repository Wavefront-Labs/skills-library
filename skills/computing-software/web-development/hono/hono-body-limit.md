---
id: computing-software.web-development.hono.hono-body-limit
name: hono-body-limit
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, upload, body-limit, bun]
level: practitioner
status: docs-checked
description: "Cap request body size in Hono with bodyLimit, a custom onError, and the extra maxRequestBodySize setting needed on Bun for large bodies."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/body-limit.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Limit request body size

Import: `import { bodyLimit } from 'hono/body-limit'`.

The middleware checks the `Content-Length` header if present. If absent it reads the body as a stream and runs the error handler once the size is exceeded.

```ts
app.post(
  '/upload',
  bodyLimit({
    maxSize: 50 * 1024, // 50kb
    onError: (c) => c.text('overflow :(', 413),
  }),
  async (c) => {
    const body = await c.req.parseBody()
    if (body['file'] instanceof File) {
      console.log(`Got file sized: ${body['file'].size}`)
    }
    return c.text('pass :)')
  }
)
```

## Options
- `maxSize: number` (required): bytes.
- `onError`: handler invoked when the limit is exceeded.

## Bun gotcha
`Bun.serve` has its own default request body limit (128MiB at the time of writing). If you set Hono's `maxSize` higher, requests still fail with 413 and `onError` is NOT called, because Bun terminates the connection before Hono sees it. Raise Bun's limit too:

```ts
export default {
  port: process.env['PORT'] || 3000,
  fetch: app.fetch,
  maxRequestBodySize: 1024 * 1024 * 200,
}
```

or `Bun.serve({ fetch(req, server) { return app.fetch(req, { ip: server.requestIP(req) }) }, maxRequestBodySize: 1024 * 1024 * 200 })`.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/body-limit.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
