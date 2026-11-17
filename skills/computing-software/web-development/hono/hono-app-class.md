---
id: computing-software.web-development.hono.hono-app-class
name: hono-app-class
category: computing-software
field: web-development
product: hono
tags: [hono, api, app, error-handling, testing]
level: practitioner
status: docs-checked
description: "Use the Hono app object: notFound, onError, fetch entry points, app.request for tests, strict mode, router option, generics and deprecated fire and mount."
sources:
  - https://github.com/honojs/website/blob/main/docs/api/hono.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The Hono app object

Methods: `app.get/post/...`, `all`, `on`, `use`, `route`, `basePath`, `notFound`, `onError`, `mount` (deprecated), `fire` (deprecated), `fetch`, `request`.

## notFound and onError
```ts
app.notFound((c) => c.text('Custom 404 Message', 404))
app.onError((err, c) => {
  console.error(`${err}`)
  return c.text('Custom Error Message', 500)
})
```
`notFound` is only called from the top-level app. If both a parent app and its routes have `onError`, the route-level handler wins.

## Entry point
Cloudflare Workers: `export default app`, or `export default { fetch(request, env, ctx) { return app.fetch(request, env, ctx) } }`. Bun:

```ts
export default { port: 3000, fetch: app.fetch }
```

## request() for tests
```ts
test('GET /hello is ok', async () => {
  const res = await app.request('/hello')
  expect(res.status).toBe(200)
})
```
Also accepts a `Request`: `app.request(new Request('Hello!', { method: 'POST' }))`.

## Options
- `strict` (default `true`): `/hello` and `/hello/` differ; `new Hono({ strict: false })` treats them the same.
- `router`: default `SmartRouter`; e.g. `new Hono({ router: new RegExpRouter() })` from `hono/router/reg-exp-router`.
- Generics: `new Hono<{ Bindings: Bindings; Variables: Variables }>()`.

## Deprecated
`app.fire()` (adds a global `fetch` listener) is deprecated; use `fire()` from `@hono/service-worker`. `app.mount()` is deprecated; use the Mount middleware. `mount()` takes a `replaceRequest` option (a function, or `false` to pass the original `Request` unchanged); by default it passes a new `Request` with the mount path removed.

## Gotcha
Because `notFound` runs only on the top-level app, a sub-app's `notFound` is ignored; define it on the root app.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/api/hono.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the claim that the Mount middleware itself accepts replaceRequest (the page documents it on app.mount()).

Method: documentation only; no commands were run.
