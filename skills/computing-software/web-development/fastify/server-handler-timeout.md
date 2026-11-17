---
id: computing-software.web-development.fastify.server-handler-timeout
name: server-handler-timeout
category: computing-software
field: web-development
product: fastify
tags: [fastify, server, handler-timeout, abort-signal, http-503]
level: advanced
status: docs-checked
description: "Use handlerTimeout to answer 503 FST_ERR_HANDLER_TIMEOUT and abort request.signal when a handler runs too long."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Routes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`handlerTimeout` (default 0, disabled) bounds how long a route handler may run. When it elapses Fastify replies 503 with code `FST_ERR_HANDLER_TIMEOUT` and aborts `request.signal`.

```js
const fastify = require('fastify')({ handlerTimeout: 5000 })

fastify.get('/slow', {
  handlerTimeout: 10000   // per-route override, positive integer only
}, async (request, reply) => {
  const res = await fetch('https://example.com', { signal: request.signal })
  return res.json()
})
```

Rules:
- The timeout is cooperative: Fastify does not kill the handler, work continues unless you pass `request.signal` to I/O that supports AbortSignal.
- It covers the whole route lifecycle: routing, onRequest, parsing, validation, handler and serialization.
- A per-route `handlerTimeout` must be a positive integer and takes precedence over the server value; once a server-level timeout is set, routes cannot opt out, only override it with a different positive integer.
- The timeout error is sent through the route's error handler, so a per-route `errorHandler` can check `error.code === 'FST_ERR_HANDLER_TIMEOUT'` and change the status code or body.
- `reply.hijack()` clears the timer; the handler then owns the response lifecycle.
- 404 handlers and custom handlers set with `setNotFoundHandler()` are not subject to it.
- `request.signal` also aborts when the client disconnects; inspect `signal.reason.code` to tell timeout from disconnect.

Unlike `connectionTimeout` and `requestTimeout` (socket level), `handlerTimeout` is application-level and works correctly with HTTP keep-alive connections.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Server.md, Routes.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
