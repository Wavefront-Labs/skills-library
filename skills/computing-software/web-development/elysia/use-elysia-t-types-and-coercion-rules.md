---
id: computing-software.web-development.elysia.use-elysia-t-types-and-coercion-rules
name: use-elysia-t-types-and-coercion-rules
category: computing-software
field: web-development
product: elysia
tags: [typebox, elysia-t, t-file, t-numeric, t-union-enum, coercion, t-optional]
level: practitioner
status: docs-checked
description: "Pick the right Elysia.t type (File, Files, Numeric, UnionEnum, ObjectString, Nullable) and avoid surprises from its Number/Boolean coercion and Optional behaviour."
sources:
  - https://elysiajs.com/patterns/typebox.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: write route schemas with `Elysia.t` (TypeBox plus server-oriented types) and predict how HTTP strings are validated.

## TypeBox basics that carry over

`t.String()`, `t.Number()`, `t.Boolean()`, `t.Array(t.Number())`, `t.Object({ x: t.Number() })`, `t.Null()`, `t.Literal(42)`, `t.Union([t.String(), t.Number()])`, `t.Partial(t.Object({...}))`, `t.Optional(...)`. Attributes follow JSON Schema: `t.String({ format: 'email' })`, `t.Number({ minimum: 10, maximum: 100 })`, `t.Array(t.Number(), { minItems: 1, maxItems: 5 })`, `t.Object({...}, { additionalProperties: true })` (default false). A mismatch is thrown into the error lifecycle (`onError`).

## Elysia-specific types

- `t.UnionEnum(['rapi', 'anis', 1, true, false])`: value must be one of the listed values.
- `t.File({ type, minSize, maxSize })`: `type` is a string or array of formats (such as `'image'`); sizes are bytes or a `'1k'` / `'5m'` string (`k` = 1024 bytes, `m` = 1048576). `t.Files()` is an array of files in one field.
- `t.Cookie({ name: t.String() }, { secrets })`: object-like cookie jar; `secrets` is a string or array (first signs, rotation).
- `t.Nullable(t.String())`: null allowed, undefined not. `t.MaybeEmpty(t.String())`: null and undefined allowed.
- `t.Form({ someValue: t.File() })`: validates a returned FormData.
- `t.UInt8Array()`, `t.ArrayBuffer()`: for bodies parsed with the `arrayBuffer` parser.
- `t.ObjectString()`, `t.BooleanString()`: strings parsed into objects or booleans when the channel (query string, header, FormData) can only carry strings.
- `t.Numeric()`: numeric string or number, transformed to a number; takes the same attributes as a numeric schema.

## Behaviour that differs from plain TypeBox

- `t.Optional` can wrap a whole route schema: `query: t.Optional(t.Object({ name: t.String() }))` makes the whole query optional (same for `body`, `headers`).
- When used directly as a route schema (e.g. inside `params: t.Object({ id: t.Number() })`), `t.Number` is converted to `t.Numeric` because params, query and headers are always strings. It is NOT converted in `body` objects or when used standalone.
- `t.Boolean` is likewise converted to `t.BooleanString`; the page's example shows it converted in `params` and not in `body`, nor standalone.

## Gotchas

- The conversion applies to the top-level route schema (`params`, `query`, `headers`) only; the page's own example shows `t.Number()` inside `body` is NOT converted.
- `t.Nullable` and `t.MaybeEmpty` are not the same: only MaybeEmpty accepts undefined.
- File size suffixes only support `k` and `m`.

## Checked

2026-11-07. Read in full: patterns/typebox (the repo has no include files). Confirmed the primitive types and attributes, `UnionEnum`, `File`/`Files` (`type`, `minSize`, `maxSize`, `k` = 1024 and `m` = 1048576 bytes), `Cookie` `secrets` (string or array, first secret signs), `Nullable`, `MaybeEmpty` (the card text says "empty string or null" but the section text says null and undefined; the skill follows the section text), `Form`, `UInt8Array`, `ArrayBuffer`, `ObjectString`, `BooleanString`, `Numeric`, `t.Optional` on whole schemas, and Number-to-Numeric conversion. Softened the Boolean bullet: the page states no "params/query/headers only" rule for `t.Boolean`, only an example with `params` converted and `body` not.

Method: documentation only; no commands were run.
