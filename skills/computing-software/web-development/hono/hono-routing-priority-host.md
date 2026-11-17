---
id: computing-software.web-development.hono.hono-routing-priority-host
name: hono-routing-priority-host
category: computing-software
field: web-development
product: hono
tags: [hono, api, routing, middleware-order, host-routing]
level: practitioner
status: docs-checked
description: "Understand Hono registration-order routing, place middleware and fallbacks correctly, and route by hostname or Host header with getPath."
sources:
  - https://github.com/honojs/website/blob/main/docs/api/routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Routing priority and host-based routing

Handlers and middleware run in REGISTRATION order, and once a handler returns a response processing stops.

```ts
app.get('/book/a', (c) => c.text('a'))
app.get('/book/:slug', (c) => c.text('common'))
// GET /book/a -> a ; GET /book/b -> common
```

A catch-all above a specific route swallows it:

```ts
app.get('*', (c) => c.text('common'))
app.get('/foo', (c) => c.text('foo'))
// GET /foo -> common (foo is never dispatched)
```

- Middleware you want to run must be written ABOVE the handler: `app.use(logger()); app.get('/foo', ...)`.
- A fallback handler goes BELOW the others: `app.get('/bar', ...); app.get('*', (c) => c.text('fallback'))`.

## Hostname in the path
```ts
const app = new Hono({
  getPath: (req) => req.url.replace(/^https?:\/([^?]+).*$/, '$1'),
})
app.get('/www1.example.com/hello', (c) => c.text('hello www1'))
app.get('/www2.example.com/hello', (c) => c.text('hello www2'))
```

## Host header
```ts
const app = new Hono({
  getPath: (req) =>
    '/' + req.headers.get('host') +
    req.url.replace(/^https?:\/\/[^/]+(\/[^?]*).*/, '$1'),
})
app.get('/www1.example.com/hello', (c) => c.text('hello www1'))
```
The same technique can route by `User-Agent`.

## Gotcha
The order bug is easy to miss: a wildcard or `:param` route placed too early hides later routes without any error.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page api/routing.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
