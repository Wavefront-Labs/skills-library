---
id: computing-software.web-development.vite.build-output-assets
name: build-output-assets
category: computing-software
field: web-development
product: vite
tags: [build-out-dir, build-assets-dir, assets-inline-limit, build-empty-out-dir, copy-public-dir]
level: practitioner
status: docs-checked
description: "Output location and asset options: outDir, assetsDir, assetsInlineLimit callback and Git LFS, emptyOutDir warning, copyPublicDir, write and reportCompressedSize."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/build-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `build.outDir` (default `dist`), relative to the project root.
- `build.assetsDir` (default `assets`), relative to `outDir`; unused in library mode.
- `build.assetsInlineLimit` (`number | (filePath, content) => boolean | undefined`, default `4096`): smaller assets inline as base64. `0` disables. A callback returns a boolean to opt in or out, `undefined` keeps the default. Git LFS placeholders are never inlined. With `build.lib`, assets always inline regardless of size.
- `build.emptyOutDir` (default `true` if `outDir` is inside `root`): outside root Vite warns instead; set it explicitly to silence. CLI: `--emptyOutDir`.
- `build.copyPublicDir` (default `true`): `false` skips copying `publicDir`.
- `build.write` (default `true`): `false` skips writing to disk, for programmatic `build()` post-processing.
- `build.reportCompressedSize` (default `true`): gzip size reporting; disabling speeds large builds.
- `build.chunkSizeWarningLimit` (default `500` kB), compared with uncompressed chunk size.
- `build.sourcemap` (`boolean | 'inline' | 'hidden'`, default `false`): `true` writes a separate file, `inline` appends a data URI, `hidden` omits the sourcemap comments.

## Checked

2026-11-04. Confirmed against the Vite build options page (docs/config/build-options.md): outDir, assetsDir, assetsInlineLimit callback and Git LFS note, emptyOutDir, copyPublicDir, write, reportCompressedSize, chunkSizeWarningLimit, sourcemap. Nothing removed.

Method: documentation only; no commands were run.
