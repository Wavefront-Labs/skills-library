---
id: computing-software.web-development.fastify.server-bodylimit-and-poisoning
name: server-bodylimit-and-poisoning
category: computing-software
field: web-development
product: fastify
tags: [fastify, server, body-limit, security, prototype-poisoning]
level: practitioner
status: docs-checked
description: "Set bodyLimit globally or per route and choose onProtoPoisoning and onConstructorPoisoning behavior."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Routes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`bodyLimit` defaults to 1048576 bytes (1 MiB). The default body reader replies with `FST_ERR_CTP_BODY_TOO_LARGE` if the body exceeds it. Routes accept a `bodyLimit` option and custom content type parsers accept a `bodyLimit` option too.

```js
const fastify = require('fastify')({ bodyLimit: 2 * 1024 * 1024 })

fastify.post('/upload', { bodyLimit: 10 * 1024 * 1024 }, handler)
```

JSON parsing guards against prototype poisoning (via secure-json-parse) for objects with `__proto__` or `constructor`:

- `onProtoPoisoning`: default `'error'`; also `'remove'` (strip the key) or `'ignore'`.
- `onConstructorPoisoning`: default `'error'`; also `'remove'` or `'ignore'`.

```js
const fastify = require('fastify')({
  onProtoPoisoning: 'remove',
  onConstructorPoisoning: 'remove'
})
```

Note: in `getDefaultJsonParser` the value `'ignore'` skips all validations, similar to calling `JSON.parse()` directly. The two arguments of `fastify.getDefaultJsonParser(onProtoPoisoning, onConstructorPoisoning)` take `'ignore'`, `'remove'` or `'error'`.

If a `preParsing` hook is provided, `bodyLimit` applies to the size of the stream the hook returns (the "decoded" body).

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Server.md, Routes.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
