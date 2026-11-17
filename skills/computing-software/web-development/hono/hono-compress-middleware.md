---
id: computing-software.web-development.hono.hono-compress-middleware
name: hono-compress-middleware
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, compression, gzip]
level: practitioner
status: docs-checked
description: "Compress Hono responses by Accept-Encoding with the compress middleware, tuning encoding, threshold and contentTypeFilter."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/compress.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compress middleware

Import: `import { compress } from 'hono/compress'`.

```ts
const app = new Hono()
app.use(compress())
```

It compresses the response body according to the `Accept-Encoding` request header.

## Options
- `encoding: 'gzip' | 'deflate'`: restrict the scheme. If unset both are allowed and `gzip` is preferred when the client offers both.
- `threshold: number`: minimum size in bytes to compress, default 1024.
- `contentTypeFilter: RegExp | (contentType: string) => boolean`: decides by `Content-Type`. A built-in compressible list is the default.

```ts
// Compress only JSON responses
app.use(compress({ contentTypeFilter: /^application\/json/ }))
```

Extend the default list with the exported regex:

```ts
import { compress, COMPRESSIBLE_CONTENT_TYPE_REGEX } from 'hono/compress'

app.use(
  compress({
    contentTypeFilter: (type) =>
      COMPRESSIBLE_CONTENT_TYPE_REGEX.test(type) ||
      type === 'application/x-myformat',
  })
)
```

## Gotcha
On Cloudflare Workers and Deno Deploy the response body is compressed automatically, so do not add this middleware there.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/compress.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
