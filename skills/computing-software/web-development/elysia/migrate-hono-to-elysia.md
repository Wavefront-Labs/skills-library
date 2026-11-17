---
id: computing-software.web-development.elysia.migrate-hono-to-elysia
name: migrate-hono-to-elysia
category: computing-software
field: web-development
product: elysia
tags: [migrate, hono, middleware, macro, scoping, validation]
level: practitioner
status: docs-checked
description: "Port a Hono app to Elysia: routes, validation, file upload, middleware, context, macros, errors, plugin scoping, cookies and tests, with the traps."
sources:
  - https://github.com/elysiajs/documentation/blob/main/docs/migrate/from-hono.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: move a Hono application to Elysia by mapping each Hono idiom to its Elysia equivalent.

## Routes and handlers

Hono wraps responses with `c.text` and `c.json`. Elysia maps a returned value to a response, and a constant can be given inline. Use `status` from the context for a non-200 code, and `listen` to start the server.

```ts
import { Elysia } from 'elysia'

new Elysia()
  .get('/', 'Hello World')
  .post('/id/:id', ({ status, params: { id } }) => status(201, id))
  .listen(3000)
```

Query, headers and body are read straight from the context: `ctx.query.limit`, `ctx.headers.authorization`, `ctx.body.name`. There is no `c.req.query()` call. Elysia only parses what the handler uses (static analysis).

## Subrouters

`app.route('/api', sub)` becomes `new Elysia({ prefix: '/api' })` plus `.use(sub)`. The prefix is optional; Hono requires one.

## Validation

Replace `zValidator` pipes with the route schema: `params: t.Object({ id: t.Number() })`, `body: t.Object({ name: t.String() })`. TypeBox coerces the param. Zod and Valibot schemas go in the same fields (Standard Schema), so no adapter package is needed.

## File upload

Replace Zod `instanceof(File)` plus a `file-type` check with `body: t.Object({ file: t.File({ type: 'image' }) })`. Elysia checks the mimetype itself, because the client-supplied `content-type` cannot be trusted.

## Middleware

- `app.use(async (c, next) => ...)` becomes `.onRequest(({ method, path }) => ...)`.
- Route middleware becomes `beforeHandle({ status, headers })` returning `status(401)`. There is no `next`.
- `c.set` / `c.get` and `declare module` for `ContextVariableMap` become `.decorate('version', 2)` for constants and `.resolve(...)` for per-request values; the types follow automatically.
- `createMiddleware` factories such as `role('admin')` become a `.macro({ role: (role) => ({ resolve(...) {...} }) })`, used as `{ role: 'admin' }` on the route.

## Errors

`app.onError` becomes a class with optional `status` and `toResponse()`, registered with `.error({ CUSTOM: CustomError })`, handled in `.onError(({ error, code }) => ...)`. A per-route `error({ error })` handler is also allowed.

## Plugin side effects

Both frameworks encapsulate by default. In Elysia add `.as('scoped')` to the sub instance so its hooks apply in the parent. The three scopes are local (default), scoped and global. Give the plugin a unique `name` so repeated `.use` applies it once; Hono can double-run a shared middleware.

## Cookies and OpenAPI

`getSignedCookie` / `setSignedCookie` become `new Elysia({ cookie: { secret: 'secret' } })` (as the migration page writes it; the cookie page's constructor examples use `secrets` and `sign`, see the cookie-secrets skill) with `cookie: { name }` in the context; assigning `name.value` signs, and reading verifies. For OpenAPI use `.use(openapi())` from `@elysia/openapi`, register `.model({...})` and refer to it as `body: 'user'`.

## Verify

`app.request('/')` becomes `await app.handle(new Request('http://localhost'))`; check `res.status` and `await res.text()`. Alternatively `treaty(app)` from `@elysia/eden` gives typed test calls.

## Gotchas

- Elysia's style guide recommends method chaining and object destructuring.
- Hono type inference failed with "Type instantiation is excessively deep" past about 100 complex routes; the docs report Elysia holding to at least 2,000.
- Choosing Elysia on Cloudflare Workers may lose Cloudflare-specific features Hono ships.

## Checked

2026-11-07. Read in full: the Migrate from Hono page (docs/migrate/from-hono.txt in the elysiajs/documentation repo). The old elysiajs.com/migrate/from-hono.html URL returns 404 because the site config excludes migrate/*, so the source now points at the repo file. Confirmed every comparison: routing, handler parsing, subrouter prefix, validation (TypeBox, Zod, Valibot), file upload, middleware, `decorate`/`resolve`, `macro`, errors, scoping (local, scoped, global) and deduplication by `name`, cookies, OpenAPI `model`, testing with `handle` and `treaty`, and the "over a 100 routes" versus "at least 2,000 routes" type-inference claim. One edit: the cookie bullet now notes that the migration page writes `cookie: { secret }` while the cookie page uses `secrets` and `sign`.

Method: documentation only; no commands were run.
