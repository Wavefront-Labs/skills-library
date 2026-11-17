---
id: computing-software.web-development.fastify.graceful-shutdown-close
name: graceful-shutdown-close
category: computing-software
field: web-development
product: fastify
tags: [fastify, shutdown, close, hooks, lifecycle]
level: advanced
status: docs-checked
description: "Understand the order of fastify.close(): closing flag, preClose, connection draining, server.close, onClose."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Hooks.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Lifecycle.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`await fastify.close()` runs in this order:

1. The server is flagged as closing. New requests receive a `Connection: close` header (HTTP/1.1) and are handled per `return503OnClosing` (default `true`: a 503 response).
2. `preClose` hooks run; in-flight requests are still being processed.
3. Connections are drained according to `forceCloseConnections`: `'idle'` closes idle keep-alive connections, `true` destroys all persistent connections, `false` forces nothing.
4. The HTTP server stops accepting new TCP connections (`server.close()`), and Node.js waits for in-flight requests to complete.
5. `onClose` hooks run; child-plugin hooks execute before parent-plugin hooks.
6. The `close` callback or returned Promise resolves.

```js
fastify.addHook('preClose', async function () {
  // stop accepting new websocket upgrades, close them
})
fastify.addHook('onClose', async (instance) => {
  await instance.db.end()
})

process.on('SIGTERM', async () => {
  await fastify.close()
  process.exit(0)
})
```

`onClose` also accepts an object with `Symbol.asyncDispose` or `Symbol.dispose`.

Gotcha: upgraded connections such as WebSocket are not tracked by the HTTP server and prevent `server.close()` from completing. Close them explicitly in a `preClose` hook.

At the end of tests it is highly recommended to call `.close()`, for example `t.after(() => fastify.close())`.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Server.md, Hooks.md, Lifecycle.md, Testing.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
