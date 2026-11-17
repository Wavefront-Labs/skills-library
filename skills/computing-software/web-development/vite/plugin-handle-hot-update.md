---
id: computing-software.web-development.vite.plugin-handle-hot-update
name: plugin-handle-hot-update
category: computing-software
field: web-development
product: vite
tags: [handle-hot-update, hmr-context, custom-hmr-event, module-graph-invalidate]
level: advanced
status: docs-checked
description: "handleHotUpdate hook: narrow affected modules, force a full reload after invalidating modules, or send custom WebSocket events for hand-rolled HMR."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`handleHotUpdate(ctx)` is per-environment, async, sequential. `ctx` is `HmrContext`: `file`, `timestamp`, `modules` (affected `ModuleNode`s; an array because one file may map to several served modules, such as Vue SFCs), `read()` and `server`. Use `read()` rather than `fs.readFile`, which can return empty content if the editor has not finished writing.

The hook can:
1. Return a filtered, narrower module array for more accurate HMR.
2. Return `[]` after a manual full reload:

```js
handleHotUpdate({ server, modules, timestamp }) {
  const invalidated = new Set()
  for (const mod of modules) {
    server.moduleGraph.invalidateModule(mod, invalidated, timestamp, true)
  }
  server.ws.send({ type: 'full-reload' })
  return []
}
```

3. Return `[]` and send a custom event:

```js
handleHotUpdate({ server }) {
  server.ws.send({ type: 'custom', event: 'special-update', data: {} })
  return []
}
```

The client handles it with `import.meta.hot.on('special-update', cb)`, which the same plugin's `transform` can inject.

## Checked

Date: 2026-11-07

Read api-plugin.md in full (handleHotUpdate). Confirmed per-environment async sequential, HmrContext fields, the read() rationale, the three options and both code examples. Nothing removed.

Method: documentation only; no commands were run.
