---
id: computing-software.web-development.vite.hmr-api-events-invalidate
name: hmr-api-events-invalidate
category: computing-software
field: web-development
product: vite
tags: [hot-invalidate, hot-on-events, hot-off, hot-send, vite-hmr-events]
level: advanced
status: docs-checked
description: "HMR invalidate inside the accept callback, built-in vite: events (beforeUpdate, error, ws:connect and others), hot.on and off, hot.send buffering."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-hmr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`hot.invalidate(message?)`: a self-accepting module that cannot handle an update propagates it to importers, as if it were not self-accepting. A message is logged in the browser console and terminal. Still call `accept` even if you invalidate immediately, or the client stops listening for future changes. Clearest pattern:

```js
import.meta.hot.accept((module) => {
  if (cannotHandleUpdate(module)) import.meta.hot.invalidate()
})
```

`hot.on(event, cb)` listens; `hot.off(event, cb)` removes. Events Vite dispatches:
- `vite:beforeUpdate`: update about to apply.
- `vite:afterUpdate`: update just applied.
- `vite:beforeFullReload`: full reload imminent.
- `vite:beforePrune`: unneeded modules about to be pruned.
- `vite:invalidate`: a module called `invalidate()`.
- `vite:error`: for example a syntax error.
- `vite:ws:disconnect`: WebSocket lost.
- `vite:ws:connect`: WebSocket (re-)established.

Plugins can send custom events (see `handleHotUpdate`).

`hot.send(event, data)` sends a custom event to the dev server; data sent before the connection exists is buffered and sent once connected.

## Checked

2026-11-07. Confirmed against guide/api-hmr.md, read in full: `hot.invalidate(message?)` behaviour, the advice to always call `accept` and invalidate inside the callback, `hot.on`/`hot.off`, all eight built-in `vite:` events and their meanings, and `hot.send` buffering before connection. Nothing removed.

Method: documentation only; no commands were run.
