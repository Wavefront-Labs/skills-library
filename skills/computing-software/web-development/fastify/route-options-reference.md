---
id: computing-software.web-development.fastify.route-options-reference
name: route-options-reference
category: computing-software
field: web-development
product: fastify
tags: [fastify, routes, options, schema, reference]
level: practitioner
status: docs-checked
description: "Complete list of route options accepted by fastify.route and the shorthand methods."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Routes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Full declaration: `fastify.route({ method, url, ... })`. Shorthands: `get`, `head`, `post`, `put`, `delete`, `options`, `patch`, `query`, `all`.

Options:
- `method`: `GET`, `HEAD`, `TRACE`, `DELETE`, `OPTIONS`, `PATCH`, `PUT`, `POST` and `QUERY`; more need `addHttpMethod`. Can be an array.
- `url` (alias `path`).
- `schema`: `body` (validated for POST, PUT, PATCH, TRACE, SEARCH, PROPFIND, PROPPATCH, LOCK or QUERY), `querystring` (alias `query`), `params`, `response` (setting a response schema allows 10-20% more throughput).
- `exposeHeadRoute`: creates a sibling HEAD route for GET routes; defaults to the `exposeHeadRoutes` instance option. To use a custom HEAD handler, define it before the GET route.
- `attachValidation`: on a schema validation error, attach `validationError` to the request instead of sending the error to the error handler.
- Hooks: `onRequest`, `preParsing`, `preValidation`, `preHandler`, `preSerialization`, `onSend`, `onResponse`, `onTimeout`, `onError`; each may be an array.
- `handler(request, reply)`: Fastify server bound to `this` (arrow functions break this).
- `errorHandler(error, request, reply)`, `childLoggerFactory`, `validatorCompiler`, `serializerCompiler`, `schemaErrorFormatter`: per-route overrides of the global ones.
- `bodyLimit`: integer, bytes; defaults to `1048576` (1 MiB).
- `handlerTimeout`: max milliseconds for the route's full lifecycle, positive integer; on timeout `request.signal` is aborted and a 503 is sent through the error handler.
- `logLevel` (an invalid level throws `FST_ERR_ROUTE_LOG_LEVEL_INVALID` at registration), `logSerializers`.
- `config`: object for custom configuration, read in the handler via `reply.routeOptions.config`.
- `version` / `constraints`: constraints include built-in `version` and `host`.
- `prefixTrailingSlash`: `both` (default), `slash` or `no-slash`; does not override `ignoreTrailingSlash`.

```js
fastify.get('/ping', { logLevel: 'warn', config: { public: true } }, async () => 'pong')
```

Gotcha: supplying the handler both inside the options object and as the third argument throws a duplicate-handler error.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Routes.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
