---
id: computing-software.web-development.hono.hono-websocket-helper
name: hono-websocket-helper
category: computing-software
field: web-development
product: hono
tags: [hono, helper, websocket, rpc, bun, node]
level: advanced
status: docs-checked
description: "Add server-side WebSockets to Hono with upgradeWebSocket per runtime (Workers, Deno, Bun, Node.js), events, RPC client and header-middleware pitfalls."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/websocket.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WebSocket helper

Adapters are separate packages: `upgradeWebSocket` from `@hono/cloudflare-workers`, `@hono/deno`, `@hono/bun` (also `websocket`), or `@hono/node-server` (Node.js).

```ts
app.get('/ws', upgradeWebSocket((c) => ({
  onMessage(event, ws) {
    console.log(`Message from client: ${event.data}`)
    ws.send('Hello from server!')
  },
  onClose: () => console.log('Connection closed'),
})))
```

Events: `onOpen` (not supported on Cloudflare Workers), `onMessage`, `onClose`, `onError`.

## Bun
```ts
import { upgradeWebSocket, websocket } from '@hono/bun'
export default { fetch: app.fetch, websocket }
```

## Node.js
Built into `@hono/node-server`; `@hono/node-ws` is deprecated. Install `ws` (and `@types/ws`), create `new WebSocketServer({ noServer: true })` and pass it to `serve()`:

```ts
import { serve, upgradeWebSocket } from '@hono/node-server'
import { WebSocketServer } from 'ws'
const wss = new WebSocketServer({ noServer: true })
serve({ fetch: app.fetch, websocket: { server: wss } })
```

## RPC mode
```ts
// server.ts
const wsApp = app.get('/ws', upgradeWebSocket((c) => { /* ... */ }))
export type WebSocketApp = typeof wsApp
// client.ts
const client = hc<WebSocketApp>('http://localhost:8787')
const socket = client.ws.$ws() // a WebSocket object
```

## Gotcha
Middleware that modifies headers (for example CORS) on a WebSocket route can fail with an immutable headers error, because `upgradeWebSocket()` also changes headers internally.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page helpers/websocket.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
