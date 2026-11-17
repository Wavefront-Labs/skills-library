---
id: computing-software.web-development.fastify.logging-redaction-serializers
name: logging-redaction-serializers
category: computing-software
field: web-development
product: fastify
tags: [fastify, logging, pino, redact, serializers]
level: practitioner
status: docs-checked
description: "Configure log level, redaction, custom serializers and child logger factories safely."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Logging.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V3.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable with `logger: true` or an options object (pino options, plus `file` and `stream`). Logging is disabled by default and cannot be enabled at runtime if it was off. Default level is `'info'`. Use `request.log` inside handlers and `fastify.log` outside them.

Redact secrets:

```js
const fastify = require('fastify')({
  logger: {
    level: 'info',
    redact: ['req.headers.authorization'],
    serializers: {
      req (request) {
        return { method: request.method, url: request.url, host: request.host }
      }
    }
  }
})
```

Serializer rules:
- The default serializers handle objects with `req`, `res` and `err` properties; `req` is the Fastify Request and `res` the Fastify Reply (V3 migration guide: since v3). Use `reply.raw.customProp` for properties on the raw response.
- The body is not available in the `req` serializer (it is not parsed yet); log it from a `preHandler` hook.
- The Reply passed to a `res` serializer cannot always be fully constructed: check that properties other than `statusCode` exist (for example `typeof reply.getHeaders === 'function'`) before using them.
- Serializers must never throw: that can cause the Node.js process to exit.

Per-route: `logLevel` and `logSerializers` route options. Per-plugin: `register(plugin, { logLevel: 'warn' })`.

Child logger customization: `fastify.setChildLoggerFactory(factory(logger, bindings, opts, rawReq))` (called per request, `this` is the Fastify instance) or the `childLoggerFactory` server option. Custom logger: pass a Pino-compatible `loggerInstance` (methods info, error, debug, fatal, warn, trace, silent, child; property `level`). Non-Pino loggers ignore `serializers`.

Pretty logs: `transport: { target: 'pino-pretty' }` with pino-pretty as a dev dependency only.

Gotcha: logging response headers can expose authentication data; use redaction. Enabling `requestIdHeader` lets callers set `reqId` to any value, unvalidated.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Logging.md, Migration-Guide-V3.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
