---
id: computing-software.web-development.hono.hono-routing-patterns
name: hono-routing-patterns
category: computing-software
field: web-development
product: hono
tags: [hono, api, routing, path-params]
level: intro
status: docs-checked
description: "Define Hono routes: methods, wildcards, all, custom on() methods, path params, optional and regexp params, slashes in params and chained routes."
sources:
  - https://github.com/honojs/website/blob/main/docs/api/routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Routing patterns

```ts
app.get('/', (c) => c.text('GET /'))
app.post('/', ...); app.put('/', ...); app.delete('/', ...)
app.query('/', (c) => c.text('QUERY /'))
app.get('/wild/*/card', (c) => c.text('GET /wild/*/card'))   // wildcard
app.all('/hello', (c) => c.text('Any Method /hello'))
app.on('PURGE', '/cache', (c) => c.text('PURGE Method /cache')) // custom method
app.on(['PUT', 'DELETE'], '/post', (c) => c.text('PUT or DELETE /post'))
app.on('GET', ['/hello', '/ja/hello', '/en/hello'], (c) => c.text('Hello'))
```

## Parameters
```ts
app.get('/user/:name', (c) => c.req.param('name'))
app.get('/posts/:id/comment/:comment_id', (c) => {
  const { id, comment_id } = c.req.param()
})
```

Optional: `app.get('/api/animal/:type?', ...)` matches `/api/animal` and `/api/animal/:type`.

Regexp: `app.get('/post/:date{[0-9]+}/:title{[a-z]+}', ...)`.

Including slashes: `app.get('/posts/:filename{.+\\.png}', ...)`.

## Chained route
```ts
app
  .get('/endpoint', (c) => c.text('GET /endpoint'))
  .post((c) => c.text('POST /endpoint'))
  .delete((c) => c.text('DELETE /endpoint'))
```

## Gotcha
In a regexp param the pattern follows the name in braces, as in `:date{[0-9]+}`; the docs write the backslash in `.png` as `\\.` inside a TS string.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page api/routing.md. Removed: the invented Verify step and the claim that strict mode is on by default.
Method: documentation only; no commands were run.
