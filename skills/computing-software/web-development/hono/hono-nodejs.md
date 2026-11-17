---
id: computing-software.web-development.hono.hono-nodejs
name: hono-nodejs
category: computing-software
field: web-development
product: hono
tags: [hono, nodejs, node-server, http2, docker]
level: practitioner
status: docs-checked
description: "Run Hono on Node.js with @hono/node-server: serve, port, graceful shutdown, WebSocket, raw incoming/outgoing, HTTP/2 and a Dockerfile."
sources:
  - https://github.com/honojs/website/blob/main/docs/getting-started/nodejs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hono on Node.js

Needs Node 18.14.1+ / 19.7.0+ / 20.0.0+ (practically, the latest of each major). Start with `npm create hono@latest my-app` (template `nodejs`).

```ts
import { serve } from '@hono/node-server'
import { Hono } from 'hono'

const app = new Hono()
app.get('/', (c) => c.text('Hello Node.js!'))
serve(app)   // http://localhost:3000
```
Port: `serve({ fetch: app.fetch, port: 8787 })`.

## Graceful shutdown
`serve()` returns the underlying server, so closing it is your job:

```ts
const server = serve(app)
process.on('SIGINT', () => { server.close(); process.exit(0) })
process.on('SIGTERM', () => {
  server.close((err) => { if (err) { console.error(err); process.exit(1) } process.exit(0) })
})
```

## WebSocket
Built in to `@hono/node-server`: install `ws` (and `@types/ws`), then

```ts
import { serve, upgradeWebSocket } from '@hono/node-server'
import { WebSocketServer } from 'ws'
app.get('/ws', upgradeWebSocket(() => ({ onMessage(event, ws) { ws.send(event.data) } })))
const wss = new WebSocketServer({ noServer: true })
serve({ fetch: app.fetch, websocket: { server: wss } })
```
`@hono/node-ws` is deprecated.

## Raw Node objects
```ts
import { serve, type HttpBindings } from '@hono/node-server' // Http2Bindings for HTTP/2
const app = new Hono<{ Bindings: HttpBindings }>()
app.get('/', (c) => c.json({ remoteAddress: c.env.incoming.socket.remoteAddress }))
```

## HTTP/2
`serve({ fetch: app.fetch, createServer })` with `createServer` from `node:http2`; for TLS use `createSecureServer` plus `serverOptions: { key, cert }` read with `readFileSync`.

## Docker
Multi-stage `node:22-alpine`: builder runs `npm ci && npm run build && npm prune --production`; runner creates a non-root `hono` user (uid 1001), copies `node_modules`, `dist`, `package.json`, `EXPOSE 3000`, `CMD ["node", "/app/dist/index.js"]`.

## Gotcha
Apps with a front-end framework may need Hono's Vite plugins for the build.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page getting-started/nodejs.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
