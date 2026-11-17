---
id: computing-software.web-development.fastify.hooks-error-response-timeout-abort
name: hooks-error-response-timeout-abort
category: computing-software
field: web-development
product: fastify
tags: [fastify, hooks, on-error, on-response, on-timeout, on-request-abort]
level: advanced
status: docs-checked
description: "Use onError, onResponse, onTimeout and onRequestAbort hooks for logging, metrics and cleanup without changing the reply."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `onResponse(request, reply, done)`: runs after the response was sent; you cannot send more. Use for metrics. It can still send data to external services, for example to gather statistics.
- `onError(request, reply, error, done)`: runs when an error is thrown, before the custom error handler set by `setErrorHandler`. For custom error logging or adding a header. Calling `reply.send` in it throws an exception, and passing an error to `done` is not supported.
- `onTimeout(request, reply, done)`: runs when a request times out and the HTTP socket has been hung up (needs `connectionTimeout` set on the instance), so you cannot send data to the client.
- `onRequestAbort(request, done)`: runs when a client closes the connection before the entire request has been processed, so you cannot send data to the client.

```js
fastify.addHook('onError', async (request, reply, error) => {
  request.log.warn({ code: error.code }, 'request failed')
})

fastify.addHook('onResponse', async (request, reply) => {
  request.log.info({ statusCode: reply.statusCode }, 'response sent')
})

fastify.addHook('onRequestAbort', async (request) => {
  request.log.info('client went away')
})
```

Gotcha: `onError` is not intended for changing the error; do that in `setErrorHandler`. `onTimeout` is triggered by socket-level timeouts set via `connectionTimeout`; per-route application-level timeouts use the `handlerTimeout` option, which uses `request.signal`.

Gotcha: client abort detection is not completely reliable (see Guides/Detecting-When-Clients-Abort.md).

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Hooks.md) and confirmed. Removed or corrected: an invented metrics.observe example; the invented Verify step.

Method: documentation only; no commands were run.
