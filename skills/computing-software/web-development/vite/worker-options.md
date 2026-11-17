---
id: computing-software.web-development.vite.worker-options
name: worker-options
category: computing-software
field: web-development
product: vite
tags: [worker-format, worker-plugins, worker-rolldown-options]
level: practitioner
status: docs-checked
description: "Worker bundle config: worker.format (iife default), worker.plugins as a function returning fresh instances for builds, and worker.rolldownOptions."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/worker-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Applied to dev, build and preview.

- `worker.format` (`'es' | 'iife'`, default `'iife'`): output format of the worker bundle.
- `worker.plugins` (`() => (Plugin | Plugin[])[]`): plugins for worker bundles. Top-level `plugins` only applies to workers in dev, so configure build workers here. The function must return new plugin instances, since they run in parallel Rolldown worker builds; changing `config.worker` in a plugin `config` hook is ignored.
- `worker.rolldownOptions`: Rolldown options for the worker bundle. `worker.rollupOptions` is a deprecated alias.

```js
export default defineConfig({
  worker: {
    format: 'es',
    plugins: () => [/* fresh plugin instances */],
  },
})
```

## Checked

2026-11-07. Re-read the Worker Options page (docs/config/worker-options.md) in full. Confirmed worker.format (es or iife, default iife), worker.plugins (function returning new instances, top-level plugins only apply to workers in dev, config hook changes ignored), worker.rolldownOptions and the deprecated worker.rollupOptions alias. Nothing removed.

Method: documentation only; no commands were run.
