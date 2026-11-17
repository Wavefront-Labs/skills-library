---
id: computing-software.web-development.fastify.migration-v4-and-v3
name: migration-v4-and-v3
category: computing-software
field: web-development
product: fastify
tags: [fastify, migration, v4, v3, upgrade]
level: advanced
status: docs-checked
description: "Key breaking changes for v3 to v4 and v2 to v3, including codemods."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V4.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V3.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fastify v4 (from v3), codemod recipe: `npx codemod@latest fastify/4/migration-recipe` (runs remove-app-use, reply-raw-access, wrap-routes-plugin, await-register-calls).

- Error handling composition: an error thrown in an async error handler goes to the upper-level handler; the root handler is Fastify's default.
- `app.use()` removed; use `@fastify/middie` or `@fastify/express`.
- `reply.res` becomes `reply.raw`.
- `return reply` is required to signal a forked promise chain.
- `exposeHeadRoutes` defaults to true.
- Route registration is synchronous: wrap routes in a plugin or `await fastify.register(...)` when using `onRoute`.
- Optional params must be explicit: `/posts/:id?`.
- Ajv v8 prohibits `type` keywords with multiple types other than `null`: use `anyOf` instead of `type: ['object','array']`.
- Variadic `listen()` deprecated; trailers added.

Fastify v3 (from v2):
- Middleware no longer built in.
- Log serializers receive Fastify Request/Reply (use `reply.raw.customProp`).
- Shared schema string substitution replaced by `$ref`: `body: { $ref: 'schemaId#' }`.
- `setSchemaCompiler`/`setSchemaResolver` replaced by `setValidatorCompiler`.
- `preParsing` signature `(request, reply, payload, done)`; return a stream with `receivedEncodedLength`.
- `onRoute`/`onRegister` are encapsulated.
- Content type parsers: `(request, payload, done)`.
- TypeScript generics: `{ Querystring, Params, Headers, Body }`.
- Thrown errors in sync handlers now reach `setErrorHandler`.
- Added `connectionTimeout`, `keepAliveTimeout` and async-await plugin support; `request.req` / `reply.res` deprecated for `request.raw` / `reply.raw`; removed `modifyCoreObjects`.

Gotcha: in v4 a route that relied on an implicitly optional parameter returns 404 until the parameter is declared explicitly (`/posts/:id?`).

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Migration-Guide-V4.md, Migration-Guide-V3.md) and confirmed. Removed or corrected: the claim that missing optional parameters 404 silently, the claim that raw access was added in v3 (it was a deprecation of req/res), and the invented Verify step with NODE_OPTIONS.

Method: documentation only; no commands were run.
