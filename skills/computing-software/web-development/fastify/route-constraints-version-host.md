---
id: computing-software.web-development.fastify.route-constraints-version-host
name: route-constraints-version-host
category: computing-software
field: web-development
product: fastify
tags: [fastify, routes, constraints, versioning, host]
level: advanced
status: docs-checked
description: "Route on Accept-Version or Host with constraints, and add custom constraint strategies carefully."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Routes.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Constraints let the same path map to different handlers.

Version (Accept-Version header, exact semver):

```js
fastify.route({
  method: 'GET', url: '/',
  constraints: { version: '1.2.0' },
  handler: (req, reply) => reply.send({ hello: 'v1' })
})
```

Fastify requires an `Accept-Version` header when the route has a version, and prefers a versioned route to a non-versioned one for the same path. Advanced ranges and pre-releases are not supported. The header may be `1.x`, `1.2.0` or `1.2.x`; if several versions share a major or minor, the highest compatible one is chosen. With no `Accept-Version` header the result is a 404. Set a `Vary` header on responses with the versioning header (e.g. `Accept-Version`) to prevent cache poisoning (or do it in a proxy/CDN).

Host (string for exact match, or RegExp):

```js
fastify.route({
  method: 'GET', url: '/',
  constraints: { host: /.*\.fastify\.example/ },
  handler: (req, reply) => reply.send('hello world from ' + req.headers.host)
})
```

A non-matching `Host` gives a 404.

Custom strategies are objects with `name`, `storage`, `deriveConstraint(req, ctx, done)` and optional `mustMatchWhenDerived`. Asynchronous custom constraints are a last resort (they impact router performance); avoid returning errors from the callback, or provide a `frameworkErrors` handler that checks `Fastify.errorCodes.FST_ERR_ASYNC_CONSTRAINT`.

Migration (v5): the `version` route option and `versioning` server option were removed; use `constraints: { version }` (FSTDEP008/009).

Gotcha: version constraints can degrade router performance.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Routes.md, Migration-Guide-V5.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
