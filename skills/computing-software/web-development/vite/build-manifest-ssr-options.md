---
id: computing-software.web-development.vite.build-manifest-ssr-options
name: build-manifest-ssr-options
category: computing-software
field: web-development
product: vite
tags: [build-manifest-option, build-ssr-manifest, build-ssr-option, build-emit-assets, build-license-option]
level: advanced
status: docs-checked
description: "Options build.manifest and ssrManifest paths, build.ssr entry, emitAssets and ssrEmitAssets, build.license output file or JSON, chunkImportMap, and build.watch."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/build-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `build.manifest` (`boolean | string`, default `false`): maps unhashed asset names to hashed ones. `true` writes `.vite/manifest.json`; a string is a path relative to `outDir`. Plugin authors can use `viteMetadata` bundle metadata.
- `build.ssrManifest`: same shape; `true` writes `.vite/ssr-manifest.json`, for style links and preload directives in production.
- `build.ssr` (`boolean | string`): SSR-oriented build. A string is the entry; `true` needs `input` or `build.rolldownOptions.input`.
- `build.emitAssets` (default `false`): non-client builds skip static assets; frameworks can force emitting and must merge them afterwards. `build.ssrEmitAssets` is the SSR-only equivalent, to be replaced by `emitAssets` once the Environment API is stable.
- `build.license` (`boolean | { fileName? }`): `true` writes `.vite/license.md` of bundled dependency licenses. `fileName` is relative to `outDir`; a `.json` name emits raw metadata (name, version, identifier, text). Reference it in code with `build.rolldownOptions.output.postBanner`.
- `build.chunkImportMap` (experimental, default `false`): import maps for chunk cache efficiency; needs `import.meta.resolve` support.
- `build.watch` (`WatcherOptions | null`, default `null`): `{}` enables the Rolldown watcher. WSL2 limits apply as in `server.watch`.

## Checked

2026-11-04. Confirmed against the Vite build options page (docs/config/build-options.md): manifest and ssrManifest paths, ssr, emitAssets, ssrEmitAssets, license output, chunkImportMap, watch. Nothing removed.

Method: documentation only; no commands were run.
