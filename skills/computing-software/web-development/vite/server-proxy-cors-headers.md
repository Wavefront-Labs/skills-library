---
id: computing-software.web-development.vite.server-proxy-cors-headers
name: server-proxy-cors-headers
category: computing-software
field: web-development
product: vite
tags: [server-proxy, server-cors, server-headers, websocket-proxy]
level: practitioner
status: docs-checked
description: "Configure server.proxy rules (string, options, regex keys, ws, configure), server.cors defaults and danger of true, and server.headers."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/server-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`server.proxy` is `Record<string, string | ProxyOptions>`. A request path starting with the key is proxied; a key starting with `^` is a RegExp. Matching requests are not transformed by Vite. With a non-relative `base`, prefix each key with it. Options extend `http-proxy-3`; `configure(proxy, options)` exposes the instance. For custom middleware use a plugin with `configureServer`.

```js
server: {
  proxy: {
    '/foo': 'http://localhost:4567',
    '/api': {
      target: 'http://jsonplaceholder.typicode.com',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, ''),
    },
    '/socket.io': { target: 'ws://localhost:5174', ws: true, rewriteWsOrigin: true },
  },
}
```

Vite does not check WebSocket request origin before proxying; the target must. `rewriteWsOrigin` bypasses that check and can open CSRF attacks.

`server.cors` (`boolean | CorsOptions`): default allows localhost, `127.0.0.1` and `::1` origins. `true` allows any website to download your source; prefer an explicit origin list.

`server.headers`: `OutgoingHttpHeaders` added to responses.

## Checked

2026-11-04. Confirmed against the Vite server options page (docs/config/server-options.md): proxy key matching, ^ RegExp keys, http-proxy-3, configure, WebSocket origin warning, cors default and danger note, headers. Nothing removed.

Method: documentation only; no commands were run.
