---
id: computing-software.web-development.vite.js-api-create-server
name: js-api-create-server
category: computing-software
field: web-development
product: vite
tags: [create-server, inline-config, resolved-config, middleware-mode-websocket-proxy]
level: practitioner
status: docs-checked
description: "Start Vite from Node with createServer and InlineConfig (configFile false), NODE_ENV conflicts with build, parent http server for WebSocket proxy, ResolvedConfig utilities."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-javascript.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { createServer } from 'vite'

const server = await createServer({
  configFile: false,
  root: import.meta.dirname,
  server: { port: 1337 },
})
await server.listen()
server.printUrls()
server.bindCLIShortcuts({ print: true })
```

`InlineConfig` is `UserConfig` plus `configFile` (`false` disables auto resolving) and `mode`. `ResolvedConfig` has resolved, non-undefined properties plus `config.assetsInclude(id)` and `config.logger`.

If `createServer` and `build` run in the same Node.js process, both depend on `process.env.NODE_ENV` (which depends on `mode`). Set `NODE_ENV` or `mode` of both to `development`, or run them in separate child processes.

Middleware mode with a WebSocket proxy: pass the parent HTTP server so the proxy binds correctly.

```ts
server: {
  middlewareMode: { server: parentServer },
  proxy: { '/ws': { target: 'ws://localhost:3000', ws: true } },
}
```

## Checked

2026-11-04. Confirmed against the Vite JavaScript API guide (docs/guide/api-javascript.md): createServer example, InlineConfig configFile, ResolvedConfig utilities, shared-process NODE_ENV note, middlewareMode with parent server for WebSocket proxy. Nothing removed.

Method: documentation only; no commands were run.
