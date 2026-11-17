---
id: computing-software.web-development.fastify.server-logger-options
name: server-logger-options
category: computing-software
field: web-development
product: fastify
tags: [fastify, server, logging, pino, logger]
level: practitioner
status: docs-checked
description: "Enable the built-in pino logger with logger options or supply your own instance with loggerInstance."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Logging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`logger` defaults to `false` (disabled; logging methods point to a null abstract-logging instance). Pass `true` for defaults or a pino options object, which goes to the Pino constructor; if missing, `level` is set to `'info'` and serializers for `req`, `res` and `err` are added (a user-supplied serializer overrides the default for that property).

```js
const fastify = require('fastify')({
  logger: { level: 'info', redact: ['req.headers.authorization'] }
})
```

To use your own logger, v5 requires the separate `loggerInstance` option; `logger` no longer accepts an instance.

```js
const loggerInstance = require('pino')()
const fastify = require('fastify')({ loggerInstance })
```

`loggerInstance` (default `null`) must be a Pino instance or conform to the Pino interface with the methods `info`, `error`, `debug`, `fatal`, `warn`, `trace` and `child`.

Pretty output in development only:

```js
logger: { transport: { target: 'pino-pretty' } }
```

`pino-pretty` must be installed as a dev dependency; it is not included. The logger options also accept `file: '/path/to/file'` (uses pino.destination()) and a `stream` field for a custom stream.

Inside handlers use `request.log` (carries the request id); elsewhere `fastify.log`.

Gotcha: passing a logger object created elsewhere to `logger` is the v4 style and now fails; move it to `loggerInstance`. See also `logController` for request-logging behavior.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Server.md, Logging.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
