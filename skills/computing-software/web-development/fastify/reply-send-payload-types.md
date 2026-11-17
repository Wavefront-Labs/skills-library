---
id: computing-software.web-development.fastify.reply-send-payload-types
name: reply-send-payload-types
category: computing-software
field: web-development
product: fastify
tags: [fastify, reply, send, serialization, payloads]
level: practitioner
status: docs-checked
description: "How reply.send treats objects, strings, Buffers, streams, ReadableStream, Response and Error payloads."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Reply.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`reply.send(payload)` picks behavior by type:

- Object: serialized with fast-json-stringify when an output schema is set, otherwise `JSON.stringify()`.
- String: without a Content-Type, sent as `text/plain; charset=utf-8`. With a Content-Type set, it is serialized by a custom serializer if one is set, otherwise sent unmodified, even for `application/json`. To serialize a string as JSON, set a custom serializer.
- Buffer / TypedArray / stream: `application/octet-stream` if no Content-Type is set. These are pre-serialized, so they are sent unmodified without response validation.
- Web `ReadableStream` is treated like a Node stream (pre-serialized). `Response` carries payload, status and headers together; its payload is pre-serialized, and its status and headers do not show in `reply.statusCode` / `reply.getHeaders()` (readonly, may confuse `onSend` checks).
- Error: Fastify builds `{ error, code, message, statusCode }` (error = HTTP message, code = Fastify error code). If the error's statusCode is below 400 it is set to 500. Custom properties such as `headers` enhance the HTTP response.
- Over HTTP/2, stream chunks are not changed by Fastify; split very large chunks in your own code.
- In async handlers that send from a callback (Buffer or stream), return or await the reply object.

```js
fastify.get('/json-string', async function (request, reply) {
  reply
    .type('application/json; charset=utf-8')
    .serializer(JSON.stringify)
    .send('Hello') // Returns "Hello" (JSON-encoded string)
})

fastify.get('/streams', function (request, reply) {
  const stream = fs.createReadStream('some-file', 'utf8')
  reply.header('Content-Type', 'application/octet-stream')
  reply.send(stream)
})
```

The type of the sent payload (after serialization and any `onSend` hooks) must be a string, Buffer, stream, `undefined` or `null`, otherwise an error is thrown.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Reply.md) and confirmed. Removed or corrected: an invented /file stream example replaced by the page's stream example; the invented Verify step.

Method: documentation only; no commands were run.
