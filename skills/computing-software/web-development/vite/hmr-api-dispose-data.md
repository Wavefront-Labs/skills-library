---
id: computing-software.web-development.vite.hmr-api-dispose-data
name: hmr-api-dispose-data
category: computing-software
field: web-development
product: vite
tags: [hot-dispose, hot-prune, hot-data, hot-decline]
level: advanced
status: docs-checked
description: "HMR cleanup and state: hot.dispose for side effects, hot.prune when no longer imported, hot.data persistence rules (mutate, never reassign), hot.decline noop."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-hmr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`hot.dispose(cb)`: for a self-accepting module, or one accepted by others, to clean up persistent side effects created by its updated copy. `cb` receives `data`.

```js
if (import.meta.hot) {
  import.meta.hot.dispose((data) => { /* cleanup side effect */ })
}
```

`hot.prune(cb)`: called when the module is no longer imported on the page. Use it instead of `dispose` when the code handles its own cleanup on updates and only needs cleanup on removal. Vite uses it for `.css` imports.

`hot.data`: one object per module path, persisted across successive instances during HMR. Mutations during execution or via the `data` argument of `dispose` are visible to the next instance. When a module is pruned, its `dispose` and `prune` callbacks get the data, then Vite clears it; a later re-import starts with an empty object.

```js
import.meta.hot.data.someValue = 'hello'        // ok
import.meta.hot.data = { someValue: 'hello' }   // not supported
```

`hot.decline()` is currently a noop kept for compatibility. To mark a module not hot-updatable use `hot.invalidate()`.

## Checked

2026-11-07. Confirmed against guide/api-hmr.md, read in full: `hot.dispose`, `hot.prune` (used for `.css` imports), `hot.data` persistence, prune and clearing behaviour, the no-reassignment rule with its two examples, and `hot.decline()` as a noop with `hot.invalidate()` as the alternative. Nothing removed.

Method: documentation only; no commands were run.
