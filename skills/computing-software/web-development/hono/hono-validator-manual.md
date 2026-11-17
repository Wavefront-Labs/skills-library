---
id: computing-software.web-development.hono.hono-validator-manual
name: hono-validator-manual
category: computing-software
field: web-development
product: hono
tags: [hono, guide, validation, validator, forms]
level: practitioner
status: docs-checked
description: "Validate input in Hono with the hono/validator middleware: targets, returning validated values, content-type requirement, lowercase headers and multiple validators."
sources:
  - https://github.com/honojs/website/blob/main/docs/guides/validation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manual validation

```ts
import { validator } from 'hono/validator'

app.post(
  '/posts',
  validator('form', (value, c) => {
    const body = value['body']
    if (!body || typeof body !== 'string') {
      return c.text('Invalid!', 400)
    }
    return { body: body }
  }),
  (c) => {
    const { body } = c.req.valid('form')
    return c.json({ message: 'Created!' }, 201)
  }
)
```

Return a Response to reject, or return the validated value. Targets: `form`, `json`, `query`, `header`, `param`, `cookie`.

## Multiple validators
```ts
app.post('/posts/:id', validator('param', ...), validator('query', ...), validator('json', ...), (c) => { /* ... */ })
```

## Gotcha 1: content-type
For `json` or `form`, the request MUST carry a matching `Content-Type` header, otherwise the body is not parsed and the callback gets `{}`. In tests with `app.request()`:

```ts
// works
await app.request('/testing', {
  method: 'POST',
  body: JSON.stringify({ key: 'value' }),
  headers: new Headers({ 'Content-Type': 'application/json' }),
})
```
Without the header you get `{}` back.

## Gotcha 2: header names are lowercase
In `validator('header', ...)` use `value['idempotency-key']`, NOT `value['Idempotency-Key']` (the latter is always undefined, so the check always fails).

```ts
validator('header', (value, c) => {
  const idempotencyKey = value['idempotency-key']
  if (idempotencyKey == undefined || idempotencyKey === '') {
    throw new HTTPException(400, { message: 'Idempotency-Key is required' })
  }
  return { idempotencyKey }
})
```

## Checked
2026-11-04: every claim left was read in the honojs/website docs page guides/validation.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
