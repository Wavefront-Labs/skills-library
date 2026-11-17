---
id: computing-software.web-development.fastify.request-object-properties
name: request-object-properties
category: computing-software
field: web-development
product: fastify
tags: [fastify, request, properties, ip, headers]
level: practitioner
status: docs-checked
description: "Reference of Fastify request properties and the v5 host, hostname and port split."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Request.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Properties: `body`, `query`, `params`, `headers`, `id`, `log`, `method`, `url`, `originalUrl`, `routeOptions`, `server`, `raw`, `ip`, `ips`, `host`, `hostname`, `port`, `protocol`, `mediaType`, `signal`, `socket`, `is404`, `validationError`.

```js
fastify.get('/', (request) => ({
  id: request.id,
  host: request.host,         // v4's hostname: 'localhost:3000'
  hostname: request.hostname, // 'localhost'
  port: request.port,         // 3000
  route: request.routeOptions.url
}))
```

Notes:
- `ip` comes from `socket.remoteAddress` (or `X-Forwarded-For` with `trustProxy`) and is `undefined` without a socket. `ips` is the `X-Forwarded-For` array (closest to furthest) and is `undefined` unless `trustProxy` is enabled. `host` uses `X-Forwarded-Host` with `trustProxy` (or `:authority` on HTTP/2). `protocol` comes from `socket.encrypted` (or `X-Forwarded-Proto` with `trustProxy`).
- `hostname` and `port` are parsed from `request.host`; `port` is `null` when the host has no port, and IPv6 hostnames keep their brackets.
- `request.headers` is a getter and an additive setter (it cannot remove headers); standard headers stay on `request.raw.headers`. Schema validation may mutate these header objects.
- `request.routeOptions` includes `bodyLimit`, `handlerTimeout`, `config`, `method`, `url`, `handler`, `attachValidation`, `logLevel`, `schema`, `version`, `exposeHeadRoute`, `prefixTrailingSlash`. In v5 the deprecated `request.context`, `routeSchema`, `routeConfig`, `routerPath`, `routerMethod` were removed in favour of it.
- `request.connection` was removed; use `request.socket`.
- `originalUrl` keeps the original url after internal re-routing; `mediaType` is `undefined` without a Content-Type.
- Methods: `getDecorator(name)`, `setDecorator(name, value)` (both throw `FST_ERR_DEC_UNDECLARED` for undeclared decorators), `getValidationFunction(schema | httpPart)`, `compileValidationSchema(schema, [httpPart])`, `validateInput(data, [schema | httpPart], [httpPart])` (httpPart wins if both are given).
- `params`, `query`, `headers`, `body`, `ip`, `host` and similar are untrusted input; params are percent-decoded (`..%2ffile` becomes `../file`).

Gotcha: in v5 `request.hostname` no longer includes the port; code relying on it must switch to `request.host`.

`is404` is true when the 404 handler is handling the request. `validationError` is set only when the route has `attachValidation` enabled and validation fails; Fastify then calls the handler instead of replying 400.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Request.md, Migration-Guide-V5.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
