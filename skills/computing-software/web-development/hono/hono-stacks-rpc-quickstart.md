---
id: computing-software.web-development.hono.hono-stacks-rpc-quickstart
name: hono-stacks-rpc-quickstart
category: computing-software
field: web-development
product: hono
tags: [hono, rpc, zod, client, typescript]
level: practitioner
status: docs-checked
description: "Share API types between server and client with Hono Stacks: Zod validation, exported AppType, hc client and a React Query example."
sources:
  - https://github.com/honojs/website/blob/main/docs/concepts/stacks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hono Stacks (RPC quickstart)

The Hono Stack is Hono (server) + Zod + Zod Validator middleware + `hc` (client).

## Server
```ts
import { zValidator } from '@hono/zod-validator'
import * as z from 'zod'

const route = app.get(
  '/hello',
  zValidator('query', z.object({ name: z.string() })),
  (c) => {
    const { name } = c.req.valid('query')
    return c.json({ message: `Hello! ${name}` })
  }
)
export type AppType = typeof route
```

For RPC inference, ALL methods must be chained and the type must come from a declared variable.

## Client
```ts
import type { AppType } from './server'
import { hc } from 'hono/client'

const client = hc<AppType>('/api')
const res = await client.hello.$get({ query: { name: 'Hono' } })
const data = await res.json()
console.log(`${data.message}`)
```

## React Query pattern
```ts
const api = new Hono()
  .post('/todo', zValidator('form', schema), (c) => { /* ... */ return c.json({ message: 'created!' }) })
  .get('/todo', (c) => c.json({ todos }))
export type AppType = typeof api
const app = new Hono(); app.route('/api', api)
```

```tsx
const client = hc<AppType>('/api')
const $post = client.todo.$post
const mutation = useMutation<InferResponseType<typeof $post>, Error, InferRequestType<typeof $post>['form']>({
  mutationFn: async (todo) => (await $post({ form: todo })).json(),
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
})
```
Import `InferResponseType` and `InferRequestType` from `hono/client`.

## Gotcha
Non-chained route definitions (`app.get(...)` as separate statements) are not captured in the type, so the client loses those routes.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page concepts/stacks.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
