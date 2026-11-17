---
id: computing-software.web-development.fastify.middleware-and-use
name: middleware-and-use
category: computing-software
field: web-development
product: fastify
tags: [fastify, middleware, express, middie, migration]
level: practitioner
status: docs-checked
description: "Use Express or Connect style middleware through @fastify/express or @fastify/middie, and prefer native hooks and plugins."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Middleware.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V4.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V3.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`fastify.use()` is not built in (middleware is not supported out of the box as of v3.0.0). To run middleware, register a plugin first:

```js
await fastify.register(require('@fastify/middie'))
fastify.use(require('cors')())
```

or `@fastify/express` for a full Express compatibility layer.

Pass a path as first argument to restrict middleware (`use('/css', ...)`, `use('/css/(.*)', ...)`, `use(['/css','/js'], ...)`); this does not support routes with parameters (e.g. `/user/:id/comments`), and wildcards are not supported in multiple paths. Fastify wraps `req`/`res` into Request/Reply after the middleware phase, so middleware gets the Node.js `req` and `res` and has no `send`; use a `preHandler` hook to get Fastify's Request and Reply. @fastify/middie provides simple Express-style middleware with improved performance.

Native replacements:
- `cors` becomes `@fastify/cors`.
- `helmet` becomes `@fastify/helmet`.
- `serve-static` becomes `@fastify/static`.

Middleware can be encapsulated with `register`, which controls where it runs.

Gotcha: middleware is not supported out of the box, so `fastify.use` needs `@fastify/express` or `@fastify/middie` registered first.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Middleware.md, Migration-Guide-V4.md, Migration-Guide-V3.md) and confirmed. Removed or corrected: a failure claim about fastify.use, reworded to what the page says; the invented Verify step.

Method: documentation only; no commands were run.
