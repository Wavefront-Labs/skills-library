---
id: computing-software.web-development.fastify.response-schema-serialization
name: response-schema-serialization
category: computing-software
field: web-development
product: fastify
tags: [fastify, serialization, response-schema, performance, security]
level: practitioner
status: docs-checked
description: "Define response schemas per status code to speed serialization and hide fields, including content-type specific schemas."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Validation-and-Serialization.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Getting-Started.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With an output schema, Fastify uses fast-json-stringify to send JSON; this can drastically increase throughput and help prevent accidental disclosure of sensitive information. The response schema is chosen by status code.

```js
const opts = {
  schema: {
    response: {
      200: {
        type: 'object',
        properties: { hello: { type: 'string' } }
      },
      '2xx': { type: 'object', properties: { ok: { type: 'boolean' } } },
      default: { type: 'object', properties: { error: { type: 'string' } } }
    }
  }
}
```

Keys: an exact status code, a class such as `'2xx'`, or `default`.

Per content type:

```js
response: {
  200: {
    content: {
      'application/json': { schema: { type: 'object', properties: { a: { type: 'string' } } } },
      '*/*': { schema: { type: 'string' } }
    }
  }
}
```

Fastify matches the response `Content-Type` against the declared keys and falls back to `*/*` if present. If the Content-Type is not declared and there is no `*/*` key, serialization fails closed: it throws `FST_ERR_MISSING_CONTENTTYPE_SERIALIZATION_FN` and replies 500 instead of using `JSON.stringify`. Declare every Content-Type the route may return, or add a `*/*` catch-all.

`fastify.setSerializerCompiler(({ schema, method, url, httpStatus, contentType }) => data => JSON.stringify(data))` replaces the serializer compiler; it must return a function that returns a string. `serializerOpts` in the factory sets fast-json-stringify options (e.g. `rounding: 'ceil'`). For a one-off serializer use `reply.serializer(...)`.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Validation-and-Serialization.md, Getting-Started.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
