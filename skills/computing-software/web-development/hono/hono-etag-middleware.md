---
id: computing-software.web-development.hono.hono-etag-middleware
name: hono-etag-middleware
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, etag, http-caching]
level: practitioner
status: docs-checked
description: "Add ETag headers and 304 responses to Hono routes with the etag middleware, weak validation, retainedHeaders and custom digest."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/etag.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ETag middleware

Import: `import { etag, RETAINED_304_HEADERS } from 'hono/etag'`.

```ts
app.use('/etag/*', etag())
app.get('/etag/abc', (c) => c.text('Hono is cool'))
```

## Retained headers
A 304 response must include the headers a 200 would have had. Defaults: Cache-Control, Content-Location, Date, ETag, Expires, Vary. Add more with `retainedHeaders`, spreading the exported default array:

```ts
app.use(
  '/etag/*',
  etag({ retainedHeaders: ['x-message', ...RETAINED_304_HEADERS] })
)
```

## Options
- `weak: boolean`: weak validation; adds `W/` prefix to the value. Default `false`.
- `retainedHeaders: string[]`: headers kept in the 304.
- `generateDigest: (body: Uint8Array) => ArrayBuffer | Promise<ArrayBuffer>`: custom hash; the default is `SHA-1`.

## Gotcha
The 304 response keeps only the retained headers. The defaults (Cache-Control, Content-Location, Date, ETag, Expires, Vary) are exported as the `RETAINED_304_HEADERS` array, which the docs spread together with any extra header you add. `generateDigest` receives the response body as a `Uint8Array` and must return an `ArrayBuffer` or a Promise of one; the default hash is `SHA-1`. Use `weak: true` for weak validation (a `W/` prefix is added to the ETag value). The middleware here is mounted with a path pattern: `app.use('/etag/*', etag())`.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/etag.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
