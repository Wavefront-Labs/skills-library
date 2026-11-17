---
id: computing-software.web-development.vite.server-warmup-watch
name: server-warmup-watch
category: computing-software
field: web-development
product: vite
tags: [server-warmup-option, server-watch, wsl2-polling, server-middleware-mode]
level: advanced
status: docs-checked
description: "server.warmup clientFiles and ssrFiles, server.watch chokidar options and WSL2 polling, and server.middlewareMode with appType custom."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/server-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`server.warmup` (`{ clientFiles?, ssrFiles? }`): paths or `tinyglobby` patterns relative to `root`, transformed and cached ahead of time. Only list frequently used files.

```js
server: { warmup: { clientFiles: ['./src/components/*.vue'], ssrFiles: ['./src/server/modules/*.js'] } }
```

`server.watch` (`object | null`): chokidar options. Skips `.git/`, `node_modules/`, `test-results/`, `cacheDir` and `build.outDir`. `null` watches nothing. Files in `node_modules` cannot be watched currently. On WSL2, edits from Windows apps are not detected; edit with WSL2 apps (and keep the project off the Windows filesystem) or set `{ usePolling: true }`, which costs high CPU.

`server.middlewareMode` (`boolean | { server: http.Server }`, default `false`): create Vite as middleware inside another server. With a WebSocket proxy, provide `server`. Use `appType: 'custom'` to skip Vite's HTML handling:

```js
const vite = await createViteServer({ server: { middlewareMode: true }, appType: 'custom' })
app.use(vite.middlewares)
```

With `'spa'` or `'mpa'`, add your middlewares before Vite's.

## Checked

2026-11-07. Re-read the Server Options page (docs/config/server-options.md) in full. Confirmed server.warmup (clientFiles, ssrFiles, tinyglobby patterns relative to root, only frequently used files), server.watch (chokidar, default skipped directories, null, node_modules limit, WSL2 behaviour and usePolling CPU cost) and server.middlewareMode (type, default false, server for WebSocket proxy, appType custom, middleware ordering for spa and mpa). Nothing removed.

Method: documentation only; no commands were run.
