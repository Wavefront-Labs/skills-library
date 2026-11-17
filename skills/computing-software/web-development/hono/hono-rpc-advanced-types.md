---
id: computing-software.web-development.hono.hono-rpc-advanced-types
name: hono-rpc-advanced-types
category: computing-software
field: web-development
product: hono
tags: [hono, rpc, typescript, client, types]
level: advanced
status: docs-checked
description: "Advanced Hono RPC client features: ApplyGlobalResponse, typed not-found, $url, $path, parseResponse, query serializer, file upload and custom fetch."
sources:
  - https://github.com/honojs/website/blob/main/docs/guides/rpc.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hono RPC: advanced client features

## Global error types
The client does not infer responses from `app.onError()` or global middleware. Merge them with `ApplyGlobalResponse`:

```ts
import type { ApplyGlobalResponse } from 'hono/client'
type AppWithErrors = ApplyGlobalResponse<typeof app, {
  401: { json: { error: string; message: string } }
  500: { json: { error: string; message: string } }
}>
const client = hc<AppWithErrors>('http://localhost')
```
`InferResponseType` then includes the error shapes.

## Typed 404
Augment the interface so `c.notFound()` is typed:

```ts
declare module 'hono' {
  interface NotFoundResponse extends Response, TypedResponse<{ error: string }, 404, 'json'> {}
}
app.get('/posts/:id', (c) => { /* ... return c.notFound() */ }).notFound((c) => c.json({ error: 'not found' }, 404))
```

## URLs and paths
```ts
client.api.posts[':id'].$url({ param: { id: '123' } }).pathname // /api/posts/123
client.api.posts.$path({ query: { page: '1', limit: '10' } })    // /api/posts?page=1&limit=10
const typed = hc<typeof route, 'http://localhost:8787'>('http://localhost:8787/') // precise TypedURL
```
`$url()` needs an ABSOLUTE base URL (`hc('/')` throws `Failed to construct 'URL'`); `$path()` works with any base.

## Other helpers
- `buildSearchParams: (query) => URLSearchParams` option on `hc` for bracket-style arrays (`${k}[]`).
- `fetch` option: `hc<T>('http://localhost', { fetch: c.env.AUTH.fetch.bind(c.env.AUTH) })` to use a service binding.
- File upload: `client.user.picture.$put({ form: { file: new File([data], name, { type }) } })` with `z.instanceof(File)` on the server.
- `InferRequestType<typeof client.todo.$post>['form']` and `InferResponseType<...>`.
- `parseResponse(client.hello.$get())` parses by Content-Type and throws `DetailedError` when not ok.

## Gotcha
Use `async`/`await` in handlers. A handler returning a `.then()` chain loses the response type (client sees `unknown`); annotate with `TypedResponse<{ hello: string }, 200, 'json'>` if unavoidable.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page guides/rpc.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
