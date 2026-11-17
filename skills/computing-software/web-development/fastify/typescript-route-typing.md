---
id: computing-software.web-development.fastify.typescript-route-typing
name: typescript-route-typing
category: computing-software
field: web-development
product: fastify
tags: [fastify, typescript, generics, routes, declaration-merging]
level: practitioner
status: docs-checked
description: "Type routes with the Body, Querystring, Params, Headers and Reply generics, plus plugin and decorator typing."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/TypeScript.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V3.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: install `@types/node`; set `target` in tsconfig.json to `es2017` or greater to avoid a FastifyDeprecation warning.

Route generics (v3+ object form):

```ts
server.get<{
  Querystring: { name: string }
  Params: { id: number }
  Headers: { 'x-foo': string }
  Body: { a: string }
  Reply: { 200: { ok: boolean }, 404: { error: string } }
}>('/x/:id', async (request, reply) => {
  reply.code(404).send({ error: 'nope' })   // narrowed by status
  return { ok: true }
})
```

Types can come from schemas: TypeBox `Static<typeof T>`, `json-schema-to-typescript` (`json2ts -i schemas -o types`), or json-schema-to-ts `FromSchema` (needs `as const`).

Plugins: use `FastifyPluginCallback<Opts>` or `FastifyPluginAsync<Opts>`; export with `fp(...)`. Decorators need declaration merging on the interfaces:

```ts
declare module 'fastify' {
  interface FastifyRequest { someProp: string }
  interface FastifyReply { someReplyProp: string }
}
```

`fastify.getDecorator<T>(name)`, `request.getDecorator<T>(name)`, `reply.getDecorator<T>(name)` and `req.setDecorator<T>(name, value)` give typed access (functions from getDecorator come with `this` already bound). `FastifyRegisterOptions` is the `Options` generic intersected with optional `prefix: string` and `logLevel`. Omitted generic properties of `RequestGenericInterface` (Body, Querystring, Params, Headers) default to `unknown`.

Vanilla JS gets typing with JSDoc: `@type {import('fastify').FastifyInstance}`.

Gotcha: declaration merging is not smart: a plugin's types are included whenever its type definition is in scope, even if the plugin is unused. `require` does not load type definitions; use `import plugin from 'plugin'` (or `import 'plugin'`) before `fastify.register(require('plugin'))`.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (TypeScript.md, Migration-Guide-V3.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
