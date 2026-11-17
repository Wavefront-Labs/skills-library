---
id: computing-software.web-development.hono.hono-custom-middleware
name: hono-custom-middleware
category: computing-software
field: web-development
product: hono
tags: [hono, guide, middleware, typescript, createmiddleware]
level: practitioner
status: docs-checked
description: "Write reusable typed Hono middleware with createMiddleware, replace c.res after next, extend Context via Variables and rely on chained type inference."
sources:
  - https://github.com/honojs/website/blob/main/docs/guides/middleware.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom middleware

Inline:

```ts
app.use(async (c, next) => {
  console.log(`[${c.req.method}] ${c.req.url}`)
  await next()
})
app.use('/message/*', async (c, next) => {
  await next()
  c.header('x-message', 'This is middleware!')
})
```

For reuse in separate files use `createMiddleware` from `hono/factory` so `c` and `next` keep their types:

```ts
const logger = createMiddleware(async (c, next) => {
  console.log(`[${c.req.method}] ${c.req.url}`)
  await next()
})
// with generics: createMiddleware<{ Bindings: Bindings }>(async (c, next) => ...
```

## Replace the response after next
```ts
const stripRes = createMiddleware(async (c, next) => {
  await next()
  c.res = undefined
  c.res = new Response('New Response')
})
```

## Extend Context type-safely
```ts
const echoMiddleware = createMiddleware<{
  Variables: { echo: (str: string) => string }
}>(async (c, next) => {
  c.set('echo', (str) => str)
  await next()
})
app.get('/echo', echoMiddleware, (c) => c.text(c.var.echo('Hello!')))
```

## Chained inference
Each `.use()` returns a new Hono instance with merged types, so later handlers see all `Variables`:

```ts
const app = new Hono()
  .use(authMiddleware)   // sets user
  .use(dbMiddleware)     // sets db
  .get('/', (c) => c.json({ user: c.var.user }))
```
This removes most need to hand-write a combined `Env`.

## Gotchas
- To use `c` in the options of a built-in middleware, build it per request (`cors({ origin: c.env.CORS_ORIGIN })(c, next)`).

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/guides/middleware.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the unstated "call c.set before next" rule.

Method: documentation only; no commands were run.
