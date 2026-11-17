---
id: computing-software.web-development.fastify.reply-status-headers-redirect
name: reply-status-headers-redirect
category: computing-software
field: web-development
product: fastify
tags: [fastify, reply, headers, status, redirect]
level: practitioner
status: docs-checked
description: "Set status, headers and content type on a reply and redirect safely with reply.redirect(url, code)."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Reply.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Status and headers:

- `reply.code(n)` / `reply.status(n)`; read via `reply.statusCode`.
- `reply.header(name, value)`, `reply.headers({ ... })`, `reply.type('text/html')`.
- `reply.getHeader(name)`, `reply.getHeaders()`, `reply.hasHeader(name)`, `reply.removeHeader(name)`.

```js
reply.code(201).header('x-id', '42').type('application/json').send({ ok: true })
```

Redirect: v5 signature is `reply.redirect(url, code?)`, default 302.

```js
reply.redirect('/new-route')          // 302
reply.redirect('/new-route', 301)     // v4 order reply.redirect(301, url) was removed
```

Properties of interest: `reply.sent`, `reply.request`, `reply.log`, `reply.raw`, `reply.server`, `reply.routeOptions`, `reply.mediaType`, `reply.elapsedTime` (replaces `getResponseTime()`).

The redirect URL must be properly encoded (`encodeURI` or `encodeurl`); invalid URLs give a 500 `TypeError`. Encoding alone does not prevent open redirects: neither escapes `/`, so input such as `//evil.com` or `/\evil.com` survives and the browser resolves it as a new host. When `dest` can come from request input, check that the resolved target is same-origin or on an allowlist. The status is `302` unless set earlier with `reply.code()` or passed as the second argument (`reply.code(303).redirect('/home')` gives 303; an explicit second argument wins).

Header values must also be encoded; invalid characters give a 500 `TypeError`. Repeated `reply.header('set-cookie', ...)` calls each send a cookie rather than replacing; reset with `reply.removeHeader('set-cookie')`. `reply.type()` adds `utf-8` as charset only for JSON subtypes without a charset. `reply.getHeaders()` returns a shallow copy that includes headers set on `reply.raw`, with Fastify's taking precedence.

Gotcha: since v5, assigning `reply.sent = true` is forbidden; use `reply.hijack()`. Without a `reply.code()` call the status is 200.

`reply.callNotFound()` invokes the custom not-found handler; only the `preHandler` hook given to `setNotFoundHandler` runs.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Reply.md, Migration-Guide-V5.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
