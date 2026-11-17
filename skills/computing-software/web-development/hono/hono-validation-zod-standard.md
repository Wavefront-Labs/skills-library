---
id: computing-software.web-development.hono.hono-validation-zod-standard
name: hono-validation-zod-standard
category: computing-software
field: web-development
product: hono
tags: [hono, guide, validation, zod, valibot, arktype]
level: practitioner
status: docs-checked
description: "Validate Hono requests with Zod, @hono/zod-validator and @hono/standard-validator (sValidator) for Zod, Valibot and ArkType."
sources:
  - https://github.com/honojs/website/blob/main/docs/guides/validation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Validation with Zod and Standard Schema

A third-party validator is recommended.

## Zod inside validator()
```ts
import * as z from 'zod'
const schema = z.object({ body: z.string() })

app.post(
  '/posts',
  validator('form', (value, c) => {
    const parsed = schema.safeParse(value)
    if (!parsed.success) return c.text('Invalid!', 401)
    return parsed.data
  }),
  (c) => { const { body } = c.req.valid('form') /* ... */ }
)
```

## Zod Validator middleware
`npm i @hono/zod-validator`

```ts
import { zValidator } from '@hono/zod-validator'
app.post('/posts', zValidator('form', z.object({ body: z.string() })), (c) => {
  const validated = c.req.valid('form')
})
```

## Standard Schema validator
Standard Schema is a common interface for Zod, Valibot and ArkType. `npm i @hono/standard-validator`, import `sValidator`:

```ts
import { sValidator } from '@hono/standard-validator'

// Zod
const schema = z.object({ name: z.string(), age: z.number() })
// Valibot: v.object({ name: v.string(), age: v.number() })   (import * as v from 'valibot')
// ArkType: type({ name: 'string', age: 'number' })           (import { type } from 'arktype')

app.post('/author', sValidator('json', schema), (c) => {
  const data = c.req.valid('json')
  return c.json({ success: true, message: `${data.name} is ${data.age}` })
})
```

## Checked
2026-11-04: every claim left was read in the honojs/website docs page guides/validation.md. Removed: the invented Verify step and the two Gotchas that applied manual-validator rules to zValidator and cited RPC advice from another page.
Method: documentation only; no commands were run.
