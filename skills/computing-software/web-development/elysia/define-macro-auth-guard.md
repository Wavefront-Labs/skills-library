---
id: computing-software.web-development.elysia.define-macro-auth-guard
name: define-macro-auth-guard
category: computing-software
field: web-development
product: elysia
tags: [macro, resolve, auth-guard, status-401, route-option, lifecycle]
level: practitioner
status: docs-checked
description: "Define an Elysia macro that adds a route option which rejects unauthenticated requests with status 401 and injects a user into the context."
sources:
  - https://elysiajs.com/patterns/macro.html
  - https://elysiajs.com/migrate/from-express.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: write a reusable route option (like `auth: true` or `role: 'admin'`) that runs lifecycle logic and adds typed values to the context.

## Basic macro

A macro is a function (or object) that returns lifecycle hooks, schema, or context additions. Once registered it becomes a property you can set in any route's hook options.

```ts
const plugin = new Elysia({ name: 'plugin' })
  .macro({
    hi: (word: string) => ({
      beforeHandle() { console.log(word) }
    })
  })

new Elysia().use(plugin).get('/', () => 'hi', { hi: 'Elysia' })
```

## Auth guard with `resolve`

Return `status(...)` (imported from `elysia`) to short-circuit with an HTTP code:

```ts
import { Elysia, status } from 'elysia'

new Elysia()
  .macro({
    auth: {
      resolve({ headers }) {
        if (!headers.authorization) return status(401, 'Unauthorized')
        return { user: 'SaltyAom' }
      }
    }
  })
  .get('/', ({ user }) => `Hello ${user}`, { auth: true })
```

`user` is typed in the handler because `resolve` added it.

## Property shorthand (since 1.2.10)

A macro property can be an object instead of a function. The object form is turned into a function that takes a boolean and only applies when true, so `isAuth: { resolve: () => ({ user }) }` equals `isAuth(enabled: boolean) { if (!enabled) return; ... }`.

## Parameterised macro

The migration guides show passing an argument: `role: (role: 'user' | 'admin') => ({ resolve({ status, headers: { authorization } }) { const user = findUser(authorization); if (user.role !== role) return status(401); return { user } } })`, used as `{ role: 'admin' }`.

## Gotchas

- Prefer `return status(...)` over `throw new Error()`. A thrown plain error becomes 500, and returned status keeps type inference for Eden and OpenAPI type gen (`throw status` loses it).
- The docs define macros inside a plugin instance and `.use()` it from the app so routes can use the option.
- The migration guide's `role` sample uses `throw status(401)`; the macro page recommends `return status(...)` for type inference.

## Checked

Checked 2026-11-07 against the Elysia documentation source (patterns/macro.html, migrate/from-express.html); each claim, option name and default was compared with the page text. Added a note that the migration guide sample uses throw status(401).

Method: documentation only; no commands were run.
