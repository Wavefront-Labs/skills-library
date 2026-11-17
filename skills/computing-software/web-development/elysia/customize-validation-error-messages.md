---
id: computing-software.web-development.elysia.customize-validation-error-messages
name: customize-validation-error-messages
category: computing-software
field: web-development
product: elysia
tags: [elysia, validation, error-handling, custom-error, validation-detail, onerror]
level: practitioner
status: docs-checked
description: "Customize Elysia validation failures with the schema error property as string or function, onError VALIDATION handling, error.all, and validationDetail."
sources:
  - https://elysiajs.com/essential/validation.html
  - https://elysiajs.com/tutorial/patterns/validation-error/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: return a clear message when a request fails schema validation.

## error property on a type

```typescript
t.Object({
	x: t.Number({ error: 'x must be a number' })
}, { error: 'Invalid object UnU' })

t.String({ format: 'email', error: 'Invalid email :(' })
t.Array(t.String(), { error: 'All members must be a string' })
```

`error` can also be a function receiving `{ errors, type, validation, value }` (the same arguments as `ValidationError`): `t.Number({ error() { return 'Expected x to be a number' } })`.

## Which error fires

The function is called per field, only when that field is invalid. For `t.Object({ x: t.Number({ error }) })`: body `{ x: "hello" }` uses the field message; body `"hello"` (not an object) uses the default error because the field was never checked, unless the object itself has `error`, in which case the object message wins.

## Catch all in onError

```typescript
new Elysia().onError(({ code, error }) => {
	if (code === 'VALIDATION') return error.message
})
```

The narrowed `error` is a `ValidationError` from `elysia/error`. Its `validator` is a TypeBox `TypeCheck`, and `error.all` lists every cause, each with `path` (OpenAPI-compliant, e.g. `/name`) and `summary`:

```typescript
const name = error.all.find((x) => x.summary && x.path === '/name')
```

A route may also pass `error({ code, error })` next to its schema.

## Validation detail

By default the error is a detail object: `type: "validation"`, `on` (such as `params`), `property`, `message`, `summary`, `found`, `expected`, `errors`. Supplying a custom `error` string replaces all of it. To keep the detail while customising the message, wrap it:

```typescript
import { validationDetail } from 'elysia'
t.Number({ error: validationDetail('Age must be a number') })
```

## Gotchas

- The `error` function is only called when its own field is invalid; supply `error` on the parent object as well to cover a wrong top-level type.

## Checked

Checked 2026-11-07 against the Elysia documentation source (essential/validation.html, tutorial/patterns/validation-error/); each claim, option name and default was compared with the page text. No changes were needed.

Method: documentation only; no commands were run.
