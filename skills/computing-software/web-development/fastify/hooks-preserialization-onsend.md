---
id: computing-software.web-development.fastify.hooks-preserialization-onsend
name: hooks-preserialization-onsend
category: computing-software
field: web-development
product: fastify
tags: [fastify, hooks, pre-serialization, on-send, payload]
level: advanced
status: docs-checked
description: "Modify a reply payload with preSerialization (objects) and onSend (serialized string, Buffer, stream)."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`preSerialization(request, reply, payload, done)` lets you change the object before it is serialized. Return the new payload or call `done(null, newPayload)`.

```js
fastify.addHook('preSerialization', async (request, reply, payload) => {
  return { wrapped: payload }
})
```

It is NOT called when the payload is a string, Buffer, stream or null.

`onSend(request, reply, payload, done)` lets you change the payload. If you change it, you may only change it to a string, Buffer, stream, ReadableStream, Response or null.

```js
fastify.addHook('onSend', async (request, reply, payload) => {
  reply.header('x-served-by', 'api')
  return payload.replace('foo', 'bar') // payload is a string here
})
```

Callback form: `done(err, newPayload)`. To send an empty body, replace the payload with `null`, for example:

```js
fastify.addHook('onSend', (request, reply, payload, done) => {
  reply.code(304)
  done(null, null)
})
```

Effects on length: an empty string `''` also gives an empty body but sets `Content-Length: 0`, whereas `Content-Length` is not set if the payload is `null`.

Gotcha: the `done` callback is not available in `async` hooks; invoking it there may cause unexpected behavior.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Hooks.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
