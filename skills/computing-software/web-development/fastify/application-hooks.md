---
id: computing-software.web-development.fastify.application-hooks
name: application-hooks
category: computing-software
field: web-development
product: fastify
tags: [fastify, hooks, on-ready, on-listen, on-close, pre-close]
level: advanced
status: docs-checked
description: "Application lifecycle hooks onReady, onListen, preClose and onClose, with ordering and error behavior."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Application hooks run on instance events, not per request.

- `onReady`: triggered before the server starts listening and when `.ready()` is invoked. It cannot change routes or add hooks. Hooks run serially, and the server only starts listening after all have completed. They take a `done` callback (or are async) and run with `this` bound to the Fastify instance.
- `onListen`: triggered when the server starts listening. Hooks run one after another; an error is logged and ignored, and the queue continues. It does not run when started via `inject()` or `ready()`. An alternative to `fastify.server.on('listening', ...)`.
- `preClose`: triggered when `close()` is invoked. The server is already rejecting new requests with 503 (when `return503OnClosing` is `true`) but has not stopped listening and in-flight requests are still processed. Useful for state such as open WebSocket or Server-Sent Events connections that would prevent `server.close()` from completing.
- `onClose`: triggered when `close()` is invoked; by then the HTTP server has stopped listening and in-flight requests are done, so it is the place to release resources such as database pools. Child plugins' `onClose` hooks run before parents'. It takes `(instance, done)` or an async `(instance)`, or an object implementing `Symbol.asyncDispose` or `Symbol.dispose`.

```js
fastify.addHook('onReady', async function () {
  await this.cache.warm()
})
fastify.addHook('onListen', async function () {
  this.log.info('listening')
})
fastify.addHook('onClose', async (instance) => {
  await instance.db.end()
})
```

Arrow functions do not get the Fastify instance as `this`; use `function` when you need it, or the `instance` parameter in `onClose`.

Gotcha: `onListen` never fires with `inject()` or `ready()`. An error in `onListen` is logged and ignored.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Hooks.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
