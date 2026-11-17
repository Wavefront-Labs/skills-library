---
id: computing-software.web-development.fastify.error-handling-set-error-handler
name: error-handling-set-error-handler
category: computing-software
field: web-development
product: fastify
tags: [fastify, errors, error-handler, set-error-handler, security]
level: practitioner
status: docs-checked
description: "Understand the default error response, set a scoped error handler, and know what it does not catch."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Errors.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V4.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default response for a thrown error: `{ statusCode, error, message, code? }`. `message` is verbatim, so internal details can leak; sanitize in a handler:

```js
fastify.setErrorHandler(function (error, request, reply) {
  request.log.error(error)
  const status = error.statusCode >= 400 ? error.statusCode : 500
  reply.code(status).send({ error: status >= 500 ? 'Internal Server Error' : error.message })
})
```

Rules:
- If the error `statusCode` is below 400, Fastify sets it to 500 before calling the handler. The handler is bound to the Fastify instance (`this.log`) and async is supported.
- Handlers are encapsulated per plugin; the error goes to the most precedent handler in its context, and the root handler is Fastify's generic one (it uses headers and status code on the Error). Throwing a new error inside a custom handler calls the parent handler; `onError` fires once for the first error.
- Headers and status code are not automatically set from the error when a custom handler is used.
- If a plugin's handler re-throws a non-Error (e.g. `throw 'foo'`), it does not propagate to the parent handler; the default handler catches it. Throw `new Error(...)`.
- It does NOT catch errors from `onResponse` hooks, 404s (use `setNotFoundHandler`) or stream errors after headers were sent.

404s: `setNotFoundHandler` is encapsulated by prefix and accepts `preValidation`/`preHandler` hooks; the handler goes through the full lifecycle.

Errors Fastify raises for invalid requests (validation, body too large, invalid media type, bad JSON...) carry no stack trace. A route response schema declaring `stack` would serialize it.

Gotcha: `allowErrorHandlerOverride` (default `false`) prevents calling `setErrorHandler` twice in one scope (FST_ERR_ERROR_HANDLER_ALREADY_SET).

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Errors.md, Server.md, Migration-Guide-V4.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
