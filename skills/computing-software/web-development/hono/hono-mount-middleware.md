---
id: computing-software.web-development.hono.hono-mount-middleware
name: hono-mount-middleware
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, mount, interop, itty-router]
level: advanced
status: docs-checked
description: "Mount another framework's fetch handler inside Hono with mount, controlling path rewriting and the arguments passed to it."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/mount.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mount middleware

Import: `import { mount } from 'hono/mount'`.

Register it with `app.all()` on a path ending in `/*`:

```ts
import { Router as IttyRouter } from 'itty-router'

const ittyRouter = IttyRouter()
ittyRouter.get('/hello', () => new Response('Hello from itty-router'))

const app = new Hono()
app.all('/itty-router/*', mount(ittyRouter.handle))
```

By default the mounted app gets a new `Request` with the matched prefix removed: `/itty-router/hello` arrives as `/hello`. It is called as `handler(request, c.env, c.executionCtx)`.

## optionHandler
`(c) => unknown` returns the arguments after the Request; an array is spread. Pass as the second argument directly or in an object:

```ts
app.all('/app/*', mount(anotherApp, (c) => c.env))
// anotherApp(request, c.env)

app.all('/app/*', mount(anotherApp, { optionHandler: (c) => [c.env, c.executionCtx] }))
// anotherApp(request, c.env, c.executionCtx)
```

## replaceRequest
`((originalRequest: Request) => Request) | false`:

```ts
app.all('/legacy/*', mount(anotherApp, {
  replaceRequest: (req) => {
    const url = new URL(req.url)
    url.pathname = url.pathname.replace(/^\/legacy/, '/api')
    return new Request(url, req)
  },
}))
```

`replaceRequest: false` passes the original Request untouched (shorthand for `(req) => req`).

## Gotcha
If the mounted app expects its full original path, set `replaceRequest: false`; otherwise the prefix is stripped.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page middleware/builtin/mount.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
