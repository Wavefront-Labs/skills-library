---
id: computing-software.web-development.vite.ssr-dev-middleware
name: ssr-dev-middleware
category: computing-software
field: web-development
product: vite
tags: [ssr-middleware-mode, ssr-load-module, transform-index-html, ssr-outlet]
level: advanced
status: docs-checked
description: "Run Vite SSR in dev: middleware mode with appType custom, the source layout, ssr-outlet placeholder, the render handler, ssrFixStacktrace, and SSR-only reload."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/ssr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SSR here means a front-end framework rendering in Node.js and hydrating on the client. This is a low-level API for library and framework authors.

Layout: `index.html`, `server.js`, `src/main.js` (universal app), `src/entry-client.js` (mounts), `src/entry-server.js` (renders). `index.html` holds a placeholder such as `<div id="app"><!--ssr-outlet--></div>` plus the client entry script.

Create Vite in middleware mode:

```js
const vite = await createViteServer({
  server: { middlewareMode: true },
  appType: 'custom',
})
app.use(vite.middlewares)
```

`vite.middlewares` is a Connect instance. Per request: read `index.html`; `template = await vite.transformIndexHtml(url, template)`; `const { render } = await vite.ssrLoadModule('/src/entry-server.js')`; `appHtml = await render(url)`; replace the outlet; send. In `catch`, call `vite.ssrFixStacktrace(e)` then `next(e)`.

Set the `dev` script to `node server`. Use `import.meta.env.SSR` for server-only branches (statically replaced, tree-shaken).

By default an SSR-only module update does not reload the browser; frameworks usually handle it, or add a `hotUpdate` plugin that sends `full-reload`.

## Checked

2026-11-04. Confirmed against the Vite SSR guide (docs/guide/ssr.md): source layout, ssr-outlet placeholder, middleware mode with appType custom, per-request render steps, ssrFixStacktrace, dev script, import.meta.env.SSR, SSR-only module reload tip. Nothing removed.

Method: documentation only; no commands were run.
