---
id: computing-software.web-development.vite.js-api-transform-preprocess
name: js-api-transform-preprocess
category: computing-software
field: web-development
product: vite
tags: [transform-with-oxc, transform-with-esbuild-deprecated, preprocess-css, css-module-inference]
level: advanced
status: docs-checked
description: "Use transformWithOxc in plugins (transformWithEsbuild deprecated) and experimental preprocessCSS to compile Sass, Less or Stylus to plain CSS with CSS module detection."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-javascript.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`transformWithOxc(code, filename, options?, inMap?)` transforms JS or TS with the Oxc Transformer, for plugins that want to match Vite's internal transform. It returns the Oxc result without `errors`, plus `warnings: string[]`. `transformWithEsbuild` is deprecated; use `transformWithOxc`.

`preprocessCSS(code, filename, config)` (experimental) turns `.css`, `.scss`, `.sass`, `.less`, `.styl` and `.stylus` into plain CSS for browsers or other tools:

```ts
interface PreprocessCSSResult {
  code: string
  map?: SourceMapInput
  modules?: Record<string, string>
  deps?: Set<string>
}
```

The preprocessor is inferred from the `filename` extension and must be installed, as with built-in CSS pre-processing. A name ending in `.module.{ext}` is treated as a CSS module, and `modules` maps original class names to transformed ones. Pre-processing does not resolve URLs in `url()` or `image-set()`.

## Checked

2026-11-07. Confirmed against the `transformWithOxc`, `transformWithEsbuild` and `preprocessCSS` sections of guide/api-javascript.md (page read in full): signatures and the result shape, the deprecation note, experimental status, supported extensions, extension-based inference, `.module.{ext}` handling and the `url()`/`image-set()` limitation. Nothing removed.

Method: documentation only; no commands were run.
