---
id: computing-software.web-development.vite.using-plugins
name: using-plugins
category: computing-software
field: web-development
product: vite
tags: [plugins-array, plugin-enforce, plugin-apply, plugin-registry]
level: practitioner
status: docs-checked
description: "Use Vite plugins: add one to plugins, presets and falsy entries, order with enforce pre/post, limit with apply build or serve, and find plugins."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/using-plugins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Plugins build on Rollup's plugin interface plus Vite-specific options. Install as a devDependency and list in `plugins`:

```js
import legacy from '@vitejs/plugin-legacy'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [legacy({ targets: ['defaults', 'not IE 11'] })],
})
```

`plugins` also accepts presets (arrays of several plugins, flattened internally). Falsy entries are ignored, which makes toggling easy.

Order with `enforce`:
- `pre`: before Vite core plugins
- default: after Vite core plugins
- `post`: after Vite build plugins

Restrict to one command with `apply: 'build'` or `apply: 'serve'`; by default plugins run for both:

```js
plugins: [{ ...typescript2(), apply: 'build' }]
```

Check the Features guide first; many cases that need plugins in Rollup are built into Vite. Community plugins are listed in the Vite Plugin Registry.

## Checked

2026-11-07. Re-read the Using Plugins guide (docs/guide/using-plugins.md) in full. Confirmed Rollup-based plugin interface, devDependencies plus plugins array, presets and falsy entries, the Features Guide first note, the Vite Plugin Registry, enforce pre/default/post ordering and apply 'build' or 'serve'. Nothing removed.

Method: documentation only; no commands were run.
