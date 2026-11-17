---
id: computing-software.web-development.hono.hono-rpc-performance
name: hono-rpc-performance
category: computing-software
field: web-development
product: hono
tags: [hono, rpc, typescript, performance, monorepo]
level: advanced
status: docs-checked
description: "Speed up Hono RPC in large apps: chain sub-routers, match versions, use project references, precompile the client type and split clients."
sources:
  - https://github.com/honojs/website/blob/main/docs/guides/rpc.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hono RPC at scale and IDE performance

## Large apps: chain everything
```ts
// authors.ts
const app = new Hono()
  .get('/', (c) => c.json('list authors'))
  .post('/', (c) => c.json('create an author', 201))
export default app

// index.ts
const app = new Hono()
const routes = app.route('/authors', authors).route('/books', books)
export default app
export type AppType = typeof routes
```
Export the type of the chained result (`routes`), not of the bare `app`.

## Why the IDE slows down
Each route triggers heavy type instantiation in tsserver. Mitigations:

1. **Same Hono version** on backend and frontend. A mismatch gives `Type instantiation is excessively deep and possibly infinite`.
2. **TypeScript project references** when the backend lives in another directory.
3. **Compile the client type** (recommended):
```ts
import { app } from './app'
import { hc } from 'hono/client'
const client = hc<typeof app>('') // computed at compile time
export type Client = typeof client
export const hcWithType = (...args: Parameters<typeof hc>): Client => hc<typeof app>(...args)
```
Use `hcWithType('http://localhost:8787/')` in the frontend after compiling. In a monorepo, a tool like turborepo can separate the server and client projects; you can also coordinate the build manually with tools like concurrently or npm-run-all.
4. **Specify type arguments manually**: `new Hono().get<'foo/:id'>('foo/:id', handler)`. Even one argument helps, but is laborious.
5. **Split clients per sub-app**: `hc<typeof authorsApp>('/authors')`, `hc<typeof booksApp>('/books')`.

## Gotcha
The docs advise chaining the handlers (and the `.route()` calls) so that the types are always inferred, and exporting the type of the chained result.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page guides/rpc.md. Removed: the invented Verify step and the claim that the server project must be built first in a monorepo.
Method: documentation only; no commands were run.
