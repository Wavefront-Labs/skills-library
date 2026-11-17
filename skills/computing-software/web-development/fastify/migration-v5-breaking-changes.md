---
id: computing-software.web-development.fastify.migration-v5-breaking-changes
name: migration-v5-breaking-changes
category: computing-software
field: web-development
product: fastify
tags: [fastify, migration, v5, breaking-changes, upgrade]
level: advanced
status: docs-checked
description: "Checklist of Fastify v4 to v5 breaking changes with before and after code."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fix all v4 deprecation warnings first: all v4 deprecations were removed in v5. Requires Node.js 20+. The guide says v4 is supported until June 30, 2025.

Breaking changes:
- Full JSON Schema required for `querystring`, `params`, `body`, `response` (include `type: 'object'` and `properties`); `jsonShortHand` removed.
- `logger` no longer takes an instance: use `loggerInstance`.
- `useSemicolonDelimiter` now defaults to false.
- `request.params` has no prototype: `Object.hasOwn(req.params, 'name')`.
- Type providers split into `validator` and `serializer` types.
- `listen()` variadic form removed: `fastify.listen({ port: 8000 })`.
- Trailers: use async functions or callbacks in `reply.trailer`.
- `request.context`, `routeSchema`, `routeConfig`, `routerPath`, `routerMethod` and `reply.context` removed: use `request.routeOptions` (`config`, `schema`, `url`, `method`).
- `reply.redirect(url, code)`: `reply.redirect('/new-route', 301)`.
- `reply.sent = true` forbidden: use `reply.hijack()`.
- Route versioning: `constraints: { version }` replaces `version` and `versioning` (FSTDEP008/009).
- Custom HEAD must be defined before the GET, or set `exposeHeadRoutes: false`.
- `request.connection` becomes `request.socket`; `reply.getResponseTime()` becomes `reply.elapsedTime`.
- `hasRoute()` needs the route as defined; `getDefaultRoute`/`setDefaultRoute` removed.
- Removed methods PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK, TRACE, SEARCH: re-add with `addHttpMethod`.
- Reference types in `decorateRequest`/`decorateReply` are forbidden.
- DELETE with JSON content type and empty body no longer allowed; plugins cannot mix async and callbacks.
- `request.hostname` excludes port; `host` and `port` added.
- Ajv formats `time` and `date-time` require a timezone (`iso-time` and `iso-date-time` accept an optional timezone).

New: diagnostics channel support.

Gotcha: `useSemicolonDelimiter` is false by default in v5, so semicolon delimiters in the query string stop working unless you set `useSemicolonDelimiter: true`.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Migration-Guide-V5.md) and confirmed. Removed or corrected: the claim that the semicolon change is silent and the statement that v4 support ended (the guide says supported until 2025-06-30); the invented Verify step.

Method: documentation only; no commands were run.
