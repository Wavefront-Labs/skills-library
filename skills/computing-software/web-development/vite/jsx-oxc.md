---
id: computing-software.web-development.vite.jsx-oxc
name: jsx-oxc
category: computing-software
field: web-development
product: vite
tags: [jsx-support, oxc-jsx-options, jsx-inject, preact-jsx]
level: practitioner
status: docs-checked
description: "Configure JSX in Vite with the oxc option: importSource for Preact, and the Vite-only jsxInject to avoid manual imports."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.jsx` and `.tsx` work out of the box, transpiled by the Oxc Transformer. Framework plugins normally configure JSX for you (Vue users should use `@vitejs/plugin-vue-jsx`).

For your own framework, use the `oxc` option:

```js
import { defineConfig } from 'vite'

export default defineConfig({
  oxc: {
    jsx: {
      importSource: 'preact',
    },
  },
})
```

Custom `jsxFactory` and `jsxFragment` are also configured here; details are in the Oxc Transformer JSX docs.

`jsxInject` is a Vite-only option that injects helper imports so you need not write them manually:

```js
export default defineConfig({
  oxc: { jsxInject: `import React from 'react'` },
})
```

## Checked

2026-11-07. Confirmed against the "JSX" section of guide/features.md (read in full, including the Dynamic Import, Glob Import, JSON, JSX, HTML and TypeScript sections): `.jsx`/`.tsx` handled by the Oxc Transformer, Vue users and `@vitejs/plugin-vue-jsx`, `oxc.jsx.importSource` for Preact, custom `jsxFactory` and `jsxFragment` via the `oxc` option, and `oxc.jsxInject` as a Vite-only option. Nothing removed.

Method: documentation only; no commands were run.
