---
id: computing-software.web-development.vite.migration-v8-minify-cjs
name: migration-v8-minify-cjs
category: computing-software
field: web-development
product: vite
tags: [oxc-minifier, cjs-interop-default, format-sniffing-removed, esm-external-require]
level: advanced
status: docs-checked
description: "Vite 8 behaviour changes: Oxc JS and Lightning CSS minifiers, consistent CommonJS default import rules, removed format sniffing, preserved require calls, import.meta.url in UMD."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/migration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Minification: Oxc minifies JS (the deprecated `build.minify: 'esbuild'` switches back; install `esbuild` yourself). Use `build.rolldownOptions.output.minify` for former `esbuild.minify*` options and `...minify.compress.drop*` for `esbuild.drop`. Property mangling is unsupported. Lightning CSS minifies CSS; `build.cssMinify: 'esbuild'` reverts.

CJS interop: a `default` import is the importee's `module.exports` if the importer is `.mjs`/`.mts`, or its closest `package.json` has `type: module`, or `__esModule` is not true; otherwise it is `module.exports.default`. `legacy.inconsistentCjsInterop: true` temporarily restores the old behaviour.

Other changes:
- Format sniffing for `browser` versus `module` fields is gone; `resolve.mainFields` order is always respected (use `resolve.alias` or a patch otherwise).
- `require` calls for externalized modules stay `require`; `esmExternalRequirePlugin` (exported by `vite`) converts them.
- `import.meta.url` is replaced with `undefined` in UMD/IIFE output unless you use `define` plus `output.intro`.
- `build.rollupOptions.watch.chokidar` is removed; use `build.rolldownOptions.watch.watcher`.
- Object-form `manualChunks` is removed and function form deprecated; use `codeSplitting`.
- In plugins, `load`/`transform` returning JS from other module types may need `moduleType: 'js'`.

## Checked

Date: 2026-11-07

Read migration.md in full. Confirmed: Oxc minifier and build.minify esbuild fallback, build.rolldownOptions.output.minify and compress.drop*, property mangling unsupported, Lightning CSS and build.cssMinify esbuild, the three CommonJS default-import conditions and legacy.inconsistentCjsInterop, removed format sniffing and resolve.mainFields, preserved require calls and esmExternalRequirePlugin re-exported from vite, import.meta.url in UMD/IIFE, watch.chokidar to watch.watcher, manualChunks, moduleType js. Nothing removed.

Method: documentation only; no commands were run.
