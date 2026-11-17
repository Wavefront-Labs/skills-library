---
id: computing-software.web-development.hono.hono-proxy-helper
name: hono-proxy-helper
category: computing-software
field: web-development
product: hono
tags: [hono, helper, proxy, reverse-proxy, security]
level: advanced
status: docs-checked
description: "Build a reverse proxy in Hono with the proxy helper: forwarding headers, stripping credentials, customFetch and strictConnectionProcessing."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/proxy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Proxy helper

Import: `import { proxy } from 'hono/proxy'`.

`proxy()` wraps `fetch()` with the same parameters and return value (plus proxy options). It replaces `Accept-Encoding` with one the runtime can handle, removes unnecessary response headers, and returns a `Response` you can return directly.

```ts
app.get('/proxy/:path', (c) => proxy(`http://${originServer}/${c.req.param('path')}`))
```

With custom headers:

```ts
app.get('/proxy/:path', async (c) => {
  const res = await proxy(`http://${originServer}/${c.req.param('path')}`, {
    headers: {
      ...c.req.header(), // only when forwarding everything, including credentials, is needed
      'X-Forwarded-For': '127.0.0.1',
      'X-Forwarded-Host': c.req.header('host'),
      Authorization: undefined, // do not propagate the Authorization header
    },
  })
  res.headers.delete('Set-Cookie')
  return res
})
```

You can pass `c.req` too: `proxy(url, { ...c.req, headers: {...} })`.

## Options (ProxyRequestInit)
`raw?: Request`, `customFetch?: (request: Request) => Promise<Response>` (override global fetch), `strictConnectionProcessing?: boolean`, plus normal `RequestInit` fields. `headers` values may be `undefined` to remove a header.

## Hop-by-hop gotcha
By default `proxy()` ignores the `Connection` header to prevent Hop-by-Hop Header Injection. Enable `strictConnectionProcessing: true` (RFC 9110) only in trusted environments:

```ts
proxy(`http://${internalServer}/${c.req.param('path')}`, { ...c.req, strictConnectionProcessing: true })
```

## Checked
2026-11-04: every claim left was read in the honojs/website docs page helpers/proxy.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
