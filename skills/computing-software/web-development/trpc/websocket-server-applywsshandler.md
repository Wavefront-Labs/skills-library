---
id: computing-software.web-development.trpc.websocket-server-applywsshandler
name: websocket-server-applywsshandler
category: computing-software
field: web-development
product: trpc
tags: [trpc, websockets, applywsshandler, ws, keepalive]
level: advanced
status: docs-checked
description: "Create a ws WebSocketServer with applyWSSHandler, enable keepAlive heartbeats, share an HTTP port, and send a reconnect notification on SIGTERM."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/websockets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install `ws` and attach the tRPC handler to a `WebSocketServer`:

```ts
import { applyWSSHandler } from '@trpc/server/adapters/ws';
import { WebSocketServer } from 'ws';

const wss = new WebSocketServer({ port: 3001 });
const handler = applyWSSHandler({
  wss,
  router: appRouter,
  createContext,
  // heartbeat messages to keep the connection open (disabled by default)
  keepAlive: { enabled: true, pingMs: 30000, pongWaitMs: 5000 },
});

process.on('SIGTERM', () => {
  handler.broadcastReconnectNotification();
  wss.close();
});
```

`broadcastReconnectNotification()` tells clients (message `{ id: null, type: 'reconnect' }`) to reconnect before the server shuts down.

Sharing a port with your HTTP server: pass the HTTP server to `WebSocketServer({ server })`; `ws` handles upgrade requests and your adapter handles the rest.

```ts
const server = createHTTPServer({ router: appRouter });
const wss = new WebSocketServer({ server });
applyWSSHandler({ wss, router: appRouter });
server.listen(3000);
```

`applyWSSHandler` accepts `maxBatchSize` like the HTTP adapters: an over-size WebSocket message is rejected as a whole, no procedure runs, and each request in it (except `subscription.stop`) gets a `BAD_REQUEST` with the message `Batch call exceeds maximum size`. `wsLink` batches calls made in the same tick into one message and has no `maxItems` option, so set the limit above the number of simultaneous calls your client makes.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/websockets.md (read in full): "Creating a WebSocket-server" with keepAlive and SIGTERM, "Sharing a port with your HTTP server", "Limiting batch size" and the reconnect notification.

Removed or corrected: the "smooths deploys" claim and the invented Verify step about connection counts.

Method: documentation only; no commands were run.
