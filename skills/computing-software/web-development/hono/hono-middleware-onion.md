---
id: computing-software.web-development.hono.hono-middleware-onion
name: hono-middleware-onion
category: computing-software
field: web-development
product: hono
tags: [hono, concepts, middleware]
level: intro
status: docs-checked
description: "Understand the Hono onion middleware model and write a response-time middleware using next and c.res."
sources:
  - https://github.com/honojs/website/blob/main/docs/concepts/middleware.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Middleware model

A handler is the primitive that returns a `Response`. Middleware runs before and after the handler, like an onion: code before `await next()` runs on the way in, code after it runs on the way out.

```ts
app.use(async (c, next) => {
  const start = performance.now()
  await next()
  const end = performance.now()
  c.res.headers.set('X-Response-Time', `${end - start}`)
})
```

You can write your own middleware, or use built-in and third-party middleware.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page concepts/middleware.md. Removed: the invented Verify step, the Practical rules (return next(), registration advice, createMiddleware) and the Gotcha, none of which are on the cited page.
Method: documentation only; no commands were run.
