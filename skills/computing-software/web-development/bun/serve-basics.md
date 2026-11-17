---
id: computing-software.web-development.bun.serve-basics
name: serve-basics
category: computing-software
field: web-development
product: bun
tags: [bun-serve, idle-timeout, server-stop, unix-socket]
level: practitioner
status: docs-checked
description: "Run an HTTP server with Bun.serve: port resolution, idleTimeout and per-request timeouts for streams, graceful stop, reload, requestIP and HTTP/2 caveats."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/http/server.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
const server = Bun.serve({
  port: 8080,
  fetch(req, server) {
    server.timeout(req, 60);               // this request: 60 s idle limit
    return new Response("ok");
  },
});
await fetch(new URL("/users", server.url)); // not `${server.url}/users` (double slash)
await server.stop();      // graceful; stop(true) forces, WebSockets get 1001
server.reload({ fetch() { return new Response("v2"); } }); // fetch, error, routes, websocket only
```

- Port: option, else `--port`, `BUN_PORT`, `PORT`, `NODE_PORT`, else 3000. Port 0 picks a random free port (`server.port`).
- `idleTimeout`: default 10 s, max 255, `0` disables. Quiet streams are cut; for SSE use `server.timeout(req, 0)`.
- `unix: "/tmp/my-socket.sock"` for a Unix socket; `server.requestIP(req)` returns null for closed requests and Unix sockets.
- `server.unref()` lets the process exit; `closeIdleConnections()` closes idle keep-alive only.
- `http3: true` needs `tls`; `http1: false` needs `http2` or `http3`, and then `server.upgrade()` (WebSockets) is unavailable.
- Metrics: `pendingRequests`, `pendingWebSockets`, `subscriberCount(topic)`.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/http/server: port resolution order (option, --port, BUN_PORT, PORT, NODE_PORT, then 3000) and port 0, server.url href ending in a slash, idleTimeout default 10 and max 255 with 0 disabling it, SSE and server.timeout(req, 0), unix socket option, requestIP null cases, stop() versus stop(true) with close code 1001, reload limited to fetch/error/routes/websocket, unref, closeIdleConnections, http3 needing tls, http1:false needing http2 or http3 and server.upgrade being HTTP/1.1 only, and the metrics properties. Nothing removed.
Method: documentation only; no commands were run.
