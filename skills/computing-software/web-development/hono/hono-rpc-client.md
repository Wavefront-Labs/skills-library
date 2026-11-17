---
id: computing-software.web-development.hono.hono-rpc-client
name: hono-rpc-client
category: computing-software
field: web-development
product: hono
tags: [hono, rpc, client, typescript, hc]
level: practitioner
status: docs-checked
description: "Share Hono API types with a typed client: export AppType, call hc, send params, query, headers and cookies, and read typed status-code responses."
sources:
  - https://github.com/honojs/website/blob/main/docs/guides/rpc.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hono RPC client (hc)

Export the type of the app (or the route you want exposed) on the server; the client infers inputs from validators and outputs from `c.json()`.

> In a monorepo set `"strict": true` in `compilerOptions` of BOTH the client and server tsconfig.json, or the types will not work.

## Server
```ts
const route = app.post(
  '/posts',
  zValidator('form', z.object({ title: z.string(), body: z.string() })),
  (c) => c.json({ ok: true, message: 'Created!' }, 201)
)
export type AppType = typeof route
```
Standard Schema validators (for example Valibot) work too.

## Client
```ts
import type { AppType } from '.'
import { hc } from 'hono/client'

const client = hc<AppType>('http://localhost:8787/')
const res = await client.posts.$post({ form: { title: 'Hello', body: 'Hono is a cool project' } })
if (res.ok) {
  const data = await res.json()
  console.log(data.message)
}
```
`res` is a fetch-compatible Response.

## Status codes
Pass the status explicitly (`c.json({ error: 'not found' }, 404)`, `c.json({ post }, 200)`) so the client can narrow: `res.status === 404` gives `{ error: string }`. Use `InferResponseType<typeof client.posts.$get, 200>` for one status.

## Params and query
Path params and query values MUST be strings:

```ts
await client.posts[':id'].$get({ param: { id: '123' }, query: { page: '1' } })
await client.posts[':postId'][':authorId'].$get({ param: { postId: '123', authorId: '456' }, query: {} })
```

## Headers, cookies, init
```ts
const client = hc<AppType>('/api', {
  headers: { Authorization: 'Bearer TOKEN' },
  init: { credentials: 'include' }, // send cookies
})
await client.search.$get({}, { headers: { 'X-Custom-Header': 'hc' } })
```
A per-request `init` (a `RequestInit`, for example `{ signal }`) has the highest priority and can override body, method and headers.

## Gotchas
- `hc` does not URL-encode `param`. Slashes in a value need `/posts/:id{.+}` on the server or `encodeURIComponent` on the client.
- Do not use `c.notFound()` if the client must read the body; its data is `unknown`.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page guides/rpc.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
