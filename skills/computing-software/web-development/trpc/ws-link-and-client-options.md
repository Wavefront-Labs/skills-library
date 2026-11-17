---
id: computing-software.web-development.trpc.ws-link-and-client-options
name: ws-link-and-client-options
category: computing-software
field: web-development
product: trpc
tags: [trpc, wslink, createwsclient, websocket, keepalive]
level: practitioner
status: docs-checked
description: "Create a WebSocket client with createWSClient and wsLink, tuning reconnection backoff, lazy mode, keepAlive pings, connectionParams and lifecycle callbacks."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/wsLink.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`wsLink` is a terminating link for the WebSocket client and subscriptions. Pass it a client from `createWSClient`:

```ts
const wsClient = createWSClient({ url: 'ws://localhost:3000' });
const trpcClient = createTRPCClient<AppRouter>({
  links: [wsLink<AppRouter>({ client: wsClient })],
});
```

`wsLink` itself takes `client` and `transformer`. Put the transformer on `wsLink`, not on `createWSClient`.

`createWSClient` options:
- `url`: string or async function returning one.
- `connectionParams`: object or async function; sent as the first message and available in `createContext`.
- `WebSocket`: ponyfill implementation.
- `retryDelayMs`: function of the attempt index; the default is exponential backoff.
- `onOpen`, `onError`, `onClose(cause)`: lifecycle callbacks.
- `lazy: { enabled, closeMs }`: close the socket after inactivity (no messages and no pending requests); default off, `closeMs` default 0.
- `keepAlive: { enabled, intervalMs, pongTimeoutMs }`: send ping messages and drop the connection if no pong arrives. Defaults: disabled, 5000 ms interval, 1000 ms pong timeout.
- `experimental_encoder`: custom wire encoding, default JSON.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/client/links/wsLink.md (read in full): usage snippet, `WebSocketLinkOptions` and `WebSocketClientOptions` with all defaults (lazy off and closeMs 0, keepAlive off, 5000 ms interval, 1000 ms pong timeout, exponentialBackoff, jsonEncoder).

Removed or corrected: the unsourced advice on when to use keepAlive and lazy, and the invented Verify step.

Method: documentation only; no commands were run.
