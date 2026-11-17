---
id: computing-software.web-development.vite.environment-runnable-ssr
name: environment-runnable-ssr
category: computing-software
field: web-development
product: vite
tags: [runnable-dev-environment, module-runner-import, fetchable-dev-environment, dispatch-fetch]
level: advanced
status: docs-checked
description: "Framework dev SSR with RunnableDevEnvironment and runner.import (successor to ssrLoadModule), FetchableDevEnvironment handleRequest/dispatchFetch, and raw DevEnvironment options."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-environment-frameworks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three communication levels exist.

`RunnableDevEnvironment` evaluates modules in the same runtime as the Vite server, so real exports cross in-process. Non-client environments use it by default in dev. Guard with `isRunnableDevEnvironment`; `environment.runner.import(url)` (file path, server path or root-relative id) fetches, transforms and evaluates with HMR, replacing `server.ssrLoadModule`. The runner is created lazily and enables source map support (`process.setSourceMapsEnabled` or `Error.prepareStackTrace`).

```js
const viteServer = await createServer({
  server: { middlewareMode: true },
  appType: 'custom',
  environments: { server: {} },
})
const { render } = await viteServer.environments.server.runner.import('/src/entry-server.js')
```

Add `import.meta.hot.accept()` to the server entry, or any change invalidates the whole server module graph.

`FetchableDevEnvironment` talks via Fetch API `Request` and `Response`; use it for runtimes that cannot run Vite (such as Cloudflare Workers). Create it in `dev.createEnvironment` with `createFetchableDevEnvironment(name, config, { handleRequest })`; call `environment.dispatchFetch(new Request(...))`, guarded by `isFetchableDevEnvironment`. Vite throws `TypeError` for non-global `Request`/`Response`. The class is an implementation detail.

Raw `DevEnvironment`: communicate through a virtual module entry (same runtime), or via `hot.send` and `hot.on` for Node-only code.

## Checked

2026-11-07. Confirmed against the "DevEnvironment Communication Levels" section of guide/api-environment-frameworks.md (page read in full): `RunnableDevEnvironment`, `isRunnableDevEnvironment`, `runner.import(url)` replacing `server.ssrLoadModule`, lazy runner and source map support, the middleware example, the `import.meta.hot.accept()` advice, `FetchableDevEnvironment` (`createFetchableDevEnvironment`, `handleRequest`, `dispatchFetch`, `TypeError`, implementation-detail warning) and the raw `DevEnvironment` options. Nothing removed.

Method: documentation only; no commands were run.
