---
id: computing-software.web-development.fastify.server-connection-timeouts
name: server-connection-timeouts
category: computing-software
field: web-development
product: fastify
tags: [fastify, server, timeouts, keep-alive, http]
level: practitioner
status: docs-checked
description: "Factory options for connectionTimeout, keepAliveTimeout, requestTimeout, maxRequestsPerSocket and forceCloseConnections."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Socket-level limits set in the `fastify({...})` factory:

- `connectionTimeout`: default 0 (no timeout). Sets the server timeout in milliseconds (Node `server.timeout`).
- `keepAliveTimeout`: default 72000 ms. Applies only when HTTP/1 is in use; for HTTP/2 the separate `http2SessionTimeout` option (default 72000) closes sessions on timeout.
- `maxRequestsPerSocket`: default 0 (no limit). Maximum requests a socket handles before the keep-alive connection is closed; HTTP/1.1 only.
- `requestTimeout`: default 0 (no limit). Maximum milliseconds for receiving the entire request from the client. Must be set to a non-zero value (for example 120 seconds) to protect against denial-of-service attacks when the server runs without a reverse proxy in front.
- `connectionTimeout`, `keepAliveTimeout`, `maxRequestsPerSocket` and `requestTimeout` are ignored when `serverFactory` is given.
- `forceCloseConnections`: default `'idle'` when the Node.js version supports `server.closeIdleConnections`, otherwise `false`. `true` destroys all persistent connections on close; `'idle'` closes only idle ones.

```js
const fastify = require('fastify')({
  connectionTimeout: 30000,
  keepAliveTimeout: 72000,
  requestTimeout: 120000,
  forceCloseConnections: 'idle'
})
```

Gotcha: `'idle'` is only supported if the HTTP server has `closeIdleConnections`; otherwise attempting to set it throws (`FST_ERR_FORCE_CLOSE_CONNECTIONS_IDLE_NOT_AVAILABLE`). With `false`, nothing is forced and idle connections stay open until they time out naturally (see `keepAliveTimeout`). `true` does not inspect connections to see whether requests have completed, and with HTTP/2 it also closes all active sessions (since Node.js v24 active sessions are closed by default).

`connectionTimeout` and `requestTimeout` operate at the socket level; `handlerTimeout` is the application-level timeout.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Server.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
