---
id: computing-software.web-development.fastify.hooks-onrequest-preparsing
name: hooks-onrequest-preparsing
category: computing-software
field: web-development
product: fastify
tags: [fastify, hooks, on-request, pre-parsing, streams]
level: advanced
status: docs-checked
description: "Use onRequest for early checks and preParsing to wrap the raw payload stream, such as decompression."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`onRequest` is the first hook: `(request, reply, done)` or `async (request, reply)`. `request.body` is `undefined` there, because body parsing happens before `preValidation`.

`preParsing` receives a fourth argument, the payload stream: `(request, reply, payload, done)` or `async (request, reply, payload)`. If it returns a value (via `return` or the callback), it must be a stream (`done(null, newPayload)` or `return newPayload`). A typical use is decompressing the request body.

```js
fastify.addHook('preParsing', async (request, reply, payload) => {
  // Some code
  await asyncMethod()
  return newPayload
})
```

Rules:
- Add a `receivedEncodedLength` property to the returned stream. It is used to correctly match the request payload with the `Content-Length` header; ideally update it on each received chunk.
- The size of the returned stream is checked not to exceed the `bodyLimit` option.
- `request.body` is `undefined` here, because body parsing happens before `preValidation`.

Gotcha: the `done` callback is not available in `async` hooks or hooks returning a Promise; invoking it there may cause unexpected behavior such as duplicate invocation of handlers.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Hooks.md) and confirmed. Removed or corrected: an invented Decompressor and parseInt example, replaced by the page's own preParsing example; the invented Verify step.

Method: documentation only; no commands were run.
