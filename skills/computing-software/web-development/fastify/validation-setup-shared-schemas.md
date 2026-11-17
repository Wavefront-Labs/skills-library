---
id: computing-software.web-development.fastify.validation-setup-shared-schemas
name: validation-setup-shared-schemas
category: computing-software
field: web-development
product: fastify
tags: [fastify, validation, json-schema, ajv, add-schema]
level: practitioner
status: docs-checked
description: "Validate body, querystring, params and headers with JSON Schema and share schemas with addSchema and $ref."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Validation-and-Serialization.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Getting-Started.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Validation uses Ajv v8; serialization uses fast-json-stringify; the two share only schemas added via `addSchema`. Supported parts: `body` (POST, PUT, PATCH), `querystring` (or `query`), `params`, `headers`. With the default validator, v5 requires a full JSON Schema including `type` for `querystring`, `params`, `body` and `response` (the `jsonShortHand` option was removed):

```js
const opts = {
  schema: {
    querystring: {
      type: 'object',
      properties: { name: { type: 'string' } },
      required: ['name']
    },
    params: {
      type: 'object',
      properties: { id: { type: 'integer' } }
    },
    headers: {
      type: 'object',
      properties: { 'x-foo': { type: 'string' } },
      required: ['x-foo']
    }
  }
}
fastify.get('/items/:id', opts, handler)
```

Node exposes header names in lowercase, and Fastify lowercases header names in a `headers` schema before compilation. Regular-expression constraints (`patternProperties` keys, `propertyNames` `pattern`) are not rewritten; write them to match lowercase.

Shared schemas: `fastify.addSchema({ $id: 'commonSchema', type: 'object', properties: {...} })` (encapsulated), then reference with `{ $ref: 'commonSchema#' }`, or a sub-part such as `{ $ref: 'http://fastify.example#/properties/hello' }`. `getSchemas()` returns the schemas visible in the current scope and `getSchema(id)` returns one. The non-standard `replace-way` form was removed in v3 in favour of `$ref`.

Validation is only attempted for `application/json` bodies unless the body schema uses `content` keyed by media type (`'application/json': { schema }`, `'text/plain': { schema }`); other content types are not validated, and the match is exact on the essence MIME type.

Schemas are application code: validation uses `new Function()`, so never use user-provided schemas. `$async` Ajv schemas should not be used for initial validation (DoS risk); do async work in `preHandler`.

Gotcha: an external `$ref` in a headers schema is not reached by header case normalization (warning FSTSEC002); inline the header schema instead.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Validation-and-Serialization.md, Getting-Started.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
