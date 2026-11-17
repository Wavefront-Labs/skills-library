---
id: computing-software.web-development.elysia.extend-context-with-state-decorate-derive-resolve
name: extend-context-with-state-decorate-derive-resolve
category: computing-software
field: web-development
product: elysia
tags: [extends-context, state, decorate, derive, resolve, affix, prefix]
level: practitioner
status: docs-checked
description: "Choose between state, decorate, derive and resolve to add properties to the Elysia context, plus remap and prefix affix for plugin name collisions."
sources:
  - https://elysiajs.com/patterns/extends-context.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: add shared values to the Elysia handler context with correct typing and timing.

## Pick the API

| API | Assigned | Use for |
| --- | --- | --- |
| `state(key, value)` | once, at call time, into `store` | shared mutable primitives |
| `decorate(key, value)` | once, at call time, onto context | constants, class instances, singletons (should not be mutated) |
| `derive(fn)` | per request, at transform (before validation) | new props from headers/query/body; types come out unknown |
| `resolve(fn)` | per request, at beforeHandle (after validation) | same, but typed |

```ts
new Elysia()
  .state('counter', 0)
  .decorate('logger', new Logger())
  .derive(({ headers }) => {
    const auth = headers['authorization']
    return { bearer: auth?.startsWith('Bearer ') ? auth.slice(7) : null }
  })
  .get('/', ({ bearer, store }) => bearer)
```

Typed resolve: declare `.guard({ headers: t.Object({ bearer: t.String({ pattern: '^Bearer .+$' }) }) })` first, then `.resolve(({ headers }) => ({ bearer: headers.bearer.slice(7) }))`.

## Rules and gotchas

- Define state/decorate before the routes that read it; using `store.counter` before `.state('counter', 0)` is a type error.
- Mutate state through the store reference (`store.counter++`). Destructuring `({ store: { counter } })` copies a primitive and loses the link.
- If `derive` or `resolve` returns `status(400)` (take `status` from the context), Elysia exits early and sends that as the response.
- Only extend context for global mutable state, request/response-related values, or values derived from existing properties; otherwise keep a plain module value.

## Three assignment patterns (state and decorate)

- key-value: `.state('counter', 0)`
- object: `.decorate({ logger: new Logger(), trace: new Trace() })`
- remap: `.state(({ version, ...store }) => ({ ...store, elysiaVersion: 1 }))` returns a whole new object; properties you omit (here `version`) are removed. Remap sets initial values only, no reactivity. `derive` only supports remap-style functions.

## Affix: avoid plugin collisions

```ts
const setup = new Elysia({ name: 'setup' }).decorate({ argon: 'a', boron: 'b', carbon: 'c' })
new Elysia().use(setup).prefix('decorator', 'setup').get('/', ({ setupCarbon }) => setupCarbon)
```

`prefix('decorator', 'setup')` renames decorated properties to camelCase (`setupCarbon`); use `prefix('all', 'setup')` to remap every property kind.

## Checked

2026-11-07. Read in full: patterns/extends-context. Confirmed the state, decorate, derive and resolve semantics and timing, the reference-versus-value gotcha, early exit with `status(400)`, key-value, object and remap patterns, and affix `prefix('decorator', ...)` and `prefix('all', ...)`. Nothing removed.

Method: documentation only; no commands were run.
