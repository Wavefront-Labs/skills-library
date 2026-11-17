---
id: computing-software.web-development.fastify.diagnostics-channel-tracing
name: diagnostics-channel-tracing
category: computing-software
field: web-development
product: fastify
tags: [fastify, diagnostics-channel, tracing, observability, v5]
level: sme
status: docs-checked
description: "Trace Fastify with node diagnostics_channel: initialization event and tracing:fastify.request.handler channels."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Hooks.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fastify v5 supports Node's `diagnostics_channel` natively. One event, `fastify.initialization`, is published at initialization with the Fastify instance as a `fastify` property of the message, so a tracing package can add hooks, plugins or routes (load the instrumentation first). Five per-request events follow the TracingChannel naming (the TracingChannel API is experimental in Node.js):

- `tracing:fastify.request.handler:start` and `:end` always fire (`:end` also carries `async: Bool`).
- `tracing:fastify.request.handler:asyncStart` and `:asyncEnd` fire for async or Promise-returning handlers.
- `tracing:fastify.request.handler:error` fires when an error occurs and adds `error: Error`.

Each message has `request`, `reply` and `route: { url, method }` (the matched pattern such as `/collection/:id`, and the HTTP method). The same object is used for all events of a request.

```js
const diagnostics = require('node:diagnostics_channel')

diagnostics.subscribe('tracing:fastify.request.handler:start', (msg) => {
  console.log(msg.route.url)    // '/:id'
  console.log(msg.route.method) // 'GET'
})
diagnostics.subscribe('tracing:fastify.request.handler:error', (msg) => {
  // handler threw
})

const fastify = require('fastify')()
fastify.route({ method: 'GET', url: '/:id', handler: () => ({ hello: 'world' }) })
```

The migration guide notes the `end` message is the same as the one emitted on `start`.

Gotcha: `asyncStart`/`asyncEnd` fire only for async or Promise-returning handlers.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Hooks.md, Migration-Guide-V5.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
