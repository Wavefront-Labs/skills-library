---
id: computing-software.web-development.hono.hono-context-responses
name: hono-context-responses
category: computing-software
field: web-development
product: hono
tags: [hono, api, context, responses]
level: practitioner
status: docs-checked
description: "Build responses with the Hono Context: status, header, body, text, json, html, notFound, redirect, res and the render/setRenderer layout pattern."
sources:
  - https://github.com/honojs/website/blob/main/docs/api/context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Context: building responses

A `Context` is created per request and lives until the response returns.

```ts
app.post('/posts', (c) => {
  c.status(201)                       // default is 200
  c.header('X-Message', 'My custom message')
  return c.text('Your post is created!')
})
```

- `c.text('Hello!')` gives `text/plain`; `c.json({ message: 'Hello!' })` gives `application/json`; `c.html('<h1>Hi</h1>')` gives `text/html`.
- `c.body('Thank you for coming', 201, { 'X-Message': 'Hello!', 'Content-Type': 'text/plain' })` returns a raw body with status and headers. Prefer `text()`/`html()` for text and HTML.
- `c.notFound()` returns a 404 (customise with `app.notFound()`).
- `c.redirect('/')` is 302 by default; `c.redirect('/', 301)` for permanent.
- `c.res` is the Response that will be returned; after `await next()` in middleware you can modify it: `c.res.headers.append('X-Debug', 'Debug message')`.

## Layouts with render / setRenderer
```tsx
app.use('/pages/*', async (c, next) => {
  c.setRenderer((content, head) => c.html(
    <html><head><title>{head.title}</title></head>
    <body><header>{head.title}</header><p>{content}</p></body></html>
  ))
  await next()
})
app.get('/pages/my-favorite', (c) => c.render(<p>Ramen and Sushi</p>, { title: 'My favorite' }))
```
Type the extra argument by augmenting `ContextRenderer`:

```ts
declare module 'hono' {
  interface ContextRenderer {
    (content: string | Promise<string>, head: { title: string }): Response | Promise<Response>
  }
}
```

## Gotcha
To change the Response that will be returned, do it after `await next()` in middleware, as in the page's `c.res.headers.append` example.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/api/context.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the unstated claims about when c.res holds the final body.

Method: documentation only; no commands were run.
