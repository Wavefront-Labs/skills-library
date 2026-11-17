---
id: computing-software.web-development.fastify.reply-serialization-helpers
name: reply-serialization-helpers
category: computing-software
field: web-development
product: fastify
tags: [fastify, reply, serialization, schema, performance]
level: advanced
status: docs-checked
description: "Use reply.serializer, serialize, getSerializationFunction and compileSerializationSchema for custom or ad hoc serialization."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Reply.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `reply.serializer(func)`: replaces the default JSON serializer for this request. By default `.send()` JSON-serializes anything that is not a Buffer, stream, string, `undefined` or Error. With a custom serializer you must set a custom `Content-Type` header, e.g. `reply.header('Content-Type', 'application/x-protobuf').serializer(protoBuf.serialize)`. It is unnecessary if you serialize yourself and send a Buffer, stream or string.
- `reply.serialize(payload)`: serializes with the custom serializer set via `.serializer()` if any, otherwise the route's default serializer, which takes the response schema for the current status code into account. Returns the serialized payload.
- `reply.getSerializationFunction(schema | httpStatus, [contentType])`: returns a serialization function for a schema or status code (depends on the route's `schema.response` or functions compiled via `compileSerializationSchema`); `undefined` if none is found.
- `reply.compileSerializationSchema(schema, [httpStatus], [contentType])`: compiles with the `SerializerCompiler` and returns a function. `httpStatus` and `contentType` are forwarded to the compiler. Cached in a `WeakMap`.
- `reply.serializeInput(data, [schema | httpStatus], [httpStatus], [contentType])`: serializes the data; if both a schema and `httpStatus` are given, `httpStatus` takes precedence. If no function exists for the schema, a new one is compiled.
- `reply.getDecorator(name)`: returns a reply decorator declared with `decorateReply` (functions come back bound to the reply); throws `FST_ERR_DEC_UNDECLARED` if undeclared.

```js
const serialize = reply.compileSerializationSchema({
  type: 'object',
  properties: { foo: { type: 'string' } }
})
serialize({ foo: 'bar' }) // '{"foo":"bar"}'

reply.serializeInput({ foo: 'bar' }, 200) // '{"foo":"bar"}'
```

Gotcha: the cache is keyed on the schema reference. If you mutate a schema and recompile, the old compiled function is reused (`newSerialize === serialize` is `true`). To change a schema, create a totally new object.

`fastify.setReplySerializer(fn)` sets a default for all routes when `reply.serializer` was not set; it is called only for 2xx statuses.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Reply.md, Server.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
