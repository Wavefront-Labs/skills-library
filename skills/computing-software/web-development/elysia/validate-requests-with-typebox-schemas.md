---
id: computing-software.web-development.elysia.validate-requests-with-typebox-schemas
name: validate-requests-with-typebox-schemas
category: computing-software
field: web-development
product: elysia
tags: [elysia, validation, typebox, body, query, params, headers, cookie, response]
level: practitioner
status: docs-checked
description: "Validate Elysia body, query, params, headers, cookie and response with t schemas, including query coercion, array formats and per-status response schemas."
sources:
  - https://elysiajs.com/essential/validation.html
  - https://elysiajs.com/at-glance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: declare schemas in the route's third argument so one definition gives runtime validation, TypeScript types and OpenAPI.

```typescript
import { Elysia, t } from 'elysia'

new Elysia().get('/id/:id', () => 'Hello', {
	query: t.Object({ name: t.String() }),
	params: t.Object({ id: t.Number() })
})
```

`t` is TypeBox tuned for servers. Get a TS type with `typeof MyType.static`.

## Per field

- body: `t.Object({...})`. GET and HEAD bodies are not parsed. Files: `t.File({ format: 'image/*' })`, `t.Files()`; a file type makes Elysia assume `multipart/form-data`.
- query: must be an object; values arrive as strings but Elysia coerces to the schema type, so `t.Number()` accepts `?id=1` and rejects `?id=salt`. Extra keys are allowed (`?name=a&alias=b` passes).
- params: normally unnecessary (inferred as string); add a schema for numeric or template-literal patterns. `/id/a` fails `t.Number()`.
- headers: `additionalProperties` is true by default; use lowercase keys.
- cookie: `t.Cookie({ name: t.String() }, { secure: true, httpOnly: true })` (like `t.Object` plus cookie options); also additional properties by default.
- response: `response: t.Object({...})`, or per status: `response: { 200: t.Object({ name: t.String() }), 400: t.Object({ error: t.String() }) }` used with `status(400, {...})`.

## Query arrays

Declare `name: t.Array(t.String())`. Both `?name=rapi,anis,neon` (comma format) and repeated keys `?name=rapi&name=anis` give an array. Without an array schema a repeated key is a single string.

## guard

`.guard({ query: t.Object({ name: t.String() }) })` applies to every handler after it. If several global schemas hit one property, the latest wins; a local schema beats a global one. Use `schema: 'standalone'` to validate both.

## Expected results

From the page's table for the first example: `/id/1?name=Elysia` passes; `/id/a?name=Elysia`, `/id/1?alias=Elysia` and `/id/a` fail.

## Gotchas

- A guard validates the handlers registered after it only.

## Checked

2026-11-07. Read in full: essential/validation (Schema type, Guard, Guard Schema Type, Body, File, Query, Coercion, Array, Params, Headers, Cookie, Response, Response per status) and the validation parts of at-glance. Confirmed every per-field rule, the query array formats, the guard precedence and the page's result tables. Retitled the Verify section as the page's own expected results and reworded the guard gotcha.

Method: documentation only; no commands were run.
