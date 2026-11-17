---
id: computing-software.web-development.trpc.websocket-origin-and-auth
name: websocket-origin-and-auth
category: computing-software
field: web-development
product: trpc
tags: [trpc, websockets, security, origin, connectionparams]
level: advanced
status: docs-checked
description: "Secure tRPC WebSockets: reject cross-origin upgrades in verifyClient and authenticate with connectionParams read from opts.info.connectionParams."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/websockets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Browsers do not apply CORS to WebSockets: a page on any origin can open a connection to your server and the browser sends its cookies. If you authenticate with cookies, check the `Origin` header. With `ws`, use `verifyClient` and pass 403 so a rejected upgrade gets `403 Forbidden`:

```ts
const allowedOrigins = new Set(['https://app.example.com']);
const wss = new WebSocketServer({
  port: 3001,
  verifyClient: ({ origin }, callback) => {
    // Browsers always send Origin, but other clients may not; decide whether to accept none.
    callback(!origin || allowedOrigins.has(origin), 403);
  },
});
```

With `noServer: true`, check `req.headers.origin` in your `upgrade` listener and end the socket with `socket.end('HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\n')` instead of calling `wss.handleUpgrade()`.

Token auth: define `connectionParams` on `createWSClient` (sent as the first message when the connection opens), and read them on the server:

```ts
export const createContext = async (opts: CreateWSSContextFnOptions) => {
  const token = opts.info.connectionParams?.token;
  // authenticate
  return {};
};
```

`createContext` runs once per connection (after connection params arrive) and all calls on that connection share it; if it throws, the server sends the error and closes the connection. A token is only checked at connect time, so it stays accepted on that connection after it expires. The page says web applications can ignore the connection params section because cookies are sent as part of the request.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/websockets.md (read in full): "Rejecting cross-origin connections" (both the verifyClient and noServer variants) and "Authentication / connection params" including the paragraph on createContext running once per connection.

Removed or corrected: the "connection params are optional" wording (reworded to the page sentence) and the invented Verify step.

Method: documentation only; no commands were run.
