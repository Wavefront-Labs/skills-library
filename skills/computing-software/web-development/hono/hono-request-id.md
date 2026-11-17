---
id: computing-software.web-development.hono.hono-request-id
name: hono-request-id
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, observability, request-id]
level: practitioner
status: docs-checked
description: "Give every Hono request a unique ID with requestId, honoring an incoming X-Request-Id and unifying platform IDs through generator."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/request-id.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Request ID

Import: `import { requestId } from 'hono/request-id'` (type: `RequestIdVariables`).

```ts
const app = new Hono()
app.use('*', requestId())
app.get('/', (c) => c.text(`Your request id is ${c.get('requestId')}`))
```

For explicit typing: `new Hono<{ Variables: RequestIdVariables }>()`.

## Incoming IDs
If the request carries the header (default `X-Request-Id`), that value is used instead of a new one:

```ts
const res = await app.request('/', { headers: { 'X-Request-Id': 'your-custom-id' } })
console.log(await res.text()) // your-custom-id
```

Disable this by setting `headerName` to an empty string.

## Options
- `limitLength: number`: max ID length, default `255`.
- `headerName: string`: default `X-Request-Id`.
- `generator: (c) => string`: default `crypto.randomUUID()`.

## Platform IDs
Some platforms (such as AWS Lambda) already generate their own request IDs per request. The middleware is unaware of them and generates a new one, which can confuse logs; use `generator` to capture the platform ID. The page links Cloudflare Ray ID, the Deno request ID and Fastly `req.xid`.

## Gotcha
On Node.js the global `crypto` exists from version 20; on older versions supply a `generator` (the Node.js adapter sets `crypto` globally so it is not needed there).

## Checked
2026-11-04: every claim left was read in the honojs/website docs page middleware/builtin/request-id.md. Removed: the invented Verify step and the claim that Cloudflare, Deno and Fastly generate IDs the same way (the page only links to their docs).
Method: documentation only; no commands were run.
