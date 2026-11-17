---
id: computing-software.web-development.fastify.server-request-id-options
name: server-request-id-options
category: computing-software
field: web-development
product: fastify
tags: [fastify, server, request-id, logging, tracing]
level: practitioner
status: docs-checked
description: "Configure requestIdHeader, requestIdLogLabel and genReqId to control the id attached to each request and log line."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each request gets `request.id` (logged as `reqId`). Options:

- `requestIdHeader`: `false` (default) uses `genReqId` immediately; `true` reads the `request-id` header; a non-empty string uses that header name; an empty string `""` sets it to `false`.
- `genReqId(rawReq)`: receives the raw incoming request and generates the id; it is expected to be error-free and is not called if the `requestIdHeader` header is present. Default: the `request-id` header value if provided, or monotonically increasing integers.
- `requestIdLogLabel` (a `logController` constructor option, default `'reqId'`): rename the log field.

```js
const fastify = require('fastify')({
  logger: true,
  requestIdHeader: 'x-request-id',
  genReqId (req) {
    return crypto.randomUUID()
  }
})
```

Gotcha: enabling `requestIdHeader` allows any caller to set `reqId` to a value of their choosing; no validation is performed on it.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Server.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
