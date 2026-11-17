---
id: computing-software.web-development.elysia.compose-macros-with-schema-and-extension
name: compose-macros-with-schema-and-extension
category: computing-software
field: web-development
product: elysia
tags: [macro, macro-schema, macro-extension, named-macro, deduplication, seed]
level: advanced
status: docs-checked
description: "Build Elysia macros that carry schemas, extend other macros, use typed resolve via named single macros, and control macro deduplication with seed."
sources:
  - https://elysiajs.com/patterns/macro.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: compose macros so a single route option brings schema, lifecycle and context together with correct types.

## Macro with a schema

A macro can contribute a validation schema. The route's own schema and the macro's co-exist, and schemas from several macros (or Standard Validator schemas) stack.

```ts
new Elysia()
  .macro({
    withFriends: {
      body: t.Object({ friends: t.Tuple([t.Literal('Fouco'), t.Literal('Sartre')]) })
    }
  })
  .post('/', ({ body }) => body.friends, {
    body: t.Object({ name: t.Literal('Lilith') }),
    withFriends: true
  })
```

## Typing lifecycle inside the same macro

TypeScript cannot infer types into a lifecycle hook of the same macro when several macros are in one object. Use the named single form `.macro('name', {...})`:

```ts
.macro('withFriends', {
  body: t.Object({ friends: t.Tuple([t.Literal('Fouco'), t.Literal('Sartre')]) }),
  beforeHandle({ body: { friends } }) { /* friends is typed */ }
})
```

The same limitation applies to a macro extending another with `resolve`:

```ts
.macro('user', { resolve: () => ({ user: 'lilith' as const }) })
.macro('user2', { user: true, resolve: ({ user }) => { /* user is typed */ } })
```

Using macro schema to type a route's own hooks works fine; the limit is only for hooks in the same macro.

## Extending macros

A macro may enable others by setting them to `true`:

```ts
.macro({
  sartre: { body: t.Object({ sartre: t.Literal('Sartre') }) },
  fouco:  { body: t.Object({ fouco: t.Literal('Fouco') }) },
  lilith: { fouco: true, sartre: true, body: t.Object({ lilith: t.Literal('Lilith') }) }
})
.post('/', ({ body }) => body, { lilith: true })
```

## Deduplication and seed

Elysia deduplicates macro lifecycle events so each runs once. By default the property value is the seed; override it by returning `seed`:

```ts
sartre: (role: string) => ({ seed: role, body: t.Object({ sartre: t.Literal('Sartre') }) })
```

## Gotchas

- Circular macro dependencies are cut off by a stack limit of 16 (runtime and types).
- If the route already has OpenAPI `detail`, Elysia merges it with the macro's detail and the route's detail wins.
- A macro that "extends" another through `resolve` types only with the named single macro workaround.

## Checked

Checked 2026-11-07 against the Elysia documentation source (patterns/macro.html); each claim, option name and default was compared with the page text. No changes were needed.

Method: documentation only; no commands were run.
