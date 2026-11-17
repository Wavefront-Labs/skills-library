---
id: computing-software.web-development.fastify.reply-hijack-trailers-early-hints
name: reply-hijack-trailers-early-hints
category: computing-software
field: web-development
product: fastify
tags: [fastify, reply, hijack, trailers, early-hints]
level: sme
status: docs-checked
description: "Take over the raw response with reply.hijack, set HTTP trailers, and send 103 early hints."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Reply.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V5.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`reply.hijack()` can be called at any point before `reply.send()`. It stops Fastify from sending the response and from running the remaining hooks (and the user handler, if hijacked earlier); you take responsibility for `reply.raw`. `reply.sent` is true afterwards, the automatic send when an async handler resolves is skipped, and a pending `handlerTimeout` timer is cleared. If you send through `reply.raw`, the `onResponse` hooks still run.

```js
fastify.get('/raw', (request, reply) => {
  reply.hijack()
  reply.raw.end('hello')
})
```

In v5 this replaces setting `reply.sent = true`.
Trailers (headers sent after the data, e.g. `Server-Timing`, `Etag`): `reply.trailer(key, fn)`, `reply.hasTrailer(key)`, `reply.removeTrailer(key)`. The function receives `(reply, payload, done)` (payload is null for streams), or can be async and return the value; directly returning a value from a sync function was removed in v5. Errors passed to `done` are ignored (enable `debug` logging to see them). HTTP/1 responses get `Transfer-Encoding: chunked`; HTTP/2 uses native trailers.

```js
fastify.get('/route', (req, reply) => {
  reply.trailer('ETag', async function (reply, payload) {
    return 'custom-etag'
  })
  reply.send('')
})
```

Early hints: `reply.writeEarlyHints(hints, callback)` sends hints so the client can preload or preconnect before the final response. `hints` is an object of key-value pairs; the optional callback runs once the hint is sent or on error.

```js
reply.writeEarlyHints({ Link: '</styles.css>; rel=preload; as=style' })
```

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Reply.md, Migration-Guide-V5.md, Server.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
