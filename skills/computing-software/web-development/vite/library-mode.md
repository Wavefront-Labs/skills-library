---
id: computing-software.web-development.vite.library-mode
name: library-mode
category: computing-software
field: web-development
product: vite
tags: [library-mode, build-lib, externalize-dependencies, umd-globals]
level: practitioner
status: docs-checked
description: "Bundle a library with build.lib: single and multiple entries, externalized dependencies with output.globals, default es/umd/cjs formats, and when to use tsdown."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/build.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `index.html` as the demo page in dev; bundle for distribution with `build.lib`. Externalize dependencies you do not want bundled (such as `vue` or `react`).

```js
import { resolve } from 'node:path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    lib: {
      entry: resolve(import.meta.dirname, 'lib/main.js'),
      name: 'MyLib',
      fileName: 'my-lib', // proper extensions are added
    },
    rolldownOptions: {
      external: ['vue'],
      output: { globals: { vue: 'Vue' } },
    },
  },
})
```

Multiple entries: make `entry` an object such as `{ 'my-lib': ..., secondary: ... }`.

Default formats: `es` and `umd` for a single entry; `es` and `cjs` for multiple. Override with `build.lib.formats`.

Without `"type": "module"` in `package.json`, extensions shift for Node.js compatibility: `.js` becomes `.mjs` and `.cjs` becomes `.js`.

For non-browser libraries or advanced flows, the docs suggest tsdown or Rolldown directly.

## Checked

2026-11-07. Confirmed against the "Library Mode" section of guide/build.md (page read in full): `build.lib` single and multiple entry examples, `rolldownOptions.external` and `output.globals`, default formats (`es` and `umd` for one entry, `es` and `cjs` for several) and `build.lib.formats`, the `"type": "module"` extension shift, and the tsdown or Rolldown advice. Nothing removed.

Method: documentation only; no commands were run.
