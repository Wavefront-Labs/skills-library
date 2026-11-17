---
id: computing-software.web-development.vite.lightning-css
name: lightning-css
category: computing-software
field: web-development
product: vite
tags: [lightningcss, css-transformer, css-minification]
level: advanced
status: docs-checked
description: "Lightning CSS in Vite: default CSS minifier in builds, the experimental css.transformer lightningcss opt-in, and where CSS Modules options move."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vite minifies CSS in production builds with Lightning CSS by default; PostCSS still does the other CSS processing.

Experimental: process all CSS with Lightning CSS by opting in:

```js
import { defineConfig } from 'vite'

export default defineConfig({
  css: {
    transformer: 'lightningcss',
    lightningcss: {
      // Lightning CSS options
    },
  },
})
```

Pass Lightning CSS options through `css.lightningcss`. Configure CSS Modules with `css.lightningcss.cssModules`, not `css.modules` (which configures PostCSS's handling).

## Checked

Date: 2026-11-07

Read features.md in full (Lightning CSS section) and shared-options.md in full (css.transformer, css.lightningcss, css.modules). Confirmed: Lightning CSS minifies CSS in builds by default, PostCSS still does other processing, css.transformer lightningcss is experimental, css.lightningcss.cssModules replaces css.modules. Nothing removed.

Method: documentation only; no commands were run.
