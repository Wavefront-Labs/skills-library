---
id: computing-software.web-development.fastify.type-providers
name: type-providers
category: computing-software
field: web-development
product: fastify
tags: [fastify, typescript, type-providers, typebox, zod]
level: advanced
status: docs-checked
description: "Infer request types from schemas with json-schema-to-ts, TypeBox or Zod providers and scope them per plugin."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Type-Providers.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Write-Type-Provider.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Type providers infer `request.query`, `body` and so on from inline schemas. Packages: `@fastify/type-provider-json-schema-to-ts`, `@fastify/type-provider-typebox`, `@fastify/type-provider-zod`.

```ts
import Fastify from 'fastify'
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox'
import { Type } from 'typebox'

const server = Fastify().withTypeProvider<TypeBoxTypeProvider>()
server.get('/route', {
  schema: { querystring: Type.Object({ foo: Type.Number(), bar: Type.String() }) }
}, (request) => {
  const { foo, bar } = request.query   // typed
})
```

Zod (`import { z } from 'zod/v4'`; `ZodTypeProvider`, `validatorCompiler`, `serializerCompiler` come from `@fastify/type-provider-zod`):

```ts
server.setValidatorCompiler(validatorCompiler)
server.setSerializerCompiler(serializerCompiler)
server.withTypeProvider<ZodTypeProvider>().get('/route', {
  schema: { querystring: z.object({ foo: z.number(), bar: z.string() }) }
}, (request) => { const { foo, bar } = request.query })
```

json-schema-to-ts needs literal types: if you move a schema into a variable, add `as const`.

Provider types do not propagate globally: call `withTypeProvider` again inside each plugin, or type modules with `FastifyInstance<RawServerDefault, RawRequestDefaultExpression<RawServerDefault>, RawReplyDefaultExpression<RawServerDefault>, FastifyBaseLogger, TypeBoxTypeProvider>`.

Writing a provider (Write-Type-Provider guide): reduce types only up to `unknown`, never `never`, in the `validator` and `serializer` members of your `FastifyTypeProvider` interface, because some `FastifyInstance` methods are contravariant on `TypeProvider` and the provider must be substitutable with `FastifyTypeProviderDefault`.

Gotcha: forgetting `as const` makes `type: 'object'` widen to `string` and inference collapses.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Type-Providers.md, Write-Type-Provider.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
