---
id: computing-software.web-development.fastify.error-codes-reference
name: error-codes-reference
category: computing-software
field: web-development
product: fastify
tags: [fastify, errors, error-codes, fst-err, reference]
level: practitioner
status: docs-checked
description: "Look up common FST_ERR codes and read them from fastify.errorCodes."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Errors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The full table of Fastify error codes is in Errors.md (Fastify Error Codes). Commonly met:

- `FST_ERR_VALIDATION`: the request failed payload validation.
- `FST_ERR_CTP_BODY_TOO_LARGE`: body larger than the limit; raise `bodyLimit`.
- `FST_ERR_CTP_INVALID_MEDIA_TYPE`: unsupported or invalid content type (415 per ContentTypeParser.md).
- `FST_ERR_DEC_REFERENCE_TYPE`: the decorator cannot be a reference type; use a getter/setter interface or an empty decorator with a hook.
- `FST_ERR_DEC_UNDECLARED`: a decorator that has not been declared was accessed.
- `FST_ERR_ROUTE_METHOD_ALREADY_SUPPORTED`: the HTTP method is already supported; pass `{ overrideExisting: true }`.
- `FST_ERR_ROUTE_LOG_LEVEL_INVALID`: route `logLevel` must match a configured logger level.
- `FST_ERR_HANDLER_TIMEOUT`: request timed out; increase `handlerTimeout` or optimize the handler.
- `FST_ERR_FORCE_CLOSE_CONNECTIONS_IDLE_NOT_AVAILABLE`: `forceCloseConnections: 'idle'` set but the HTTP server lacks `closeIdleConnections`.
- `FST_ERR_BAD_STATUS_CODE`: the status code is not valid.
- `FST_ERR_MISSING_CONTENTTYPE_SERIALIZATION_FN`: missing `Content-Type` serialization function.
- `FST_ERR_BAD_URL`: router received an invalid URL. `FST_ERR_ASYNC_CONSTRAINT`: router error with asynchronous constraints.
- `FST_ERR_ERROR_HANDLER_NOT_FN` / `FST_ERR_ERROR_HANDLER_ALREADY_SET`: `setErrorHandler` given a non-function / called twice in a scope without `allowErrorHandlerOverride: true`.

Access them via `errorCodes` (`import { errorCodes } from 'fastify'` or `require('fastify').errorCodes`) and match with `instanceof`:

```js
const { errorCodes } = require('fastify')
fastify.setErrorHandler((err, req, reply) => {
  if (err instanceof errorCodes.FST_ERR_BAD_STATUS_CODE) { /* ... */ }
  reply.send(err)
})
```

Errors Fastify creates for rejected invalid requests (validation, body too large, invalid media type, empty/invalid JSON body, bad URL, max param length, missing route content type) have no stack trace.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Errors.md) and confirmed. Removed or corrected: the claim that all Fastify errors carry a FST_ERR_ code; the invented Verify step.

Method: documentation only; no commands were run.
