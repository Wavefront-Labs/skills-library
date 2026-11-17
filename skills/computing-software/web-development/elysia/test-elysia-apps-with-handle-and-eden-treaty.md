---
id: computing-software.web-development.elysia.test-elysia-apps-with-handle-and-eden-treaty
name: test-elysia-apps-with-handle-and-eden-treaty
category: computing-software
field: web-development
product: elysia
tags: [elysia, eden-test, eden-treaty, unit-test, handle, bun-test]
level: practitioner
status: docs-checked
description: "Test Elysia routes without a server using app.handle or app.fetch with a Request, or a type-safe treaty(app) client, and type-check tests with tsc."
sources:
  - https://elysiajs.com/eden/test.html
  - https://elysiajs.com/eden/treaty/unit-test.html
  - https://elysiajs.com/tutorial/features/unit-test/
  - https://elysiajs.com/essential/route.html
  - https://elysiajs.com/essential/plugin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: assert behaviour of routes (including lifecycle) with bun test, Vitest or Jest.

## Raw request

`app.handle(new Request('http://localhost/'))` (or `app.fetch(...)` in the tutorial) takes a Web Standard Request and returns a Response, processed like a real request, no server needed.

```typescript
import { describe, it, expect } from 'bun:test'
import { Elysia } from 'elysia'

describe('Elysia', () => {
	it('should return Hello World', async () => {
		const app = new Elysia().get('/', 'Hello World')
		const text = await app.fetch(new Request('http://localhost/')).then((r) => r.text())
		expect(text).toBe('Hello World')
	})
})
```

The same code works with Vitest (import from `vitest`) and Jest (`@jest/globals`).

## Typed client without a network

Pass the instance to Treaty; it skips the network and infers types, so no generic is needed:

```typescript
import { treaty } from '@elysia/eden'
const app = new Elysia().get('/hello', 'hi')
const api = treaty(app)

it('returns a response', async () => {
	const { data } = await api.hello.get()
	expect(data).toBe('hi')
})
```

## Against a running server

The older Eden test page uses `edenTreaty<typeof app>('http://localhost:3000')` after `.listen(3000)`. Run `bun test`.

## Type-level test

`tsc --noEmit test/**/*.ts` verifies types between client and server, useful during migrations.

## Async and lazy plugins

Before calling `handle`, wait for deferred modules: `await app.modules`.

## Gotchas

- Unlike mocks, `handle` runs the full lifecycle, so hooks and validation are exercised.
- The Eden test page imports `edenTreaty` while the rest of the docs use `treaty`; the Eden overview describes `treaty` as the improved version of Eden Treaty 1 (`edenTreaty`), so use `treaty`.

## Checked

2026-11-07. Read in full: eden/test, eden/treaty/unit-test, tutorial/features/unit-test, essential/route (Handle), essential/plugin (Testing) and essential/best-practice (Testing). Confirmed `handle` and `fetch` with a Web Standard Request, bun, Vitest and Jest examples, `treaty(app)` without a network, `tsc --noEmit`, `await app.modules`, and the "behaves like an actual request, unlike mocks" tip. Reworded the `edenTreaty` gotcha to cite the Eden overview.

Method: documentation only; no commands were run.
