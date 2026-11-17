---
id: computing-software.web-development.hono.hono-logger-middleware
name: hono-logger-middleware
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, logging]
level: intro
status: docs-checked
description: "Log requests and responses in Hono with the logger middleware, custom PrintFunc and NO_COLOR handling."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/logger.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Logger middleware

Import: `import { logger } from 'hono/logger'`.

```ts
const app = new Hono()
app.use(logger())
app.get('/', (c) => c.text('Hello Hono!'))
```

It logs the incoming request (method, path) as `<-- POST /blog` and the outgoing response (method, path, status, elapsed time) as `--> POST /blog 201 93ms`. Status codes are colour-coded; elapsed time is shown in ms or s.

## Custom PrintFunc
The optional argument is `PrintFunc(str: string, ...rest: string[])`:

```ts
export const customLogger = (message: string, ...rest: string[]) => {
  console.log(message, ...rest)
}
app.use(logger(customLogger))
```

You can reuse it inside a route to add your own lines between the request and response logs:

```ts
app.post('/blog', (c) => {
  customLogger('Blog saved:', `Path: ${blog.url},`, `ID: ${blog.id}`)
  // <-- POST /blog
  // Blog saved: Path: /blog/example, ID: 1
  // --> POST /blog 201 93ms
})
```

## Gotcha
To disable colour, set the `NO_COLOR` environment variable. Cloudflare Workers has no `process.env`, so it outputs plain text anyway.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page logger.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
