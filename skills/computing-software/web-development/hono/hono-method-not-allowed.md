---
id: computing-software.web-development.hono.hono-method-not-allowed
name: hono-method-not-allowed
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, routing, http-405]
level: practitioner
status: docs-checked
description: "Return 405 with an Allow header instead of 404 when a path exists but the method does not, using Hono methodNotAllowed."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/method-not-allowed.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Method Not Allowed

Import: `import { methodNotAllowed } from 'hono/method-not-allowed'`.

Without it, a request whose path matches a route but whose method is unsupported gets 404. With it, you get `405 Method Not Allowed` and an `Allow` header.

```ts
const app = new Hono()
app.use(methodNotAllowed({ app }))

app.get('/hello', (c) => c.text('Hello!'))
app.post('/hello', (c) => c.text('Posted!'))

// PUT /hello -> 405 Method Not Allowed
// Allow: GET, HEAD, POST
```

## Custom response
```ts
app.use(methodNotAllowed({
  app,
  onMethodNotAllowed: (c, methods) =>
    c.json({ error: 'Method Not Allowed' }, 405, { Allow: methods.join(', ') }),
}))
```

## Options
- `app: Hono`: the middleware collects allowed methods per path from this instance's registered routes.
- `onMethodNotAllowed: (c: Context, allowedMethods: string[]) => Response | Promise<Response>`: generates the response, including its `Allow` header. By default the middleware returns 405 with `Allow` set to the allowed methods.

## Gotcha
The middleware reads the allowed methods from the registered routes of the `app` instance you pass. A custom `onMethodNotAllowed` generates the whole response, including the `Allow` header.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page method-not-allowed.md. Removed: the invented Verify step, the claim that app is required, and the claim that a custom handler must set Allow itself (the page says it generates the response including its Allow header).
Method: documentation only; no commands were run.
