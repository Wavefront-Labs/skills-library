---
id: computing-software.web-development.vite.build-manifest
name: build-manifest
category: computing-software
field: web-development
product: vite
tags: [vite-manifest, manifest-chunk, is-entry, dynamic-imports-manifest]
level: advanced
status: docs-checked
description: "Read .vite/manifest.json: the ManifestChunk fields, entry, dynamic entry, non-entry, asset and CSS key rules, and the css-code-split key difference."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/backend-integration.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/build-options.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/ssr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`build.manifest` (`boolean | string`, default `false`): `true` makes `vite build` write `.vite/manifest.json` beside the assets; a string is the manifest path relative to `build.outDir`. It is a `Record<name, chunk>`; each chunk follows `ManifestChunk`:

- `file`: output file name
- `src?`: input file name if known
- `name?`: chunk or asset name if known
- `isEntry?`, `isDynamicEntry?` (JS chunks only)
- `imports?`, `dynamicImports?`: arrays of manifest keys (JS chunks only)
- `css?`: CSS files imported by the chunk
- `assets?`: non-CSS asset files imported by the chunk

Key rules:
- Entry chunks (from `build.rolldownOptions.input`): `isEntry: true`, key is the src path relative to the project root.
- Dynamic entry chunks: `isDynamicEntry: true`, key is the relative src path.
- Non-entry chunks: key is the generated file's base name prefixed with `_`.
- Asset chunks (images, fonts): key is the relative src path.
- CSS: with `build.cssCodeSplit: false` one file keyed `style.css`; otherwise keyed like JS chunks (entry without `_`, non-entry with `_`).

The `Manifest` and `ManifestChunk` types are exported from `vite`. For SSR, `build.ssrManifest` (or the `--ssrManifest` CLI flag) writes a separate `.vite/ssr-manifest.json`.

## Checked

Date: 2026-11-07. Read backend-integration.md in full (example manifest, ManifestChunk interface, key rules list) and build-options.md (read in full) (`build.manifest`, `build.ssrManifest`, `build.cssCodeSplit`). ssr.md was only searched, not read in full: the `--ssrManifest` line writing `.vite/ssr-manifest.json` was confirmed. Added the string form and default of `build.manifest` and the exact ssr-manifest path; the `Manifest`/`ManifestChunk` exports from `vite` are confirmed by the page's `import type` line.

Method: documentation only; no commands were run.
