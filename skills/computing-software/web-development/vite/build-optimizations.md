---
id: computing-software.web-development.vite.build-optimizations
name: build-optimizations
category: computing-software
field: web-development
product: vite
tags: [css-code-splitting, modulepreload, async-chunk-loading, chunk-import-map]
level: advanced
status: docs-checked
description: "Automatic Vite build optimizations: CSS code splitting, modulepreload directives, parallel async chunk preloading, and the opt-in chunk import map."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/build-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Applied automatically (except the chunk import map) and needing configuration only to disable.

- CSS code splitting: CSS used by an async chunk goes in its own file, loaded by `<link>` before the chunk evaluates (avoids FOUC). One file instead: `build.cssCodeSplit: false`.
- Preload directives: `<link rel="modulepreload">` for entry chunks and their direct imports in built HTML.
- Async chunk loading: for `Entry -> A -> C`, Vite rewrites dynamic imports with a preload step so `C` is fetched in parallel with `A`, tracing imports to any depth.
- Chunk import map (opt-in, experimental, default `false`): `build.chunkImportMap: true`; it needs browser `import.meta.resolve` support. Chunks import via IDs mapped to URLs, so updating `C` does not invalidate `A` or the entry. It does not yet apply to CSS and assets; updating an asset invalidates the chunks referencing it, without cascading.

```js
export default { build: { chunkImportMap: true } }
```

## Checked

Date: 2026-11-07. Read the Build Optimizations section of features.md (features.md read in full) and the `build.chunkImportMap` and `build.cssCodeSplit` sections of build-options.md (read in full). Added the experimental flag, default and the `import.meta.resolve` requirement from build-options.md. Other bullets matched the page text.

Method: documentation only; no commands were run.
