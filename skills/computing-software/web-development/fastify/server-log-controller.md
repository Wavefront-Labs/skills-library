---
id: computing-software.web-development.fastify.server-log-controller
name: server-log-controller
category: computing-software
field: web-development
product: fastify
tags: [fastify, server, logging, log-controller, customization]
level: advanced
status: docs-checked
description: "Customize request logging by subclassing the LogController class passed through the logController option."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`logController` (default `undefined`) accepts an instance of `LogController` (or a subclass) to customize Fastify's internal log lines. The class is exported from `fastify`; override only the methods you want to change, all others keep their default behavior. An invalid value raises `FST_ERR_LOG_INVALID_LOG_CONTROLLER`.

The constructor takes an optional options object:
- `disableRequestLogging`: `boolean | (req) => boolean`, default `false`; when `true` (or the function returns `true`) per-request log lines are suppressed.
- `requestIdLogLabel`: string, default `'reqId'`; the label for the request identifier.

Methods and signatures:
- `isLogDisabled(request)`: checks whether request logging is disabled; it impacts all other log methods.
- `incomingRequest(request, reply, metadata)`: `info` level.
- `requestCompleted(error, request, reply, metadata)`: `error` level when an error is present, `info` otherwise.
- `defaultErrorLog(error, request, reply, metadata)`: `error` for 5xx, `info` for 4xx.
- `streamError(error, request, reply, metadata)`: stream errors after headers were sent.
- `routeNotFound(request, reply, metadata)`: `info` level.
- `writeHeadError(error, request, reply, metadata)`: warning when `writeHead` fails during error handling.
- `serializerError(error, request, reply, metadata)`: `metadata.statusCode` holds the triggering status code.
- `serviceUnavailable(logger, server)`: logs a 503 while closing; always emitted, not gated by `disableRequestLogging`.

```js
const { LogController } = require('fastify')

class MyLogController extends LogController {
  constructor () {
    super({
      requestIdLogLabel: 'traceId',
      disableRequestLogging: (request) => request.url === '/health'
    })
  }

  incomingRequest (request, reply, metadata) {
    request.log.debug({ req: request }, 'incoming request')
  }
}

const fastify = require('fastify')({
  logger: true,
  logController: new MyLogController()
})
```

Gotcha: when you override a method you take full control of it; the default `disableRequestLogging` check is not applied automatically. For conditional logging call `this.isLogDisabled(request)` yourself or override `isLogDisabled` too.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Server.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
