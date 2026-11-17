---
id: computing-software.web-development.vite.build-css-minify
name: build-css-minify
category: computing-software
field: web-development
product: vite
tags: [build-css-code-split, build-css-target, build-css-minify, build-minify, terser-options]
level: practitioner
status: docs-checked
description: "Build CSS and JS minification options: cssCodeSplit, cssTarget for odd browsers, cssMinify (lightningcss), minify oxc or terser, terserOptions and maxWorkers."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/build-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `build.cssCodeSplit` (default `true`): CSS from async chunks stays a chunk fetched with it. `false` extracts all CSS into one file. With `build.lib` the default is `false`.
- `build.cssTarget` (default `build.target`): separate CSS minify target for non-mainstream browsers. Example in the docs: Android WeChat WebView lacks `#RGBA` colors, so set `chrome61` to keep `rgba()`. With `cssMinify: 'lightningcss'` it beats `css.lightningcss.targets`.
- `build.cssMinify` (`boolean | 'lightningcss' | 'esbuild'`, default `'lightningcss'`, `false` if client `build.minify` is off). `'esbuild'` needs `npm add -D esbuild`.
- `build.minify` (`boolean | 'oxc' | 'terser' | 'esbuild'`): default `'oxc'` for client, `false` for SSR. Oxc is documented as 30 to 90x faster than terser with 0.5 to 2% worse compression. `'esbuild'` is deprecated. Terser needs `npm add -D terser`. In lib mode with the `es` format, whitespace is not minified, since that would remove pure annotations and break tree-shaking.
- `build.terserOptions`: Terser minify options plus `maxWorkers` (default CPUs minus 1).

## Checked

2026-11-04. Confirmed against the Vite build options page (docs/config/build-options.md): cssCodeSplit, cssTarget and the WeChat example, cssMinify, minify defaults, Oxc speed claim as stated by the docs, lib-mode whitespace note, terserOptions maxWorkers. Nothing removed.

Method: documentation only; no commands were run.
