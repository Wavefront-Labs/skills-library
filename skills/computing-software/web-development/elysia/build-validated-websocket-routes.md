---
id: computing-software.web-development.elysia.build-validated-websocket-routes
name: build-validated-websocket-routes
category: computing-software
field: web-development
product: elysia
tags: [websocket, ws-route, message-validation, bun-websocket-config, backpressure]
level: practitioner
status: docs-checked
description: "Add a WebSocket endpoint with Elysia .ws(), validate messages, query and headers, use open/message/close/drain handlers and tune idleTimeout and compression."
sources:
  - https://elysiajs.com/patterns/websocket.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: expose a real-time endpoint with typed, validated messages.

## Minimal echo

```ts
import { Elysia } from 'elysia'

new Elysia()
  .ws('/ws', {
    message(ws, message) { ws.send(message) }
  })
  .listen(3000)
```

Signature: `.ws(endpoint: path, options: Partial<WebSocketHandler<Context>>)`. Elysia uses uWebSockets (the same implementation and API Bun uses).

## Validate messages and connection data

```ts
.ws('/ws', {
  body: t.Object({ message: t.String() }),   // incoming message
  query: t.Object({ id: t.String() }),
  message(ws, { message }) {
    const { id } = ws.data.query              // schema-validated values live on ws.data
    ws.send({ id, message, time: Date.now() })
  }
})
```

Schema can cover: message (`body`), `query`, `params`, `header`, `cookie`, and `response` (value returned from the handler). By default Elysia parses an incoming stringified JSON message into an object for validation.

## Handlers

- `open(ws)`: new connection. `ws` is a `ServerWebSocket` with a per-connection `id` and `data: Context`.
- `message(ws, message)`: the `Message` type follows the schema's message type; default `string`.
- `close(ws)`.
- `drain(ws, code, reason)`: server is ready for more data.
- Other options: `parse` (parses the incoming message before validation; previously named `transformMessage`), `beforeHandle` (runs before the HTTP connection is upgraded; the docs call it the ideal place for validation), `transform` (runs before validation) and `header` (additional headers added before the upgrade).

## Configuration

Set in the constructor: `new Elysia({ websocket: { idleTimeout: 30 } })`. Options (extend Bun's WebSocket config):

- `perMessageDeflate` default `false` (compression off)
- `maxPayloadLength` maximum message size in bytes
- `idleTimeout` default `120` seconds
- `backpressureLimit` default `16777216` (16MB) of buffered bytes per connection
- `closeOnBackpressureLimit` default `false`

## Gotchas

- `beforeHandle` runs before the HTTP connection is upgraded, which the docs call the ideal place for validation.
- Validated query values are read from `ws.data.query` inside handlers (as in the docs example).
- Without a message schema, `message` is a `string`.

## Checked

Checked 2026-11-07 against the Elysia documentation source (patterns/websocket.html); each claim, option name and default was compared with the page text. Corrected the hook list (parse was formerly transformMessage; only beforeHandle is documented as pre-upgrade).

Method: documentation only; no commands were run.
