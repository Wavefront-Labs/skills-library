---
id: computing-software.web-development.vite.static-asset-imports
name: static-asset-imports
category: computing-software
field: web-development
product: vite
tags: [asset-url-import, assets-include, asset-inlining, raw-import]
level: practitioner
status: docs-checked
description: "Import static assets as URLs, with ?url, ?inline, ?no-inline and ?raw suffixes; hashed names, assetsInclude, and the assetsInlineLimit base64 rule."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/assets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Importing an asset returns its resolved public URL: `/src/img.png` in dev, a hashed `/assets/img.2d8efhg.png` in the build. CSS `url()` is handled the same way.

```js
import imgUrl from './img.png'
import workletURL from 'extra-scalloped-border/worklet.js?url'
import a from './img.svg?no-inline'
import b from './img.png?inline'
import shader from './shader.glsl?raw'
```

- Common image, media and font types are detected automatically; extend with `assetsInclude`. Others use `?url`.
- Assets below `build.assetsInlineLimit` bytes are inlined as base64. The inline and no-inline query suffixes (as in the imports above) force the choice.
- Git LFS placeholders are never inlined; download the real files before building.
- TypeScript needs `vite/client` to recognise asset imports.
- SVG URLs put into a hand-built CSS `url()` need double quotes: `` `url("${imgUrl}")` ``.

## Checked

2026-11-07. Re-read the Static Asset Handling guide (docs/guide/assets.md) in full. Confirmed the dev and build URL examples, CSS url() handling, ?url, ?inline, ?no-inline and ?raw suffixes, assetsInclude, the assetsInlineLimit base64 rule, Git LFS placeholders, the vite/client types note and the SVG double-quote tip. Nothing removed.

Method: documentation only; no commands were run.
