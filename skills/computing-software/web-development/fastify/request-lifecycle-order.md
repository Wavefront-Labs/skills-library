---
id: computing-software.web-development.fastify.request-lifecycle-order
name: request-lifecycle-order
category: computing-software
field: web-development
product: fastify
tags: [fastify, lifecycle, hooks, request]
level: practitioner
status: docs-checked
description: "Know the order of request hooks and where errors, validation and serialization fit in a Fastify request."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Lifecycle.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Request hooks run in this order:

1. `onRequest`
2. `preParsing`
3. body parsing (content type parser)
4. `preValidation`
5. validation
6. `preHandler`
7. route handler
8. `preSerialization`
9. `onSend`
10. response is sent
11. `onResponse`

Side hooks: `onError` runs when an error occurs, before the custom error handler; `onTimeout` fires on socket timeout (`connectionTimeout`); `onRequestAbort` fires when the client aborts.

Consequences:
- `request.body` is `undefined` in `onRequest` and `preParsing` because parsing happens before `preValidation`.
- A validation failure skips `preHandler` and the handler and goes to the error path (400).
- An error thrown at a step goes to the `onError` hook, then `setErrorHandler`, then the reply is sent. JSON payloads are serialized by the reply serializer if set, else the serializer compiler when a schema exists for the status code, else `JSON.stringify`.
- Replying from a hook stops the hook chain: the remaining hooks and the handler do not run.
- `reply.hijack()` (before or during the handler) stops later hooks and the handler and stops Fastify sending the response; if `reply.raw` is used to respond, `onResponse` hooks still run.
- With `handlerTimeout` configured, a timer starts after routing; if no response is sent in time, `request.signal` is aborted and a `503` is sent. The timer is cancelled when the response completes or on `reply.hijack()`.

```js
fastify.addHook('onRequest', async (request) => { request.start = Date.now() })
fastify.addHook('onResponse', async (request, reply) => {
  request.log.info({ ms: Date.now() - request.start }, 'done')
})
```

Gotcha: `preSerialization` is skipped when the payload is a string, Buffer, stream or null.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Lifecycle.md, Hooks.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
