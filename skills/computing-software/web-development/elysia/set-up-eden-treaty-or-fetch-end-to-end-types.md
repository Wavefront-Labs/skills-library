---
id: computing-software.web-development.elysia.set-up-eden-treaty-or-fetch-end-to-end-types
name: set-up-eden-treaty-or-fetch-end-to-end-types
category: computing-software
field: web-development
product: elysia
tags: [elysia, eden-overview, eden-treaty, eden-fetch, type-safety, monorepo]
level: practitioner
status: docs-checked
description: "Install Eden, export the Elysia App type, call the API with treaty or edenFetch, and fix the usual type inference problems such as version mismatch or path aliases."
sources:
  - https://elysiajs.com/eden/overview.html
  - https://elysiajs.com/eden/installation.html
  - https://elysiajs.com/eden/treaty/overview.html
  - https://elysiajs.com/eden/fetch.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get a type-safe client for an Elysia server with no code generation.

## Install and export

On the frontend: `bun add @elysia/eden` and `bun add -d elysia` (use the same Elysia version as the server). On the server, export the type:

```typescript
const app = new Elysia()
	.get('/hi', () => 'Hi Elysia')
	.get('/id/:id', ({ params: { id } }) => id)
	.post('/mirror', ({ body }) => body, { body: t.Object({ id: t.Number(), name: t.String() }) })
	.listen(3000)

export type App = typeof app
```

## Eden Treaty (recommended)

```typescript
import { treaty } from '@elysia/eden'
import type { App } from './server'

const client = treaty<App>('localhost:3000')
const { data } = await client.hi.get()
const { data: id } = await client.id({ id: 1895 }).get()
const { data: m } = await client.mirror.post({ id: 1895, name: 'Skadi' })
```

Path to property: `/` is `.get()`, `/hi` is `.hi.get()`, `/deep/nested` POST is `.deep.nested.post()`. Dynamic segments become a function with the parameter name: `/item/:name` is `.item({ name: 'Skadi' })`, so `.id` after it is `/item/:name/id`.

## Eden Fetch

```typescript
import { edenFetch } from '@elysia/eden'
const fetch = edenFetch<App>('http://localhost:3000')
const nendoroid = await fetch('/mirror', { method: 'POST', body: { id: 1895, name: 'Skadi' } })
await fetch('/id/:id', { params: { id: '1895' } })
```

It returns `{ data, error }`; `error.status` and `error.value` work as in Treaty. It has no WebSocket support. Since Elysia 1.0 it is no longer faster than Treaty; prefer Treaty unless one process has over 500 routes consumed by a single frontend codebase, where Fetch gives better TS performance.

## When inference breaks

1. `compilerOptions.strict: true` in tsconfig.
2. Mismatched Elysia versions: run `npm why elysia`, there must be one top-level version.
3. TypeScript at least 5.0 on the client.
4. Server code must use method chaining.
5. Server returning Bun-specific types (`Bun.file`): add `@types/bun` to the client.
6. Monorepo path aliases must resolve to the same files from the frontend as from the backend, otherwise types resolve to `any`. Namespace them (`@frontend/*`, `@backend/*`) and share a root tsconfig with `baseUrl`.

## Gotchas

- Eden is under 2KB and relies purely on type inference.

## Checked

2026-11-07. Read in full: eden/overview, eden/installation, eden/treaty/overview (path mapping and dynamic path sections) and eden/fetch. Confirmed install commands, the `App` type export, Treaty and Fetch examples, path-to-property mapping, the six inference fixes, the Fetch WebSocket limitation, and the 500-route guidance. Nothing removed.

Method: documentation only; no commands were run.
