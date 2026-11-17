---
id: computing-software.web-development.vite.js-api-vite-dev-server
name: js-api-vite-dev-server
category: computing-software
field: web-development
product: vite
tags: [vite-dev-server, transform-request, module-graph, wait-for-requests-idle, server-restart]
level: advanced
status: docs-checked
description: "ViteDevServer members: middlewares, watcher, ws, moduleGraph, transformRequest, ssrLoadModule, reloadModule, restart and the experimental waitForRequestsIdle."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-javascript.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ViteDevServer` members:
- `config`: resolved config.
- `middlewares`: connect app; attach middleware or use as a handler in a custom server or connect-style framework.
- `httpServer`: Node server, `null` in middleware mode.
- `watcher`: chokidar instance; with `server.watch: null`, `add` and `unwatch` do nothing.
- `ws`: WebSocket server with `send(payload)`.
- `pluginContainer`: runs plugin hooks on a file.
- `moduleGraph`: import relationships, URL-to-file mapping, HMR state.
- `resolvedUrls`: printed URLs; `null` in middleware mode or when not listening.
- `transformRequest(url, options?)`: resolve, load and transform without HTTP.
- `transformIndexHtml(url, html, originalUrl?)`: built-in plus plugin HTML transforms.
- `ssrLoadModule(url, { fixStacktrace? })` and `ssrFixStacktrace(e)`.
- `reloadModule(module)`: triggers HMR; no-op if `hmr` is false.
- `listen(port?, isRestart?)`, `restart(forceOptimize?)` (same as `--force`), `close()`, `bindCLIShortcuts(options?)`.

`waitForRequestsIdle(ignoredId?)` (experimental) waits until all static imports are processed, an escape hatch for tools like Tailwind delaying CSS class generation. In a `load` or `transform` hook pass the module `id` to avoid deadlocks; with the default HTTP1 server it blocks one of six channels until done. The dependency optimizer uses it; `optimizeDeps.holdUntilCrawlEnd: false` may become the default.

## Checked

2026-11-04. Confirmed against the Vite JavaScript API guide (docs/guide/api-javascript.md, ViteDevServer interface and waitForRequestsIdle note): every member listed, nullability in middleware mode, restart forceOptimize, HTTP1 six-channel note, holdUntilCrawlEnd. Nothing removed.

Method: documentation only; no commands were run.
