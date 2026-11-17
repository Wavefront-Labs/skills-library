---
id: computing-software.web-development.vite.server-hmr-ws-console
name: server-hmr-ws-console
category: computing-software
field: web-development
product: vite
tags: [server-hmr, server-ws, hmr-overlay, forward-console]
level: advanced
status: docs-checked
description: "Tune HMR overlay, the server.ws WebSocket options (clientPort, reverse proxy fallback) and server.forwardConsole for browser errors in the terminal."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/server-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`server.hmr` (`boolean | { overlay?: boolean }`): `overlay: false` disables the error overlay. The old WebSocket options under it (`protocol`, `host`, `port`, `path`, `clientPort`, `timeout`, `server`) are deprecated and synced to `server.ws`.

`server.ws`: `false` disables the WebSocket, or an object with `protocol` (`ws`/`wss`), `host`, `port`, `path`, `timeout` (default 30000 ms), `clientPort`, `server` (custom HTTP server).

```js
server: { ws: { protocol: 'wss', host: 'localhost', port: 3001 } }
```

Reverse proxies must proxy WebSocket. If not, the client falls back to a direct connection and logs "Direct websocket connection fallback"; the browser error can be ignored. To avoid it: proxy WebSocket, or set `strictPort: true` with `ws.clientPort` equal to `server.port`, or set `ws.port` different from `server.port`.

`server.forwardConsole` (default auto: `true` when an AI coding agent is detected, else `false`) forwards browser events to the server console:

```js
server: { forwardConsole: { unhandledErrors: true, logLevels: ['warn', 'error'] } }
```

## Checked

2026-11-04. Confirmed against the Vite server options page (docs/config/server-options.md): hmr overlay, deprecated WebSocket options, server.ws fields and 30000 ms timeout, reverse-proxy fallback advice, forwardConsole default. Nothing removed.

Method: documentation only; no commands were run.
