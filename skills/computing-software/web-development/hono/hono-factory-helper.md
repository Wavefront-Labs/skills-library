---
id: computing-software.web-development.hono.hono-factory-helper
name: hono-factory-helper
category: computing-software
field: web-development
product: hono
tags: [hono, helper, typescript, factory, middleware]
level: practitioner
status: docs-checked
description: "Create typed middleware, handlers and apps in Hono with createFactory, createMiddleware, createHandlers, createApp, initApp and defaultAppOptions."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/factory.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Factory helper

Import: `import { createFactory, createMiddleware } from 'hono/factory'`.

## createMiddleware
```ts
const messageMiddleware = createMiddleware(async (c, next) => {
  await next()
  c.res.headers.set('X-Message', 'Good morning!')
})
```
To take arguments, wrap it in a function:

```ts
const messageMiddleware = (message: string) =>
  createMiddleware(async (c, next) => {
    await next()
    c.res.headers.set('X-Message', message)
  })
app.use(messageMiddleware('Good evening!'))
```

## createFactory and createHandlers
`createFactory<Env>()` lets you type `Env` once. `factory.createHandlers(...)` defines handlers away from `app.get('/')` with correct types:

```ts
const factory = createFactory()
const middleware = factory.createMiddleware(async (c, next) => {
  c.set('foo', 'bar')
  await next()
})
const handlers = factory.createHandlers(logger(), middleware, (c) => c.json(c.var.foo))
app.get('/api', ...handlers)
```

## createApp: Env in one place
```ts
type Env = { Variables: { myVar: string } }
const factory = createFactory<Env>()
const app = factory.createApp()
const mw = factory.createMiddleware(async (c, next) => { await next() })
```

## Options
- `defaultAppOptions: HonoOptions`, applied to apps from `createApp()`, e.g. `createFactory({ defaultAppOptions: { strict: false } })`.
- `initApp: (app) => void`, runs on each app created, e.g. install a middleware that sets `c.set('db', drizzle(c.env.MY_DB))`.

```ts
export default createFactory<Env>({
  initApp: (app) => {
    app.use(async (c, next) => {
      c.set('db', drizzle(c.env.MY_DB))
      await next()
    })
  },
})
```

## Gotcha
Without `createFactory<Env>()` and `createApp()`, `Env` has to be set in two places: `new Hono<Env>()` and `createMiddleware<Env>()`.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/helpers/factory.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the speculative "can drift" claim.

Method: documentation only; no commands were run.
