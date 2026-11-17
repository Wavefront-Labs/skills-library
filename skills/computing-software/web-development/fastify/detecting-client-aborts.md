---
id: computing-software.web-development.fastify.detecting-client-aborts
name: detecting-client-aborts
category: computing-software
field: web-development
product: fastify
tags: [fastify, request, abort, signal, disconnect]
level: advanced
status: docs-checked
description: "Detect that a client aborted a request using request.signal, onRequestAbort or the raw close event."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Detecting-When-Clients-Abort.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Request.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`clientErrorHandler` is not for this: it handles raw socket errors such as bad requests, not client aborts (there is no socket error on abort).

`request.signal` is an AbortSignal that aborts on handler timeout or client disconnect (created lazily on first access). On timeout `signal.reason` is the `FST_ERR_HANDLER_TIMEOUT` error; on disconnect it is a generic `AbortError`; check `signal.reason.code` to tell them apart. Pass it to `fetch()`, database queries or any API accepting a `signal`:

```js
fastify.get('/', async (request, reply) => {
  const res = await fetch(upstreamUrl, { signal: request.signal })
  return res.json()
})
```

The guide's approach uses the raw request `close` event with `aborted`:

```js
app.addHook('onRequest', async (request, reply) => {
  request.raw.on('close', () => {
    if (request.raw.aborted) {
      app.log.info('request closed')
    }
  })
})
```

You can check `request.raw.aborted` at any point in the handler, and doing it in app code lets you log Fastify details like `reqId`. The `onRequestAbort` hook is also available.

Gotcha: `aborted` is deprecated in Node but `destroyed` is not a replacement; a request can be destroyed when the server closes the connection. Network interruptions without a clean abort will not trigger it, and a server crash can look like a false abort.

Test: abort a `fetch` with an `AbortController` after 1 s against a route that sleeps 3 s and look for the log line.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Detecting-When-Clients-Abort.md, Request.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
