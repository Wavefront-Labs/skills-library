---
id: computing-software.web-development.vite.web-workers
name: web-workers
category: computing-software
field: web-development
product: vite
tags: [web-worker, worker-query-suffix, shared-worker, worker-inline]
level: practitioner
status: docs-checked
description: "Bundle web workers with new Worker(new URL(...)) or the ?worker, ?sharedworker, ?worker&inline and ?worker&url suffixes, with the static-option rules."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/assets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Recommended: the standards-closer constructor form (also `new SharedWorker()`):

```ts
const worker = new Worker(new URL('./worker.js', import.meta.url), {
  type: 'module',
})
```

Detection only works when `new URL()` is written directly inside `new Worker()`; otherwise it is a static asset URL. All option values must be static (string literals).

Query suffixes give a custom worker constructor as default export:

```js
import MyWorker from './worker?worker'
import SharedW from './worker?sharedworker'
import Inline from './worker?worker&inline' // base64 in the bundle
import workerUrl from './worker?worker&url'
const worker = new MyWorker()
```

Notes:
- Worker scripts can use ESM `import` instead of `importScripts()`. In dev this relies on browser module-worker support; in production it is compiled away.
- By default the worker is a separate chunk in production.
- Configure bundling of all workers with the worker options.

## Checked

2026-11-07. Re-read the Features guide (docs/guide/features.md) in full, Web Workers section, and the Static Asset Handling guide (docs/guide/assets.md) in full. Confirmed the new Worker(new URL(...)) form, the direct-use and static-option rules, the ?worker, ?sharedworker, ?worker&inline and ?worker&url suffixes, ESM import in workers, the separate chunk default and the pointer to Worker Options. Nothing removed.

Method: documentation only; no commands were run.
