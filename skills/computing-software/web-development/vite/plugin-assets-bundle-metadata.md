---
id: computing-software.web-development.vite.plugin-assets-bundle-metadata
name: plugin-assets-bundle-metadata
category: computing-software
field: web-development
product: vite
tags: [vite-metadata, emit-file-asset, rolldown-file-url, vite-asset-token, chunk-import-map-plugin]
level: advanced
status: docs-checked
description: "Plugin build APIs: viteMetadata importedCss and importedAssets, emitFile asset references in JS, CSS and HTML, and reading the chunk import map in generateBundle."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Output bundle metadata: chunks and assets expose `viteMetadata.importedCss` and `viteMetadata.importedAssets` (both `Set<string>`) on `RenderedChunk` (`renderChunk`, `augmentChunkHash`) and `OutputChunk` / `OutputAsset` (`generateBundle`, `writeBundle`). Use them instead of `build.manifest` to inspect emitted CSS and assets.

```ts
generateBundle(_, bundle) {
  for (const output of Object.values(bundle)) {
    const css = output.viteMetadata?.importedCss
  }
}
```

Emitted assets: `this.emitFile({ type: 'asset', name, source })` returns a `referenceId`; the final name is unknown until generation.
- In JS: `import.meta.ROLLDOWN_FILE_URL_<referenceId>`, a JS expression, so append query or hash by string concatenation.
- In CSS or HTML: the token `__VITE_ASSET__<referenceId>__` with any query or hash right after, e.g. `url(__VITE_ASSET__<referenceId>__#frag)`.

Chunk import map (experimental, with `build.chunkImportMap`): chunk imports use unique IDs. In `generateBundle` or `writeBundle`, read the emitted asset named by `build.rolldownOptions.experimental.chunkImportMap.fileName` (default `importmap.json`) and parse `.imports` for the ID-to-file mapping.

## Checked

Date: 2026-11-07

Read api-plugin.md in full (Output Bundle Metadata, Referencing Emitted Assets, Chunk Import Map Information). Confirmed viteMetadata fields and hook locations, emitFile referenceId, import.meta.ROLLDOWN_FILE_URL_<referenceId>, the __VITE_ASSET__ token, build.chunkImportMap and the importmap.json default and .imports. Nothing removed.

Method: documentation only; no commands were run.
