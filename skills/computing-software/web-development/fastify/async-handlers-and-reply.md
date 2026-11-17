---
id: computing-software.web-development.fastify.async-handlers-and-reply
name: async-handlers-and-reply
category: computing-software
field: web-development
product: fastify
tags: [fastify, handlers, async, promises, reply]
level: practitioner
status: docs-checked
description: "Return values or reply.send from async handlers, and when to return reply to avoid double sends."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Routes.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V4.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In an async handler, return the payload and Fastify sends it:

```js
fastify.get('/', async (request, reply) => {
  return { hello: 'world' }
})
```

If you send the response yourself with `reply.send`, signal that with `return reply` (or `await reply`) so the promise chain is forked correctly:

```js
fastify.get('/', async (request, reply) => {
  setImmediate(() => reply.send({ hello: 'world' }))
  return reply
})
```

Rules:
- Returning a value AND calling `reply.send(value)`: the first takes precedence, the second is discarded, and a warn log is emitted.
- `undefined` cannot be returned (see Promise resolution in Routes.md).
- If you use `async`/promises and `reply.send`, do `return reply` / `await reply`; if you return the value, do not use `reply.send`.
- If a callback API calls `reply.send()` outside the promise chain, `await reply` (or `return reply`) so the handler waits.
- It is recommended to use only one style (callback or async) for consistent error handling.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Routes.md, Migration-Guide-V4.md) and confirmed. Removed or corrected: a v5 plugin-mixing bullet not in the cited pages; the invented Verify step.

Method: documentation only; no commands were run.
