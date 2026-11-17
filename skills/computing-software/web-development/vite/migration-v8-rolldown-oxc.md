---
id: computing-software.web-development.vite.migration-v8-rolldown-oxc
name: migration-v8-rolldown-oxc
category: computing-software
field: web-development
product: vite
tags: [migrate-from-v7, rolldown-vite, esbuild-to-oxc, optimize-deps-rolldown-options]
level: advanced
status: docs-checked
description: "Migrating Vite 7 to 8: the new default targets, rolldown-vite path, esbuild option to oxc and optimizeDeps.esbuildOptions to rolldownOptions mappings, esbuild optional."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/migration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default `build.target` (`baseline-widely-available`) moved: Chrome 107 to 111, Edge 107 to 111, Firefox 104 to 114, Safari 16.0 to 16.4.

Vite 8 uses Rolldown and Oxc instead of esbuild and Rollup. `rolldown-vite` (Vite 7 with Rolldown) is an intermediate step; leave it by setting `"vite": "^8.0.0"`.

- `optimizeDeps.esbuildOptions` is deprecated but auto-converted to `optimizeDeps.rolldownOptions`: `minify` to `output.minify`, `treeShaking` to `treeshake`, `define` to `transform.define`, `loader` to `moduleTypes`, `resolveExtensions` to `resolve.extensions`, `mainFields` to `resolve.mainFields`, `conditions` to `resolve.conditionNames`, `keepNames` to `output.keepNames`, `platform`, and `plugins` (partial).
- `esbuild` option is deprecated but auto-converted to `oxc`: `jsxInject`, `include`, `exclude`, `jsx` (`automatic` becomes `{ runtime: 'automatic' }`, `transform` becomes `runtime: 'classic'`), `define`. `banner` and `footer` need a transform-hook plugin; `esbuild.supported` is unsupported.
- Inspect converted values in `configResolved` via `config.oxc` or `config.optimizeDeps.rolldownOptions`.
- Oxc does not lower native decorators yet; use Babel or SWC plugins as the workaround.
- esbuild is now an optional dependency. `transformWithEsbuild` is deprecated in favour of `transformWithOxc`.

## Checked

2026-11-04. Confirmed against the Vite migration guide (docs/guide/migration.md): new target versions, rolldown-vite step, the esbuildOptions to rolldownOptions and esbuild to oxc mapping lists, configResolved inspection, native decorators limitation, esbuild optional dependency and transformWithOxc. Nothing removed.

Method: documentation only; no commands were run.
