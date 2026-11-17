---
id: computing-software.web-development.fastify.schema-controller-buckets
name: schema-controller-buckets
category: computing-software
field: web-development
product: fastify
tags: [fastify, schema, schema-controller, ajv, compilers]
level: sme
status: docs-checked
description: "Customize how schemas are stored and compiled with the schemaController option, bucket and compilersFactory."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`schemaController` (factory option) fully manages where schemas are stored (`bucket`) and which module compiles them (`compilersFactory`). It is useful when your schemas live in a data structure unknown to Fastify, or to tweak all schema processing, e.g. Ajv v8 JTD or Standalone mode (see the `@fastify/ajv-compiler` docs).

- `bucket`: a factory `function (parentSchemas) => ({ add, getSchema, getSchemas })`, called whenever `fastify.register()` is called. `add(inputSchema)` runs on `fastify.addSchema()`; `getSchema(schema$id)` runs on `fastify.getSchema(id)` and returns the raw schema; `getSchemas()` must return an object mapping each schema `$id` to its raw JSON Schema, including all schemas referenced by route `$ref`s. `parentSchemas` are the schemas of the parent context, which `getSchemas()` should return.
- `compilersFactory`: `{ buildValidator(externalSchemas, ajvServerOption), buildSerializer(externalSchemas, serializerOptsServerOption) }`. Each is called when a new validator or serializer instance is needed (on `register()` only if new schemas were added in that encapsulation context). `buildValidator` returns a validator compiler `({ schema, method, url, httpPart })`; `buildSerializer` returns a serializer compiler `({ schema, method, url, httpStatus, contentType })`. `externalSchemas` come from `bucket.getSchemas()` and resolve external `$ref`s.

```js
const fastify = require('fastify')({
  schemaController: {
    bucket: (parent) => {
      const store = new Map(Object.entries(parent || {}))
      return {
        add (schema) { store.set(schema.$id, schema) },
        getSchema (id) { return store.get(id) },
        getSchemas () { return Object.fromEntries(store) }
      }
    },
    compilersFactory: {
      buildValidator (externalSchemas, ajvServerOption) {
        const ajv = new Ajv(ajvServerOption.customOptions)
        return ({ schema }) => ajv.compile(schema)
      },
      buildSerializer () {
        return () => (data) => JSON.stringify(data)
      }
    }
  }
})
```

`addSchema` is encapsulated, and `getSchemas()` returns the schemas visible in the selected scope.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Server.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
