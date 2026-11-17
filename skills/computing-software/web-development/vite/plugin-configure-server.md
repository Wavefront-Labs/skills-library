---
id: computing-software.web-development.vite.plugin-configure-server
name: plugin-configure-server
category: computing-software
field: web-development
product: vite
tags: [configure-server-hook, post-middleware, close-server-hook, preview-server-hooks]
level: advanced
status: docs-checked
description: "Use configureServer and configurePreviewServer to add middleware (before or after internals, via a returned function), store the server, and clean up in closeServer."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`configureServer(server)`: async, sequential, global. Called before internal middlewares are installed, so custom middleware runs first:

```js
configureServer(server) {
  server.middlewares.use((req, res, next) => { /* ... */ })
}
```

To run after internal middlewares, return a function:

```js
configureServer(server) {
  return () => { server.middlewares.use((req, res, next) => { /* ... */ }) }
}
```

Store `server` in a closure variable for other hooks (WebSocket, watcher, module graph). It is not called in production builds, so guard for its absence.

`configurePreviewServer(server)` works the same for the preview server.

`closeServer({ reason })`: async, parallel, called after the dev server is torn down, to dispose resources. `reason` is `'restart'` (config change or `server.restart()`) or `'close'` (the `q` shortcut or `server.close()`).

`closePreviewServer()`: same for preview; it never restarts so there is no reason.

```js
async closeServer({ reason }) { if (reason === 'close') await resource.dispose() }
```

## Checked

Date: 2026-11-07

Read api-plugin.md in full (configureServer, configurePreviewServer, closeServer, closePreviewServer). Confirmed kinds, middleware order, the returned post hook, stored server access, absence in production builds, and the restart/close reasons. Nothing removed.

Method: documentation only; no commands were run.
