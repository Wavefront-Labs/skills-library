---
id: computing-software.web-development.hono.hono-serve-static
name: hono-serve-static
category: computing-software
field: web-development
product: hono
tags: [hono, static-files, serve-static, bun, deno, nodejs]
level: practitioner
status: docs-checked
description: "Serve static files in Hono on Node, Bun or Deno with serveStatic: root, path, rewriteRequestPath, mimes, onFound, onNotFound, precompressed and security caveats."
sources:
  - https://github.com/honojs/website/blob/main/docs/getting-started/nodejs.md
  - https://github.com/honojs/website/blob/main/docs/getting-started/bun.md
  - https://github.com/honojs/website/blob/main/docs/getting-started/deno.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# serveStatic on Node.js, Bun and Deno

Import per runtime:

```ts
import { serveStatic } from '@hono/node-server/serve-static' // Node
import { serveStatic } from '@hono/bun'                      // Bun
import { serveStatic } from '@hono/deno'                     // Deno (deno add jsr:@hono/deno)
```

```ts
app.use('/static/*', serveStatic({ root: './' }))           // /static/x -> ./static/x
app.use('/favicon.ico', serveStatic({ path: './favicon.ico' }))
app.get('*', serveStatic({ path: './static/fallback.txt' }))
app.use('*', serveStatic({ root: './static' }))              // /hello.txt -> ./static/hello.txt
```

## Options (documented on the Bun and Deno pages)
```ts
serveStatic({
  root: './',
  rewriteRequestPath: (path) => path.replace(/^\/static/, '/statics'),
  mimes: { m3u8: 'application/vnd.apple.mpegurl', ts: 'video/mp2t' },
  onFound: (_path, c) => { c.header('Cache-Control', 'public, immutable, max-age=31536000') },
  onNotFound: (path, c) => { console.log(`${path} is not found, you access ${c.req.path}`) },
  precompressed: true, // serve files like .br or .gz by Accept-Encoding: Brotli, then Zstd, then Gzip; else the original
})
```

## Gotchas
- **Node `root` is relative to `process.cwd()`**, not the source file. For stable paths use `serveStatic({ root: fileURLToPath(new URL('./', import.meta.url)) })` with `import { fileURLToPath } from 'node:url'`.
- **Case sensitivity:** route matching is case-sensitive but Windows and macOS file systems are not (`/ADMIN/secret.txt` reaches `/admin/secret.txt`; Windows also accepts 8.3 names such as `/PROTEC~1`). Path-scoped middleware like `app.use('/admin/*', auth)` does NOT match those spellings. Keep protected files outside the static root, or apply the middleware to every path serveStatic handles.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page getting-started/nodejs.md, bun.md and deno.md. Removed: the invented Verify step and the Cloudflare Workers Static Assets bullet (not on the cited pages).
Method: documentation only; no commands were run.
