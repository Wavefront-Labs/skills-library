---
id: computing-software.web-development.hono.hono-test-client
name: hono-test-client
category: computing-software
field: web-development
product: hono
tags: [hono, helper, testing, typescript, rpc]
level: practitioner
status: docs-checked
description: "Write type-safe Hono endpoint tests with testClient from hono/testing, including chained route definitions, query params and custom headers."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Testing helper (testClient)

Import: `import { testClient } from 'hono/testing'`.

`testClient(app)` returns a client typed from your routes like the RPC client, so tests get autocomplete.

## Requirement
Define routes by CHAINING directly on `new Hono()`. Type inference flows through chained `.get()`/`.post()` calls; the usual `const app = new Hono(); app.get(...)` pattern gives no route types.

```ts
// index.ts
const app = new Hono().get('/search', (c) => {
  const query = c.req.query('q')
  return c.json({ query: query, results: ['result1', 'result2'] })
})
export default app
```

```ts
// index.test.ts
import { testClient } from 'hono/testing'
import { describe, it, expect } from 'vitest'
import app from './app'

describe('Search Endpoint', () => {
  const client = testClient(app)
  it('should return search results', async () => {
    const res = await client.search.$get({ query: { q: 'hono' } })
    expect(res.status).toBe(200)
    expect(await res.json()).toEqual({ query: 'hono', results: ['result1', 'result2'] })
  })
})
```

## Headers and init
The second argument is an `init` option (RequestInit-like) for headers, method, body:

```ts
const res = await client.search.$get(
  { query: { q: 'hono' } },
  { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } }
)
```

## Gotcha
If routes are defined separately after creating the Hono instance, `testClient` does not get the type information for specific routes. Export the chained app.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page helpers/testing.md. Removed: the invented Verify step and the claim that untyped routes lose the search property silently.
Method: documentation only; no commands were run.
