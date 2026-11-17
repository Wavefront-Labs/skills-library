---
id: computing-software.web-development.fastify.http2-and-https
name: http2-and-https
category: computing-software
field: web-development
product: fastify
tags: [fastify, http2, https, tls, server]
level: practitioner
status: docs-checked
description: "Run Fastify over HTTPS, secure HTTP/2 with allowHTTP1, or plaintext h2c."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/HTTP2.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/TypeScript.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
HTTPS:

```js
const fs = require('node:fs')
const fastify = require('fastify')({
  https: {
    key: fs.readFileSync('/path/to/key.pem'),
    cert: fs.readFileSync('/path/to/cert.pem')
  }
})
```

Secure HTTP/2 needs `http2: true` plus `https`; `allowHTTP1: true` falls back for clients that do not speak h2:

```js
const fastify = require('fastify')({
  http2: true,
  https: {
    allowHTTP1: true,
    key: fs.readFileSync('/path/to/key.pem'),
    cert: fs.readFileSync('/path/to/cert.pem')
  }
})
```

Omit `https` for plaintext HTTP/2 (h2c), for microservices: `fastify({ http2: true })`. Test with `npx h2url https://localhost:3000` (secure) or `npx h2url http://localhost:3000` (plain). ALPN negotiation lets HTTPS and HTTP/2 share one socket.

Generate a dev cert: `openssl genrsa -out key.pem`, then `openssl req -new -key key.pem -out csr.pem`, then `openssl x509 -req -days 9999 -in csr.pem -signkey key.pem -out cert.pem`. (TypeScript docs; they test the HTTPS server with `curl -k https://localhost:8080`.)

Notes: `keepAliveTimeout` does not apply to HTTP/2; use `http2SessionTimeout` (default 72000). TypeScript raw types switch to `Http2ServerRequest` / `Http2ServerResponse`.

Gotcha: HTTP/2 is supported in browsers only over a secure connection, so plaintext h2c is not usable from browsers. None of the HTTP/2-specific APIs are exposed by Fastify; Node's `req` and `res` are reachable through Request and Reply.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (HTTP2.md, TypeScript.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
