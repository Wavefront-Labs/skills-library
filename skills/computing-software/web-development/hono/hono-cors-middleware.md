---
id: computing-software.web-development.hono.hono-cors-middleware
name: hono-cors-middleware
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, cors, security]
level: practitioner
status: docs-checked
description: "Configure CORS in Hono with the cors middleware: origin lists and functions, allowMethods, credentials, env-based setup and the Vite conflict."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/cors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CORS middleware

Import: `import { cors } from 'hono/cors'`. Register it BEFORE the routes.

```ts
app.use('/api/*', cors())
app.use(
  '/api2/*',
  cors({
    origin: 'http://example.com',
    allowHeaders: ['X-Custom-Header', 'Upgrade-Insecure-Requests'],
    allowMethods: ['POST', 'GET', 'OPTIONS'],
    exposeHeaders: ['Content-Length', 'X-Kuma-Revision'],
    maxAge: 600,
    credentials: true,
  })
)
```

## Options (all optional)
- `origin`: `string | string[] | (origin, c) => string`, default `*`.
- `allowMethods`: `string[]` or `(origin, c) => string[]`, default `['GET','HEAD','PUT','POST','DELETE','PATCH','QUERY']`.
- `allowHeaders` (default `[]`), `exposeHeaders` (default `[]`), `maxAge`, `credentials`.

Multiple origins: `origin: ['https://example.com', 'https://example.org']`. Function form: `origin: (origin, c) => origin.endsWith('.example.com') ? origin : 'http://example.com'`.

Per-origin methods:

```ts
cors({
  origin: (origin) => (origin === 'https://example.com' ? origin : '*'),
  allowMethods: (origin, c) =>
    origin === 'https://example.com'
      ? ['GET', 'HEAD', 'POST', 'PATCH', 'DELETE']
      : ['GET', 'HEAD'],
})
```

## Environment-dependent config
```ts
app.use('*', async (c, next) => {
  const corsMiddlewareHandler = cors({ origin: c.env.CORS_ORIGIN })
  return corsMiddlewareHandler(c, next)
})
```

## Gotcha with Vite
Set `server: { cors: false }` in `vite.config.ts` so Vite's built-in CORS does not conflict with Hono's.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/cors.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
