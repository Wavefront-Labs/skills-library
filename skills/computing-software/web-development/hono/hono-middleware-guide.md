---
id: computing-software.web-development.hono.hono-middleware-guide
name: hono-middleware-guide
category: computing-software
field: web-development
product: hono
tags: [hono, guide, middleware, execution-order]
level: intro
status: docs-checked
description: "Learn Hono middleware: handler vs middleware, app.use with path and method, onion execution order, error behavior of next, built-ins and Deno version trap."
sources:
  - https://github.com/honojs/website/blob/main/docs/guides/middleware.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Middleware guide

- **Handler**: returns a `Response`; only one handler runs.
- **Middleware**: `await next()` and return nothing to continue, OR return a `Response` to exit early.

```ts
app.use(logger())               // any method, all routes
app.use('/posts/*', cors())     // path
app.post('/posts/*', basicAuth()) // method and path
app.post('/posts', (c) => c.text('Created!', 201))
// order: logger() -> cors() -> basicAuth() -> handler
```

## Execution order
Registration order decides. Code before `next()` of the first-registered middleware runs first; code after `next()` runs last:

```
middleware 1 start
  middleware 2 start
    middleware 3 start
      handler
    middleware 3 end
  middleware 2 end
middleware 1 end
```

## Errors
If a handler or middleware throws, Hono catches it and passes it to `app.onError()` or converts it to a 500 before returning up the chain. So `next()` never throws: there is no need to wrap it in try/catch/finally.

## Built-ins
```ts
import { poweredBy } from 'hono/powered-by'
app.use(poweredBy())
app.use(logger())
app.use('/auth/*', basicAuth({ username: 'hono', password: 'acoolproject' }))
```

## Context in middleware args
```ts
app.use('*', async (c, next) => {
  const middleware = cors({ origin: c.env.CORS_ORIGIN })
  return middleware(c, next)
})
```

## Gotcha (Deno)
Mixing Hono and middleware versions via `jsr:` imports (for example `jsr:@hono/hono@4.4.0` with `jsr:@hono/hono@4.4.5/deno`) can break at runtime.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page guides/middleware.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
