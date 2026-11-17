---
id: computing-software.web-development.hono.hono-request-api
name: hono-request-api
category: computing-software
field: web-development
product: hono
tags: [hono, api, request, query, headers]
level: practitioner
status: docs-checked
description: "Read request data in Hono with c.req: param, query, queries, header, json, text, arrayBuffer, blob, formData, valid, path, url, method, raw and cloneRawRequest."
sources:
  - https://github.com/honojs/website/blob/main/docs/api/request.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HonoRequest (c.req)

`c.req` wraps the standard `Request`.

```ts
const id = c.req.param('id')                       // one param
const { id, commentId } = c.req.param()            // all params
const q = c.req.query('q')                         // one query value
const { q, limit, offset } = c.req.query()         // all
const tags = c.req.queries('tags')                 // /search?tags=A&tags=B -> string[]
const ua = c.req.header('User-Agent')
```

## Body readers
`await c.req.json()`, `.text()`, `.arrayBuffer()`, `.blob()`, `.formData()`, and `.parseBody()` (see the parseBody skill). `c.req.valid('form' | 'json' | 'query' | 'header' | 'cookie' | 'param')` returns validated data.

## Metadata
`c.req.path` (`/about/me`), `c.req.url` (`http://localhost:8787/about/me`), `c.req.method` (`GET`), `c.req.raw` (the raw Request, e.g. `c.req.raw.cf?.hostMetadata` on Workers).

`c.req.routePath` and `c.req.matchedRoutes` are deprecated since v4.8.0; use `routePath()` and `matchedRoutes()` from `hono/route`.

## cloneRawRequest
Clones the raw Request even after validators or HonoRequest methods consumed the body:

```ts
import { cloneRawRequest } from 'hono/request'
app.post('/forward', validator('json', (data) => data), async (c) => {
  const clonedReq = await cloneRawRequest(c.req)
  await clonedReq.json() // does not throw
})
```

## Gotcha
`c.req.header()` with no arguments returns a record whose keys are all LOWERCASE. `headerRecord['X-Foo']` fails; use `c.req.header('X-Foo')` or `headerRecord['x-foo']`.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page api/request.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
